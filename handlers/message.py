from aiogram import types, Dispatcher

async def message_handler(message: types.Message):
    try:
        number = float(message.text)
        square = number ** 2
        await message.answer(f'{square}')
    except ValueError:
        await message.answer(message.text)

def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(message_handler)