#!/usr/bin/env python3

"""
This runs on the Sepolia testnet (the formatting of the blockexplorer)
"""

import os
from web3 import Web3

ethereum_rpc_endpoint = 'http://localhost:8545'
web3 = Web3(Web3.HTTPProvider(ethereum_rpc_endpoint))

# Sender and Recipient Details
sender_address = os.environ['ETH_SENDER_ADDRESS'] # your wallet address
recipient_address = os.environ['ETH_RECIPIENT_ADDRESS']
private_key = os.environ['ETH_PRIVATE_KEY']

# Transaction Value and Gas
balance = web3.eth.get_balance(sender_address)
balance_in_ether = web3.from_wei(balance, 'ether')
wei_to_send = web3.to_wei(0.01, 'ether')
gas_price = web3.eth.gas_price
nonce = web3.eth.get_transaction_count(sender_address)

# ChainID
chain_id = web3.eth.chain_id

# Transaction with EIP-155 Replay Protection
tx = {
  'nonce': nonce, 
  'to': recipient_address, 
  'value': wei_to_send, 
  'gas': 21000, 
  'gasPrice': gas_price, 
  'chainId': chain_id
}

# Signing the Transaction
signed_tx = web3.eth.account.sign_transaction(tx, private_key)

# Sending the Transaction
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Transaction Hash
print(f'Transaction sent, hash: {tx_hash.hex()}')
print(f'Blockexplorer URL: https://sepolia.etherscan.io/tx/{tx_hash.hex()}')

# List the balance
balance = web3.eth.get_balance(sender_address)
balance_in_ether = web3.from_wei(balance, 'ether')
print(f'Available balance: {balance_in_ether} ETH')
