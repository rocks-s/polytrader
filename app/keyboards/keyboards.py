from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard(user_id):
        return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤖AutoTrading",
                    callback_data=f"autotrading:{user_id}"
                ),
                InlineKeyboardButton(
                    text="🪞CopyTrading (soon)",
                    callback_data=f"none"
                )
                
            ],
            [
                 InlineKeyboardButton(
                    text="📊Portfolio",
                    callback_data=f"portfolio:{user_id}"
                ),
                InlineKeyboardButton(
                    text="💰Wallet",
                    callback_data=f"wallet"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨Check Subscription",
                    callback_data=f"check_subscription:{user_id}"
                ) 
            ]
        ]
    )


#===============Returns Back==================


def go_back_main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠Main Menu",
                    callback_data=f"go_back:main_menu"
                )
            ]
        ]
    )


#===============Wallet==================


def wallet_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄Refresh",
                    callback_data=f"wallet"
                ),
                InlineKeyboardButton(
                    text="🏠Main Menu",
                    callback_data=f"go_back:main_menu"
                ),
                InlineKeyboardButton(
                    text="Withdraw",
                    callback_data=f"none"
                )
            ]
        ]
    )


#===============AutoTrading==================


def autotrading_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="New",
                    callback_data=f"add_autotrading_stg:{user_id}"
                ),
                InlineKeyboardButton(
                    text="Back",
                    callback_data=f"go_back:main_menu"
                ),
            ]
        ]
    ) 


def aats_category_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Crypto",
                    callback_data=f"aats_crypto:{user_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data=f"go_back:main_menu"
                ),
            ]
        ]
    )


def aats_crypto_coin_keyboard(user_data):
    user_id = user_data.split(':')[-1]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="BTC",
                    callback_data=f"{':'.join(user_data.split(':')[:-1] + ['BTC'] + [user_id])}"
                ),
            ],
            # [
            #     InlineKeyboardButton(
            #         text="Back",
            #         callback_data=f"none"
            #     ),
            # ]
        ]
    )


def aats_crypto_timeframe_keyboard(user_data):
    user_id = user_data.split(':')[-1]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="5Min",
                    callback_data=f"{':'.join(user_data.split(':')[:-1] + ['5Min'] + [user_id])}"
                ),
            ],
            # [
            #     InlineKeyboardButton(
            #         text="Back",
            #         callback_data=f"none"
            #     ),
            # ]
        ]
    )


def aats_crypto_side_keyboard(user_data):
    user_id = user_data.split(':')[-1]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Either",
                    callback_data=f"{':'.join(user_data.split(':')[:-1] + ['Either'] + [user_id])}"
                ),
            ],
            # [
            #     InlineKeyboardButton(
            #         text="Back",
            #         callback_data=f"none"
            #     ),
            # ]
        ]
    )


def aats_crypto_created_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="AutoTrades list",
                    callback_data=f"autotrading:{user_id}"
                ),
                InlineKeyboardButton(
                    text="Main Menu",
                    callback_data=f"go_back:main_menu"
                )
            ]
        ]
    )


#===============subscription================


def subscribe_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✨Subscribe",
                    callback_data=f"subscribe:{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Go back",
                    callback_data=f"go_back:main_menu"
                )
            ]
        ]
    )

def select_chain_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Arbitrum",
                    callback_data=f"select_chain:Arbitrum"
                ),
                InlineKeyboardButton(
                    text="BSC (BEP-20)",
                    callback_data=f"select_chain:BSC"
                )

            ],
            [
                InlineKeyboardButton(
                    text="OP",
                    callback_data=f"select_chain:OP"
                ),
                InlineKeyboardButton(
                    text="Ethereum",
                    callback_data=f"select_chain:Ethereum"
                )
            ],
            # [
            #     InlineKeyboardButton(
            #         text="Linea",
            #         callback_data=f"select_chain:Linea"
            #     ),
            #     InlineKeyboardButton(
            #         text="Base",
            #         callback_data=f"select_chain:Base"
            #     )
            # ],
            [
                InlineKeyboardButton(
                    text="🏠Main Menu",
                    callback_data=f"go_back:main_menu"
                )
            ]
        ]
    )

def check_transfer_keyboard(chain, user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="I transferred",
                    callback_data=f"checkTrfr:{chain}:{user_id}"
                )
            ]
        ]
    )
