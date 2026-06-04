import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession


from config.config import Base, engine
from config.proxies import proxies
from app.handlers.commands import router as commands_router
from app.handlers.callbacks import router as callback_router
from app.utils.proxy_checker import get_stable_proxy


Base.metadata.create_all(bind=engine) #maybe earlier


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "config", ".env"))


TOKEN = os.getenv("BOT_TOKEN")
PROXY = asyncio.run(get_stable_proxy(proxies))


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
    


if __name__ == "__main__":
    if PROXY:
        asyncio.run(main())
    else:
        print('None of the proxies are working')
        
