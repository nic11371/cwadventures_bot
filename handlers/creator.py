from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

creator = Router()


@creator.message(Command('bye'))
async def end(message: Message):
    await message.answer('Пока')