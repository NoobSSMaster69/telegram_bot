from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Додати_час')
b2 = KeyboardButton('/Вставити_часи')
b3 = KeyboardButton('/Назад')

kb_tt = ReplyKeyboardMarkup(resize_keyboard=True)

kb_tt.add(b1).add(b2).add(b3)
