import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram import F

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    image_url = "https://disk.yandex.ru/i/A-H0qAgBSF5e3Q"
    text = f"<i>Я рад Вас приветствовать в моем канале</i>"
    await message.answer_photo(
        photo=image_url, caption=text, show_caption_above_media=True,
        message_effect_id="5104841245755180586", parse_mode=ParseMode.HTML)


@dp.message(Command("place"))
async def send_venue(message: Message):
    await message.answer_venue(
        latitude=55.75482,
        longitude=37.62169,
        title="Красная площадь",
        address="Москва Красная площадь"
    )


@dp.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID: {message.photo[-1].file_id}\n\n'
                        f'Ваше имя: {message.from_user.first_name}\n\n'
                        f'Ваш ID: {message.from_user.id}')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Бот включен!")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен!")
