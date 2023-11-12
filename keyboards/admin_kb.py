from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Розклад')
b2 = KeyboardButton('/Часи_занять')
b3 = KeyboardButton('/Правити_Розклад')
b4 = KeyboardButton('/Правити_Часи')


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.row(b1, b2).add(b3).add(b4)

