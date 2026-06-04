from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from web3 import Web3
import os
import logging
from dotenv import load_dotenv
from config.config import chains_data, SessionLocal
from app.models.models import User
from sqlalchemy.orm.attributes import flag_modified


logging.basicConfig(
    filename='logs/evm_address_control.log',
    level=logging.ERROR,#INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", "config", ".env"))

mnemonic = os.getenv("SEED_PHRASE")

# mnemonic → seed
seed = Bip39SeedGenerator(mnemonic).Generate()

# seed → HD wallet 
bip44_ctx = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)

# 4billion addresses from index 0

base_addr_index = int(os.getenv("gen_addr_index"))

def generate_evm_address(addr_index):
    addr_index = base_addr_index + addr_index

    addr = (bip44_ctx
            .Purpose()
            .Coin()
            .Account(0)
            .Change(Bip44Changes.CHAIN_EXT)
            .AddressIndex(addr_index)
            .PublicKey()
            .ToAddress())
    return addr

erc20_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function",
        }
    ]


def get_balance(address, token_address, rpc_url):

    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url)) 
    except Exception:
        logging.exception("Failed to connect to the network RPC")
        return {
            "data": None,
            "error": f"Failed to connect to the network RPC"
        } 
    try:
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=erc20_abi
        )

        balance = contract.functions.balanceOf(
            Web3.to_checksum_address(address)
        ).call()

        decimals = contract.functions.decimals().call()
    except Exception:
        logging.exception("Failed to get balance from blockchain")
        return {
            "data": None,
            "error": f"Failed to get balance from blockchain"
        } 

    return {
            "data": balance / 10**decimals,
            "error": None
        } 
  

subscription_price = float(os.getenv("SUBSCRIPTION_PRICE"))


def check_transfer(chain, user_id):
    chain_data = chains_data.get('EVM').get(chain)
    if not chain_data:
        return {
            "transfer_received": None,
            "error": "The network is not supported for checking"
        }
    rpc_url = chain_data.get('RPC_URL')
    usdt_token_address = chain_data.get('USDT_TOKEN_ADDRESS')

    db = SessionLocal()

    user = db.query(User).filter_by(id=user_id).first()
    user_data = user.addresses_data[chain]
    user_address = user_data['address']
    last_balance = user_data['last_balance']
    new_transfer = get_balance(user_address, usdt_token_address, rpc_url)
    data, error = new_transfer.values()

    answer = {"transfer_received": None,
              "error": None}

    if error:
        user.is_subscribed = None
        # logging.info(f'Cannot check deposit for user.id: {user.id}')    
        answer['transfer_received'] = None
        answer["error"] = error
    elif data <= last_balance:
        # if user.is_subscribed is None:
        #     user.is_subscribed = False
        #     logging.info(f'Problematic deposit has been checked for user.id: {user.id}') 
        answer['transfer_received'] = False
        answer["error"] = 'transfer not found'
    elif data - last_balance < subscription_price:
        answer['transfer_received'] = False
        answer["error"] = 'amount less than subscription price'
    else:
        user.is_subscribed = True
        user.addresses_data[chain]['last_balance'] = data
        flag_modified(user, "addresses_data")
        answer['transfer_received'] = True
        answer["error"] = None
    db.commit()
    db.close()
    return answer

