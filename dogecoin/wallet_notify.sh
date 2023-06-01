#!/usr/bin/env bash
balance=$(curl -s -u "rpcuser:rpcpass" -d '{"jsonrpc": "1.0", "id": "curl", "method": "getbalance", "params": ["main"]}' -H 'content-type: text/plain;' http://127.0.0.1:44555/ | jq -r '.result')
echo "[$(date +%FT%T)] $1 $2" >> /var/log/wallet-notify.log
python3 /opt/scripts/wait_for_confirmations.py $1
