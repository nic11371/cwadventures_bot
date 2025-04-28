from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, KeyboardButtonPollType, \
    KeyboardButtonRequestUser, KeyboardButtonRequestChat


def keyboards():
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        KeyboardButton(text="Запросить геолокацию", request_location=True),
        KeyboardButton(text="Запросить контакт", request_contact=True)
    )
    builder.row(KeyboardButton(
        text="Создать викторину",
        request_poll=KeyboardButtonPollType(type="quiz"))
    )
    builder.row(
        KeyboardButton(
            text="Выбрать премиум пользователя",
            request_user=KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        KeyboardButton(
            text="Выбрать супергруппу с форумами",
            request_chat=KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )
    return builder
