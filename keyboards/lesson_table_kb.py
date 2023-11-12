from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Додати_пару')
b2 = KeyboardButton('/Вставити_пари')
b3 = KeyboardButton('/Назад')
b4 = KeyboardButton('/Наступний_день')

kb_lt = ReplyKeyboardMarkup(resize_keyboard=True)

kb_lt.add(b1).add(b2).row(b4, b3)
