from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Розклад')
b2 = KeyboardButton('/Зараз')
b3 = KeyboardButton('/Адміністратор')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1, b2).add(b3)
