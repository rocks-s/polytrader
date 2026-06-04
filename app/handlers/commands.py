from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
import app.keyboards.keyboards as keyboards
from config.config import SessionLocal
from app.models.models import User
import app.texts.texts as texts

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    db = SessionLocal()
    user_tg_id = message.from_user.id
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

    # await message.answer(
    #     texts.MAIN_MENU,
    #     reply_markup=keyboards.main_keyboard(user_id) # callback_data should be <= 64 bytes;
                                                                        
    # )
    await message.answer_photo(
        photo=FSInputFile("assets/images/banner.jpg"),
        caption=texts.MAIN_MENU,
        reply_markup=keyboards.main_keyboard(user_id)
    )
