from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot

async def quiz_1(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    button = InlineKeyboardButton('Далее', callback_data='quiz_2')

    keyboard.add(button)

    question = 'Where are you from?'

    answer = ['Bishkek', 'Moskow', 'Tokyo', 'Gorod']

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation='Вы живете не в этом городе',
        open_period=60,
        reply_markup=keyboard
    )

async def quiz_2(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    button = InlineKeyboardButton('Следущее', callback_data='quiz_2')

    keyboard.add(button)

    question = 'Choose the country'

    answer = ['КР', 'РФ', 'КНР', 'КЗ']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='Да ну?',
        open_period=60,
        reply_markup=keyboard
    )

def register_handler_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='quiz_2')
