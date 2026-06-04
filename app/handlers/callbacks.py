import os
import re
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm.attributes import flag_modified
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.models.models import User
from config.config import SessionLocal, chains_data
import app.keyboards.keyboards as keyboards
from app.services.evm_addr_control import generate_evm_address, check_transfer
import app.texts.texts as texts




load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", "config", ".env"))
subsc_price = float(os.getenv("SUBSCRIPTION_PRICE"))
free_aats_quantty = int(os.getenv("free_aats_quantty"))
chkTrsf_attempts_perDay = int(os.getenv("chkTrsf_attempts_perDay"))
class UserInput(StatesGroup):
    aats_crypto_inputs = State()

router = Router()


#===============Returns Back==================


@router.callback_query(F.data.startswith("go_back"))
async def autotrading_handler(callback: CallbackQuery):
    await callback.answer()
    direction = callback.data.split(":")[1]
    # user_id = callback.data.split(":")[2]
    user_tg_id = callback.from_user.id
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=user_tg_id).first() #once
    db.close() 
    if direction == 'main_menu':
        # await callback.message.answer(texts.MAIN_MENU,reply_markup=keyboards.main_keyboard(user.id))
        await callback.message.answer_photo(
        photo=FSInputFile("assets/images/banner.jpg"),
        caption=texts.MAIN_MENU,
        reply_markup=keyboards.main_keyboard(user.id)
    )


#===============Wallet==================         
    

@router.callback_query(F.data.startswith("wallet"))
async def autotrading_handler(callback: CallbackQuery):
    await callback.answer()
    user_tg_id = callback.from_user.id
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=user_tg_id).first()
    db.close()
    if not user.is_subscribed:
        await callback.message.answer(
        texts.WALLET,
        reply_markup=keyboards.wallet_keyboard())
    else:
        pass


#===============Portfolio==================


@router.callback_query(F.data.startswith("portfolio"))
async def autotrading_handler(callback: CallbackQuery):
    await callback.answer()
    user_tg_id = callback.from_user.id
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=user_tg_id).first()
    db.close()
    if not user.is_subscribed:
        await callback.message.answer(
        texts.PORTFOLIO,
        reply_markup=keyboards.go_back_main_menu_keyboard())
    else:
        pass


#===============AutoTrading==================


@router.callback_query(F.data.startswith("autotrading"))
async def autotrading_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = int(callback.data.split(":")[1])
    db = SessionLocal()
    user = db.query(User).filter_by(id=user_id).first()
    db.close()
    user_autrd_strgs = user.autotrading_stgs
    answer = 'No strategies yet'
    if user_autrd_strgs:
        answer = ""
        for strategy in user_autrd_strgs:
            if strategy['market'] == 'crypto':
                answer += f"{user_autrd_strgs.index(strategy) + 1}. {strategy['coin']} · "
                answer += f"{strategy['timeframe']} · {strategy['side']}\n"
                answer += f"├ 💰Amount: {strategy['amount']}\n├ Window: {strategy['time_window']}\n"
                answer += f"├ Range: {strategy['price_range']}\n├ 🔥Pnl: {strategy['pnl']}"
                answer += '\n\n'

    await callback.message.answer(
        f"AutoTrading Strategies({len(user_autrd_strgs)})\n\n" + answer,
        reply_markup=keyboards.autotrading_keyboard(user_id))


@router.callback_query(F.data.startswith("add_autotrading_stg"))
async def add_aats_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = int(callback.data.split(":")[1])
    db = SessionLocal()
    user = db.query(User).filter_by(id=user_id).first()
    if not user.is_subscribed:
        if len(user.autotrading_stgs) < free_aats_quantty:
            await callback.message.answer(
                f"Which category would you like to focus on?",
                reply_markup=keyboards.aats_category_keyboard(user_id))
        else:
             await callback.message.answer(f"You can add only {free_aats_quantty} strategy without subscription")
    else:
        await callback.message.answer(
            f"Which category would you like to focus on?",
            reply_markup=keyboards.aats_category_keyboard(user_id))

             


