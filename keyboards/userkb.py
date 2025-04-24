from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Menu', callback_data='menu')],
    [InlineKeyboardButton(text='Заказать', callback_data='order')],
    [InlineKeyboardButton(text='Заказать', callback_data='profile')]
],  resize_keyboard=True,
    input_field_placeholder="Напиши что-нибудь"
)
