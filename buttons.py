from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_button = KeyboardButton(text="Отмена")
cancel.add(cancel_button)

sizes_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
sizes_kb.add(KeyboardButton('S'), KeyboardButton('M'), KeyboardButton('L'), KeyboardButton('XL'), KeyboardButton('2XL'), KeyboardButton('3XL'))
