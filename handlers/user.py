import keyboards.userkb as kb
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram import F


user = Router()


@user.message(CommandStart())
async def start(message: Message):
    image_url = "https://disk.yandex.ru/i/A-H0qAgBSF5e3Q"
    text = f"<i>Я рад Вас приветствовать в моем канале</i>"
    await message.answer_photo(
        photo=image_url, caption=text, show_caption_above_media=True,
        message_effect_id="5104841245755180586", parse_mode=ParseMode.HTML)
    await message.answer("Какое число больше?", reply_markup=kb.main)


@user.message(Command("place"))
async def send_venue(message: Message):
    await message.answer_venue(
        latitude=55.75482,
        longitude=37.62169,
        title="Красная площадь",
        address="Москва Красная площадь"
    )


@user.message(F.text == '100')
async def hundred(message: Message):
    await message.reply("Неправильно")


@user.message(F.text == '101')
async def hundred_one(message: Message):
    await message.reply("Правильно")


@user.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID: {message.photo[-1].file_id}\n\n'
                        f'Ваше имя: {message.from_user.first_name}\n\n'
                        f'Ваш ID: {message.from_user.id}')


@user.message(F.contact)
async def contact(message: Message):
    contact_name = message.contact.first_name
    contact_phone = message.contact.phone_number
    await message.answer(
        f"Получил контакты юзера:\n\nУ тебя он записан: {contact_name}\nТелефон: {contact_phone}")
