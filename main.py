from decouple import config
from aiogram import Dispatcher, Bot, executor, types
import logging




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}\n'
                                f'Твой ID - {message.from_user.id}')
    await message.answer('Привет')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)