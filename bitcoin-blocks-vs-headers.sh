#!/usr/bin/env bash

headers=$(curl -s -u "bitcoinrpc:bitcoinpass" -d '{"jsonrpc": "1.0", "id": "bitcoind", "method": "getblockchaininfo", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:18332/ | jq -r '.result.headers')
blocks=$(curl -s -u "bitcoinrpc:bitcoinpass" -d '{"jsonrpc": "1.0", "id": "bitcoind", "method": "getblockchaininfo", "params": []}' -H 'content-type: text/plain;' http://127.0.0.1:18332/ | jq -r '.result.blocks')

echo "blocks=$blocks / headers=$headers"
echo "$headers - $blocks" | bc
