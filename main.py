from config import bot, dp
from aiogram import executor, types
from handlers import commands, quiz, game_dice, fsm_store
import logging

commands.register_commands(dp)
quiz.register_handler_quiz(dp)
game_dice.register_handlers(dp)
fsm_store.reg_handler_fsm_store(dp)

chat_id = '372040467'


async def on_startup(dp):
    await bot.send_message(chat_id=chat_id, text='Bot started')

async def on_shutdown(dp):
    await bot.send_message(chat_id=chat_id, text='Bot stopped')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown )