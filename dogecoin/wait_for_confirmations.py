#!/usr/bin/env python3

# the dogecoin.conf has a walletnotify parameter, 
# the script can be found in the same directory
# walletnotify=/opt/scripts/wallet_notify.sh %s %w
#

import requests
import sys
from time import sleep as delay

import pytz
import socket
from pymongo import MongoClient
from datetime import datetime as dt

""" example of response
{'result': {'amount': 10.0, 'confirmations': 3, 'instantlock': True, 'instantlock_internal': True, 'chainlock': True, 'blockhash': 'x_blockhash_x', 'blockindex': 2, 'blocktime': 1633092283, 'txid': 'x_txid_x', 'walletconflicts': [], 'time': 1633092150, 'timereceived': 1633092150, 'details': [{'address': 'x_recipient-address_x', 'category': 'receive', 'amount': 10.0, 'label': '', 'vout': 1}], 'hex': 'x'}, 'error': None, 'id': 'requests'}
"""

# env vars
wallet_node_username = "rpcuser"
wallet_node_password = "rpcpass"
wallet_node_base_url = "http://127.0.0.1:44555"
wallet_name = "main"
transaction_id = sys.argv[1]
crypto_symbol = "DOGE"
crypto_name = "Dogecoin"
rpc_username = "rpcuser"
rpc_password = "rpcpass"
rpc_port = "44555"

tz_sast = "Africa/Johannesburg"
mongodb_uri = "mongodb://mongodb-rs-0:30001,mongodb-rs-1:30002,mongodb-rs-2:30003/?replicaSet=rs0"
hostname = socket.gethostname()

def get_transaction(wallet_name, txid):
    request_url = wallet_node_base_url
    request_headers = {"content-type": "text/plain"}
    request_data = {"jsonrpc": "1.0", "id": "curl", "method": "gettransaction", "params": [txid]}
    response = requests.post(request_url, headers=request_headers, auth=(wallet_node_username, wallet_node_password), json=request_data)
    return response.json()

def get_blockhash(wallet_name, transaction_id):
    current_blockhash = 0
    while current_blockhash == 0:
        txinforaw = get_transaction(wallet_name, transaction_id)
        if 'blockhash' in txinforaw['result'].keys():
            current_blockhash = 1
        else:
            delay(5)
    return txinforaw

def parse_response(payloadraw):
    payload = payloadraw['result']
    parsed = {'amount': payload['amount'], 'confirmations': payload['confirmations'], 'txid': payload['txid'], 'time': payload['time'], 'timereceived': payload['timereceived'], 'address': payload['details'][0]['address'], 'blockhash': payload['blockhash']}
    return parsed

def get_balance(wallet):
    request_url = "http://127.0.0.1:{port}/".format(port=rpc_port)
    headers = {"content-type": "text/plain"}
    request_data = {"jsonrpc": "1.0", "id": "curl", "method": "getbalance", "params": [wallet]}
    response = requests.post(request_url, headers=headers, json=request_data, auth=(rpc_username, rpc_password))
    json_response = response.json()
    return json_response

def insert_balance_into_mongodb(network_name, wallet, crypto_symbol, crypto_name, metric_value, txid, tx_amount):
    client = MongoClient(mongodb_uri)
    db = client.crypto_wallets
    balances = db.balances
    doc_key = {'txid': txid}
    doc_data = {'timestamp': dt.now(pytz.timezone(tz_sast)), 'crypto_symbol': crypto_symbol, 'crypto_name': crypto_name, 'amount': tx_amount, 'balance': metric_value, 'node_name': hostname, 'network_name': network_name, 'wallet_name': wallet, 'txid': txid}
    #doc_data = {'timestamp': dt.now(pytz.timezone(tz_sast)), 'crypto_symbol': crypto_symbol, 'crypto_name': crypto_name, 'balance': metric_value, 'node_name': hostname, 'network_name': network_name, 'wallet_name': wallet, 'txid': txid}
    #response = balances.insert_one(doc_data)
    #response = balances.update(doc_key, doc_data, upsert = True)
    response = balances.update_one(doc_data,{"$set": doc_key}, upsert = True)
    return response

txinforaw = get_blockhash(wallet_name, transaction_id)
txinfo = parse_response(txinforaw)

confirmations = 0

while confirmations < 2:
    txinforaw = get_transaction(wallet_name, transaction_id)
    txinfo = parse_response(txinforaw)
    confirmations = txinfo['confirmations']
    tx_amount = txinfo['amount']
    print("not confirmed yet as {txid} has {confirmations} confirmations".format(txid=txinfo['txid'], confirmations=confirmations))
    delay(10)

print("txid {txid} has {confirmations} confirmations".format(txid=txinfo['txid'], confirmations=confirmations))
balance = get_balance("main")
mongodb_response = insert_balance_into_mongodb('testnet', 'main', crypto_symbol, crypto_name, balance['result'], transaction_id, tx_amount)
