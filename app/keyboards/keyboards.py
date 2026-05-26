from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_subscription_keyboard(user_id):
        return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Check Subscription",
                    callback_data=f"check_subscription:{user_id}"
                )
            ]
        ]
    )

def subscribe_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Subscribe",
                    callback_data=f"subscribe:{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Go back",
                    callback_data=f"go back"
                )
            ]
        ]
    )

def select_chain_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Arbitrum",
                    callback_data=f"select_chain:Arbitrum:{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="TRON(trc-20)",
                    callback_data=f"select_chain:TRON:{user_id}"
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