@router.callback_query(F.data.startswith("aats_category"))
async def aats_category_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = int(callback.data.split(":")[1])
    await callback.message.answer(
        f"Which category would you like to focus on?",
        reply_markup=keyboards.aats_category_keyboard(user_id)) 


@router.callback_query(F.data.startswith("aats_crypto"))
async def aats_crypto_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data
    reply_markup=None
    if data.count(':') == 1:
        text = 'Which asset should the bot autonomously trade?\nPick one'
        reply_markup = keyboards.aats_crypto_coin_keyboard(data)
    elif data.count(':') == 2:
            text = "Which timeframe should the bot autonomously trade?\nPick one"
            reply_markup=keyboards.aats_crypto_timeframe_keyboard(data)
    elif data.count(':') == 3:
            text = "Which direction should the bot purchase?\nPick one"
            reply_markup=keyboards.aats_crypto_side_keyboard(data)
    elif data.count(':') == 4:
            text = """Type amount in USD that the bot should use when it executes\n
Example: 830"""
            await state.set_state(UserInput.aats_crypto_inputs)
            await state.set_data({"past_callback": data,
                                  "amount": None
                                  })
    await callback.message.answer(text, reply_markup=reply_markup)

    
@router.message(UserInput.aats_crypto_inputs)
async def aats_crypto_input(message: Message, state: FSMContext):
    mess = message.text
    state_data = await state.get_data()
    user_id = state_data['past_callback'].split(':')[-1]
    if state_data['amount'] is None:
        try:
            float(mess)
        except ValueError:
            await message.answer("Amount must be digit, try again")
            return
        if float(mess) < 1 or float(mess) > 10**12:
            await message.answer("Amount must be > 1, try again")
            return
        else:
            state_data['amount'] = float(mess[:7])
            state_data['time_window'] = None
            await state.set_data(state_data)
            text = """With how many seconds left in the candle should the bot start looking for an entry?\n
Example: 60; Max: 300"""
            await message.answer(text)
    elif state_data['time_window'] is None:
        if not mess.isdigit() or int(mess) > 300:
            await message.answer("Time window must be integer and < 300, try again")
            return
        else:
            state_data['time_window'] = int(mess)
            state_data['price_range'] = None
            await state.set_data(state_data)
            text = """What price range should trigger the bot for entry?\n
Price in cents (0-100). The bot fires when the chosen side trades inside this range.\n
Example: 90-98"""
            await message.answer(text)

    elif state_data['price_range'] is None:
        pattern = r"^\d{2}-\d{2}$"
        if not bool(re.fullmatch(pattern, mess)) or int(mess[:2]) > int(mess[3:]):
            await message.answer("Range dont match examples, try again")
            return
        else:
            state_data['price_range'] = mess
            # await state.set_data(state_data)
            past_callback, amount, time_window, price_range = state_data.values()
            coin, timeframe, side, user_id = past_callback.split(':')[1:]
            price_range = [int(price_range[:2]), int(price_range[3:])]
            
            db = SessionLocal()
            user = db.query(User).filter_by(id=user_id).first()
            new_strategy = {
                'ID': len(user.autotrading_stgs) + 1,
                'status': 'active', #/on pause
                'market': 'crypto', 
                'coin': coin,
                'timeframe': timeframe,
                'time_window': time_window, #sec
                'price_range': price_range, #cents
                'side': side, #/Down/Both
                'amount': amount, #USD for trading 
                'pnl': 0
            }
            user.autotrading_stgs = user.autotrading_stgs + [new_strategy]
            db.commit()
            db.close()
            await state.clear()
            text = """AutoTrading Strategy Created\n
The watcher will start scanning for entries on the next tick."""
            await message.answer(text, reply_markup=keyboards.aats_crypto_created_keyboard(user_id))
    
#===============check_subscription================


