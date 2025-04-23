from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='100')],
    [KeyboardButton(text='101')]
],  resize_keyboard=True,
    input_field_placeholder="Напиши что-нибудь интересное"
)
