import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.client.session.aiohttp import AiohttpSession

from app.models.models import User
from app.config import SessionLocal, Base, engine
import app.keyboards.keyboards as keyboards
from app.handlers.commands import router as commands_router
from app.handlers.callbacks import router as callback_router

Base.metadata.create_all(bind=engine) #maybe earlier


load_dotenv(".env")


TOKEN = os.getenv("BOT_TOKEN")
PROXY = os.getenv("PROXY")


bot = Bot(
    token=TOKEN,
    session=AiohttpSession(proxy=PROXY)
)

dp = Dispatcher()

dp.include_router(callback_router)
dp.include_router(commands_router)



async def main():
    print("Bot is started")
    await dp.start_polling(bot)
    


# if __name__ == "__main__":
asyncio.run(main())