@router.callback_query(F.data.startswith("check_subscription"))
async def check_subscription_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = int(callback.data.split(":")[1])
    db = SessionLocal()
    user = db.query(User).filter_by(id=user_id).first()
    db.close()
    if not user.is_subscribed:
         await callback.message.answer(f"""
        ❗️You are not subscribed! The subscription cost is {subsc_price} USDT per month. 
To subscribe, you need to transfer {subsc_price} USDT to our address in the selected network.
Do you want to subscribe?
        """,
        reply_markup=keyboards.subscribe_keyboard(user_id))
    else:
        await callback.message.answer("You are subscribed! Your subscription expires in 1 month") #go back


@router.callback_query(F.data.startswith("subscribe"))
async def subscribe_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        f"Select network to transfer {subsc_price} USDT", 
        reply_markup=keyboards.select_chain_keyboard()
    )


@router.callback_query(F.data.startswith("select_chain"))
async def select_chain_handler(callback: CallbackQuery):
    await callback.answer()
    chain = callback.data.split(":")[1]
    tg_user_id = callback.from_user.id
    db = SessionLocal()

    user = db.query(User).filter_by(telegram_id=tg_user_id).first()

    if chains_data.get('EVM').get(chain): # all EVM chains
        if not user.addresses_data or not user.addresses_data.get(chain):
            user_address = generate_evm_address(user.id)
            user.addresses_data = user.addresses_data | {chain: {
                    'address': user_address,
                    'last_balance': 0 
                }}
            db.commit()
        
        user_address = user.addresses_data[chain]['address']
        db.close()
        await callback.message.answer(
            f"""<b>Transfer {subsc_price}</b> USDT to\n\n <code>{user_address}</code>\n 
        <b>[ in {chain.upper()} network ]</b> \n\nAnd then click the button below\n
Please transfer <b>No Less</b> than this amount (network fee on you), otherwise we will not be able to confirm your payment
            """,
            reply_markup=keyboards.check_transfer_keyboard(chain, user.id),
            parse_mode="HTML"
            )  
    elif chain == "TRON":
        pass


@router.callback_query(F.data.startswith("checkTrfr")) 
async def check_transfer_handler(callback: CallbackQuery):
    await callback.answer()
    user_tg_id = callback.from_user.id
    chain = callback.data.split(":")[1]
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=user_tg_id).first()
    # db.close()
    spent_date = user.chkTrsf_attempts_spent.get('spent_date')
    if spent_date:
        spent_date = datetime.strptime(spent_date, "%Y-%m-%d %H:%M")
        hours_passed = (datetime.now() - spent_date).total_seconds() / 3600
        if hours_passed >= 0.017:
            user.chkTrsf_attempts_spent['left'] = chkTrsf_attempts_perDay
            user.chkTrsf_attempts_spent['spent_date'] = None
    attempts = user.chkTrsf_attempts_spent.get('left')
    if attempts is None:
        attempts = chkTrsf_attempts_perDay
    if attempts > 0: 
        transer = check_transfer(chain, user.id)
        received, error = transer.values()
        if error: #all troubles
            attempts -= 1
            user.chkTrsf_attempts_spent['left'] = attempts
            if received is None: 
                await callback.message.answer(
                'Sorry, we have some troubles to check your transfer, Try again later'
                )
            else: #user troubles
                if error == 'transfer not found':
                    await callback.message.answer(
                        f"""We cannot find your transfer, make sure you have transferred the tokens\n
Then click the button below (You have {attempts} attempts left today for all networks)
                        """,
                        reply_markup=keyboards.check_transfer_keyboard(chain, user.id)
                    )
             
                elif error == 'amount less than subscription price':
                    await callback.message.answer(
                            """Amount less than subscription price\n
Contact support to resolve this problem""",
                            reply_markup=keyboards.go_back_main_menu_keyboard())
                
        else:
            await callback.message.answer(
                'Thank you, we get your payment! Your subcription expires in 1 month',
                reply_markup=keyboards.go_back_main_menu_keyboard()
                )
            
    else:
        user.chkTrsf_attempts_spent['spent_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        await callback.message.answer(
            'You have reached daily attempts limit, try again tomorrow',
            reply_markup=keyboards.go_back_main_menu_keyboard())
    flag_modified(user, "chkTrsf_attempts_spent")
    db.commit()
    db.close()

    


