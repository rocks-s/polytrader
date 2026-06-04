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
users_deposit_chains = [ #names
    {'EVM': [ # EVM should be first in this list
        'Polygon', 'Arbitrum','OP', 'BNB', 'Base', 'Linea', 'Ethereum' ]}, 
    'Tron'
    ]

chains_data = {

    # if dev wants to add new chain he should know that len of chain should be <= 11 (in EVM chains)
    # because length of callback data in telegram api is limited to 64 bytes.
    'EVM': {
        'Arbitrum': {'RPC_URL': "https://arb1.arbitrum.io/rpc" ,
                    'USDT_TOKEN_ADDRESS': "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9" # arb 0x912CE59144191C1204E64559FE8253a0e49E6548 
                    },
        # 'Polygon': {'RPC_URL': "https://polygon.drpc.org/" ,
        #             'USDT_TOKEN_ADDRESS': "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
                    # },
        'OP': {'RPC_URL': "https://optimism-rpc.publicnode.com" ,
                    'USDT_TOKEN_ADDRESS': "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"
                    },
        'BSC': {'RPC_URL': "https://bsc-rpc.publicnode.com" ,
                    'USDT_TOKEN_ADDRESS': "0x55d398326f99059ff775485246999027b3197955"
                    },
        'Ethereum': {'RPC_URL': "https://ethereum-rpc.publicnode.com" , 
                    'USDT_TOKEN_ADDRESS': "0xdAC17F958D2ee523a2206206994597C13D831ec7"
                    },
        # 'Linea': {'RPC_URL': "https://linea-rpc.publicnode.com" ,
        #             'USDT_TOKEN_ADDRESS': "0xA219439258ca9da29E9Cc4cE5596924745e12B93"
        #             },
        # 'Base': {'RPC_URL': "https://base-rpc.publicnode.com" ,
        #             'USDT_TOKEN_ADDRESS': "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2"
        #             },
    }

}

#later maybe add user own wallet seed phrase or 1 user 1 account/wallet
deposit_addresses = { # polymarket all deposits account login: adm.devall@gmail.com

}
                


                        




