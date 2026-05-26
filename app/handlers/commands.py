from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards.keyboards as keyboards
from app.config import SessionLocal
from app.models.models import User
# from keyboards.main import main_keyboard

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    db = SessionLocal()
    user_tg_id = str(message.from_user.id)
    try:
        user = db.query(User).filter_by(telegram_id=user_tg_id).first()
        if not user:
            user = User(telegram_id=user_tg_id)
            db.add(user)
            db.commit()
            db.refresh(user)
        user_id = user.id
    finally:
        db.close()

    await message.answer(
        "To use the bot, you should subscribe",
        reply_markup=keyboards.check_subscription_keyboard(user_id) # callback_data should be <= 64 bytes;
                                                                        
    )



