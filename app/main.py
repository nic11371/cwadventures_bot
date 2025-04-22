from aiogram import Bot, Dispatcher, executor, types
from aiorgram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("TOKEN")

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)