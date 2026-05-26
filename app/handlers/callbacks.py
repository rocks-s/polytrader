import os
from dotenv import load_dotenv
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.models.models import User
from app.config import SessionLocal, users_deposit_chains
import app.keyboards.keyboards as keyboards
from app.services.evm_addr_gen import generate_evm_address, check_transfer


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
subsc_price = float(os.getenv("SUBSCRIPTION_PRICE"))
router = Router()


@router.callback_query(F.data.startswith("check_subscription"))
async def check_subscription_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = int(callback.data.split(":")[1])
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(id=user_id).first()
    finally:
        db.close()
    if not user.is_subscribed:
         await callback.message.answer(f"""
        You are not subscribed! The subscription cost is {subsc_price} USDT per month. 
To subscribe, you need to transfer {subsc_price} USDT to our address in the selected network.
Do you want to subscribe?
        """,
        reply_markup=keyboards.subscribe_keyboard(user_id))
    else:
        await callback.message.answer("You are subscribed! Your subscription expirates in 1 month") #go back


@router.callback_query(F.data.startswith("subscribe"))
async def subscribe_handler(callback: CallbackQuery):
    await callback.answer()
    #subscribe logic
    user_id = int(callback.data.split(":")[1])
    await callback.message.answer(
        f"Select network to transfer", 
        reply_markup=keyboards.select_chain_keyboard(user_id)
    )


@router.callback_query(F.data.startswith("select_chain"))
async def select_chain_handler(callback: CallbackQuery):
    await callback.answer()
    chain = callback.data.split(":")[1]
    user_id = int(callback.data.split(":")[2])
    db = SessionLocal()

    user = db.query(User).filter_by(id=user_id).first()

    if chain in users_deposit_chains[0]['EVM']: # all EVM chains
        if not user.addresses_data or not user.addresses_data.get(chain):
            user_address = generate_evm_address(user_id)
            user.addresses_data = user.addresses_data | {chain: {
                    'address': user_address,
                    'last_transfer_data': {'tx_hash': None, 'block': None} 
                }}
            db.commit()
        
        user_address = user.addresses_data[chain]['address']
        db.close()
        await callback.message.answer(
            f"Transfer {subsc_price} USDT to {user_address} in {chain.upper()} network and then click the button below",
            reply_markup=keyboards.check_transfer_keyboard(chain, user_id)
            )  
    elif chain == "TRON":
        pass


@router.callback_query(F.data.startswith("checkTrfr")) 
async def check_transfer_handler(callback: CallbackQuery):
    await callback.answer()
    chain = callback.data.split(":")[1]
    user_id = callback.data.split(":")[2]
    transer_data = check_transfer(chain, user_id)
    received, error = transer_data.values()
    if received is None:
        await callback.message.answer(
            'We have some troubles to check your transfer, Try again later'
        ) #backend errors | logs += 1
        return
    if error:
        await callback.message.answer(
            error
        ) #user troubles
        return
    await callback.message.answer(
        'Thank you, we get your payment! Your subcription is activated'
        )
    
@router.callback_query(F.data.startswith("go_back:")) 
async def check_transfer_handler(callback: CallbackQuery):
    await callback.answer()
    menu = callback.data.split(":")[1]
    


