from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from web3 import Web3
import os
import copy
from dotenv import load_dotenv
from app.config import chains_data, SessionLocal
from app.models.models import User
from sqlalchemy.orm.attributes import flag_modified

db = SessionLocal()


ENV='dev'
if ENV == 'dev':
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
else:
    load_dotenv(".env")
# 1. твоя seed phrase
mnemonic = os.getenv("SEED_PHRASE")


# 2. mnemonic → seed
seed = Bip39SeedGenerator(mnemonic).Generate()

# 3. seed → HD wallet (Ethereum standard = Polygon compatible)
bip44_ctx = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)

# 4. берём первый адрес (index 0)

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


decimals = int(os.getenv("token_decimals"))
to_block = "latest"


def get_last_incoming_transfer(address, token_address, rpc_url, from_block):
    # address='0x2de1B4F23E40EA0c414334a1D10248726f23D761'
    # token_address='0x912CE59144191C1204E64559FE8253a0e49E6548'
    # decimals = 6

    address = Web3.to_checksum_address(address)

    TOKEN_ADDRESS = Web3.to_checksum_address(
        token_address 
    )
    # приводим адрес пользователя к checksum формату (обязательно для сравнения)
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url)) 
    except Exception as e:
        return {
            "data": None,
            "error": "Failed to connect to the network RPC"
        } 
    
    try:

        TRANSFER_TOPIC = "0x" + w3.keccak(
        text="Transfer(address,address,uint256)"
        ).hex()
        # хэш сигнатуры события Transfer, используется для фильтрации логов ERC20

        logs = w3.eth.get_logs({
            "fromBlock": from_block,  
            "toBlock": to_block,       
            "address": TOKEN_ADDRESS,  # фильтр по контракту токена
            "topics": [
                TRANSFER_TOPIC,  # событие Transfer
                None,             # from (не фильтруем отправителя)
                "0x" + address[2:].lower().rjust(64, "0")
                # to (фильтр: только входящие переводы на наш адрес)
            ]
        })
    except Exception as e:
        return {
            "data": None,
            "error": "Failure to retrieve transactions on the blockchain"
        } #error_logs: add +1
    

    if not logs:
        return {
            "data": None,
            "error": None
        }
    
    last = logs[-1]
    tx_hash = last["transactionHash"].hex()
    value = int(last["data"].hex(), 16)/(10**decimals)
    block = last['blockNumber'] #int

    return {
        "data": {
            "tx_hash": tx_hash,
            "amount": value,
            "block": str(block)
            },
        "error": None
    }
  

subscription_price = float(os.getenv("SUBSCRIPTION_PRICE"))


def check_transfer(chain, user_id):
    chain_data = chains_data.get(chain)
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
    from_block = user_data['last_transfer_data']['block']
    from_block = int(from_block) if from_block else 0 #our db init block for this chain or (latest - (time_to_transfer * avg blocks/time))
    last_tx_hash = user_data['last_transfer_data']['tx_hash']
    new_transfer = get_last_incoming_transfer(user_address, usdt_token_address, rpc_url, from_block)
    data, error = new_transfer.values()

    if error:
        return {
            "transfer_received": None,
            "error": error
        }
    if not data or data['tx_hash'] == last_tx_hash:
        return {
            "transfer_received": False,
            "error": "transfer not found"
        }
    print(f"amount: {data['amount']}")
    if float(data['amount']) < subscription_price:
        return {
            "transfer_received": False,
            "error": "amount less than subscription_price"
        }
    
    last_tx_hash = data["tx_hash"]
    block = data["block"]
    user.addresses_data[chain]['last_transfer_data']['tx_hash'] = last_tx_hash
    user.addresses_data[chain]['last_transfer_data']['block'] = block
    flag_modified(user, "addresses_data")
    user.is_subscribed = True
    db.commit()
    db.close()
    return {
        "transfer_received": True,
        "error": None
    }
    
# print(get_last_incoming_transfer('0x2de1B4F23E40EA0c414334a1D10248726f23D761', 
#                                  '0x912CE59144191C1204E64559FE8253a0e49E6548',
#                                  'https://arb1.arbitrum.io/rpc',

#                                   from_block=465429544,)) # 465429544
