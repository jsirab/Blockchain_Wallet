


# Import dependencies
import subprocess
import json
from web3 import Web3

# Load and set environment variablesfrom dotenv import load_dotenv
from dotenv import load_dotenv
import os
load_dotenv()
mnemonic=os.getenv("mnemonic")


# Import constants.py and necessary functions from bit and web3 
from constants import * 
from decimal import Decimal
from bit import Key, PrivateKey, PrivateKeyTestnet
from bit.network import NetworkAPI
from bit import *
from web3 import Web3
from eth_account import Account

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = f'./derive -g --mnemonic="{mnemonic}" --numderive="{numderive}" --coin="{coin}" --format=json' 
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)



# Create a dictionary object called coins to store the output from `derive_wallets`.
coins ={ ETH : derive_wallets(mnemonic,ETH,3),
         BTCTEST : derive_wallets(mnemonic,BTCTEST,3)
}
coins


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    return None 

print(coin)
print(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == ETH: 
        gasEstimate = w3.eth.estimateGas(
            {"from":account.address, "to":to, "value": amount}
        )
        return { 
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_acc.address)
        }
    
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin,account,to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    if coin == ETH:
        signed_tx = account.sign_transaction(raw_tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result.hex()
    elif coin == BTCTEST:
        signed_tx = account.sign_transaction(rawt_x)
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

print(priv_key_to_account )    
