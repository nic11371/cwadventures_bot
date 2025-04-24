import keyboards.userkb as kb
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode, ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


user = Router()


class Test(StatesGroup):
    address = State()
    comment = State()
    number = State()


@user.message(CommandStart())
async def start(message: Message, state: FSMContext):
    image_url = "https://disk.yandex.ru/i/A-H0qAgBSF5e3Q"
    text = f"<i>Я рад Вас приветствовать в моем канале</i>"
    await message.bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.UPLOAD_PHOTO)
    await message.answer_photo(
        photo=image_url, caption=text, show_caption_above_media=True,
        message_effect_id="5104841245755180586", parse_mode=ParseMode.HTML)
    await message.bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.answer("Ссылки ниже", reply_markup=kb.main)


@user.message(Command("place"))
async def send_venue(message: Message):
    await message.answer_venue(
        latitude=55.75482,
        longitude=37.62169,
        title="Красная площадь",
        address="Москва Красная площадь"
    )


@user.message(Command('test'))
async def progress(message: Message):
    message = await message.answer("Начинаем...")

    for i in range(1, 11):
        await asyncio.sleep(1)
        await message.edit_text(f"Прогресс: {i * 10}%")

    await message.edit_text("Готово")


@user.message(Command('test1'))
async def progress_one(message: Message):
    message = await message.answer("Начинаем...")
    await asyncio.sleep(2)
    await message.edit_text("В процессе...")
    await asyncio.sleep(3)
    await message.edit_text("Готово")


@user.message(Command("images"))
async def upload_photo(message: Message):
    img = FSInputFile("static/1.jpg")
    await message.answer_photo(
        img, captions="С компьютера"
    )


@user.message(Command('about'))
async def upload_file(message: Message):
    file = FSInputFile('static/resume.pdf')
    await message.answer_document(file, caption='Мое резюме')


@user.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID: {message.photo[-1].file_id}\n\n'
                        f'Ваше имя: {message.from_user.first_name}\n\n'
                        f'Ваш ID: {message.from_user.id}')


# @user.message(F.photo)
# async def download_photo(message: Message, bot: Bot):
#     await bot.download(
#         message.photo[-1], destination=f"{message.photo[-1].file_id}.jpg")


@user.message(F.contact)
async def contact(message: Message):
    contact_name = message.contact.first_name
    contact_phone = message.contact.phone_number
    await message.answer(
        f"Получил контакты юзера:\n\nУ тебя он записан: {contact_name}\nТелефон: {contact_phone}")


@user.callback_query(F.data == 'menu')
async def menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Меню для заказа недоступно')


@user.callback_query(F.data == 'order')
async def order(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Оплата пока что не принимается')


@user.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Появится в скором времени')
