import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.user import user
from handlers.creator import creator
from handlers.admin import admin

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_routers(user, creator, admin)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Бот включен!")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен!")
