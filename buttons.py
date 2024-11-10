from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_button = KeyboardButton(text="Отмена")
cancel.add(cancel_button)