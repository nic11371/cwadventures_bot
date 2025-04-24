import keyboards.userkb as kb
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable


user = Router()


class Test(StatesGroup):
    address = State()
    comment = State()
    number = State()


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler:
        Callable[[Message, Dict[str, Any]],
        Awaitable[Any]], event: Message, data: Dict[
            str, Any]) -> Any:
                    print(f"Юзер {event.from_user.id} сообщение: {event.text}")
                    result = await handler(event, data)
                    return result


@user.message(CommandStart())
async def start(message: Message, state: FSMContext):
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
    await message.answer(f'Ваш адрес:\
                        {data["address"]}\nВаш комментарий курьеру: \
                        {data["comment"]}\nВаш номер телефона: \
                        {data["number"]}')
    await state.clear()
