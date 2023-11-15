#!/usr/bin/env bash
# this checks the timestamp of the latest block
# compares it with the time to see how many seconds the node is out of sync

apicall=$(curl -s -XPOST -H 'Content-Type: application/json' --data '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest", false],"id":1}' http://127.0.0.1:8545 > /tmp/call.json)
latestblocktimestamp=$(cat /tmp/call.json | jq -r '.result.timestamp' | tr -d '\n' |  xargs -0 printf "%d")
latestblocknumber=$(cat /tmp/call.json | jq -r '.result.number' | tr -d '\n' |  xargs -0 printf "%d")
currentdate=$(date +%s)

echo "BlockNumber: $latestblocknumber"
echo "BlockNumberTimestamp: $latestblocktimestamp"
echo "TimeDifference: $(($currentdate - $latestblocktimestamp))s"
