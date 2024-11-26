from config import bot, dp
from aiogram import executor, types
from handlers import commands, quiz, game_dice, fsm_store, message, send_products, webapp, admin_group, send_and_delete_products
import logging
from db import db_main

commands.register_commands(dp)
send_products.register_list_handler(dp)
quiz.register_handler_quiz(dp)
game_dice.register_handlers(dp)
webapp.register_webapp(dp)
send_and_delete_products.register_handlers(dp)
fsm_store.reg_handler_fsm_store(dp)

admin_group.register_admin_handler(dp)
message.register_message_handler(dp)

chat_id = '372040467'


async def on_startup(dp):
    await bot.send_message(chat_id=chat_id, text='Bot started')

    await db_main.sql_create()

async def on_shutdown(dp):
    await bot.send_message(chat_id=chat_id, text='Bot stopped')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown )