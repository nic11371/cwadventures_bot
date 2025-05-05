import os
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from keyboards.userkb import keyboards
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from typing import Callable, Dict, Any, Awaitable
from database.requests import set_user, save_info_user, save_content_user
from static import commands


user = Router()


class Choice(StatesGroup):
    select_amount = State()


class Test(StatesGroup):
    address = State()
    comment = State()
    number = State()


# @user.message(CommandStart())
# async def start(message: Message, bot: Bot):
#     await bot.set_my_commands(commands=commands)
#     await message.answer(
#         "Выберите действие:",
#         reply_markup=keyboards().as_markup(resize_keyboard=True),
#     )

@user.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! Как дела?")


@user.message(Command('order'))
async def start_order(message: Message, state: FSMContext, bot: Bot):
    await set_user(message.from_user.id)
    await state.set_state(Test.address)
    await message.answer('Введите адрес для доставки')


@user.message(Test.address)
async def comment(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Test.comment)
    await message.answer("Введите сообщение для курьера")


@user.message(Test.comment)
async def number(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(Test.number)
    await message.answer("Введите свой номер телефона")


@user.message(Test.number)
async def result(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(text="Номер должен состоять из цифр")
        return
    await state.update_data(number=message.text)
    data = await state.get_data()
    await save_info_user(
        message.from_user.id, data["address"], data["comment"], data["number"])
    await message.answer("Ваша заявка успешно отправлена")
    await state.clear()


@user.message(F.photo)
async def any_content_handler(message: Message):
    tg_id = message.from_user.id
    content_id = message.photo[-1].file_id

    await save_content_user(tg_id=tg_id, content_id=content_id)
    await message.answer("Контент от пользователя сохранен")


# @user.message(F.photo)
# async def download_photo(message: Message):
#     await message.bot.download(
#         message.photo[-1], destination=f"{message.photo[-1].file_id}.jpg")


# @user.message()
# async def download_content(message: Message, bot: Bot):
#     tg_id = message.from_user.id
#     file_id = message.photo[-1].file_id #возможно неправильно. надо проверить
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     my_path = f"files/{file_path}"
#     await bot.download_file(file_path=file_path, destination=my_path)


@user.message(Command('subscribe'))
async def top_up(message:  Message):
    await message.bot.send_invoice(
        message.from_user.id,
        title="Подписка на бота",
        description="Активация подписки на бота на 1 месяц",
        provider_token=(os.getenv('PAYMENTS_PAYMASTER')),
        currency="rub",
        photo_url="https://disk.yandex.ru/i/A-H0qAgBSF5e3Q",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=[
            LabeledPrice(
                label='Подписка на бота (1 месяц)', amount=1000)
        ],
        start_parameter="",
        payload="test-invoice-payload"
    )


@user.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@user.message(F.successful_payment)
async def successful_payment(message: Message):
    payment_info = message.successful_payment
    await message.answer(
        f"Спасибо за оплату, {message.from_user.first_name}! 🎉\n"
        f"Вы успешно активировали подписку на 1 месяц.\n\n"
        f"Детали платежа: {payment_info.total_amount / 100} {payment_info.currency}\n"
        f"Если у вас возникнут вопросы, напишите в поддержку."
    )


@user.message(Command('donate'))
async def top_up(message: Message, state: FSMContext):
    await message.answer("Введите сумму, которую вы хотите пополнить:")
    await state.set_state(Choice.select_amount)


@user.message(Choice.select_amount)
async def donation_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount < 10:
            await message.answer("Минимальная сумма пополнения — 10 рублей. Попробуйте снова.")
            return
        amount_in_cents = amount * 100 

        await message.bot.send_invoice(
            chat_id=message.from_user.id,
            title="Пополнение",
            description=f"Ваше пополнение на сумму {amount} руб.",
            provider_token=os.getenv('PAYMENTS_PAYMASTER'),
            currency="rub",
            prices=[LabeledPrice(label="Пополнение", amount=amount_in_cents)],
            payload="donation"
        )
        await state.clear()

    except ValueError:
        await message.answer("Введите корректное число (целое число больше 10).")