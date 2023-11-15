#!/usr/bin/env python3

"""
Install:
 pip install eth_keys
 pip install eth-hash[pycryptodome]
 pip install bip-utils
 pip install mnemonic
"""

from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44, Bip44Changes

# Define a dictionary where we will store our values
body = {}

# Generate a random mnemonic in english
mnemo = Mnemonic("english")
mnemonic = mnemo.generate(256)
body['mnemonic'] = mnemonic

# Generate the seed from the mnemonic
seed = Bip39SeedGenerator(mnemonic).Generate()

# Generate the Bip44 wallet (Ethereum)
wallet = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)

# Get the first account
account = wallet.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)

# Extract the private key from the account
private_key = account.PrivateKey().Raw().ToHex()
body['private_key'] = private_key

# Extract the address from the account
address = account.PublicKey().ToAddress()
body['address'] = address

# Print the stored values
print(body)
