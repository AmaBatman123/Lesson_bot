from config import bot, dp
from aiogram import executor, types
import logging
from handlers import commands, quiz, game_dice, fsm_store

commands.register_commands(dp)
quiz.register_handler_quiz(dp)
game_dice.register_handlers(dp)
fsm_store.reg_handler_fsm_store(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)