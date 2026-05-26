from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DB config

DATABASE_URL = "sqlite:///db.db"

# 1. Engine (соединение с БД)
engine = create_engine(
    DATABASE_URL,
    echo=False  # True если хочешь видеть SQL запросы
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

# Base.metadata.create_all(bind=engine)

#
users_deposit_chains = [
    {'EVM': [ # EVM should be first in this list
        'Polygon', 'Arbitrum','OP', 'BNB', 'Base', 'Linea', 'Ethereum' ]}, 
    'Tron'
    ]

chains_data = {

    # if dev wants to add new chain he should know that len of chain should be <= 11 (in EVM chains)
    # because length of callback data in telegram api is limited to 64 bytes.

    'Arbitrum': {'RPC_URL': "https://arb1.arbitrum.io/rpc" ,
                 'USDT_TOKEN_ADDRESS': "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9" # arb 0x912CE59144191C1204E64559FE8253a0e49E6548
                 },
    'Polygon': {'RPC_URL': "https://polygon.drpc.org/" ,
                 'USDT_TOKEN_ADDRESS': "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
                }
}
                


                        




