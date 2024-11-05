import asyncio

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
import random

async def game_dice(message: types.Message):

    games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']

    chosen_game = random.choice(games)

    await bot.send_dice(chat_id=message.chat.id, emoji=chosen_game)


async def PVE_game_dice(message: types.Message):

    games_PVE = ['🎯', '🎳', '🎲']

    chosen_PVE_game = random.choice(games_PVE)

    # Бросок бота
    await bot.send_message(chat_id=message.chat.id, text='Бот делает бросок')
    bot_turn = await bot.send_dice(chat_id=message.chat.id, emoji=chosen_PVE_game)
    await asyncio.sleep(3)

    # Бросок игрока
    await bot.send_message(chat_id=message.chat.id, text='Игрок делает бросок')
    player_turn = await bot.send_dice(chat_id=message.chat.id, emoji=chosen_PVE_game)

    # Подсчет очков
    bot_score = bot_turn.dice.value
    player_score = player_turn.dice.value

    await asyncio.sleep(3)
    if bot_score < player_score:
        result_message = 'Игрок победил!'
    elif bot_score > player_score:
        result_message = 'Бот победил!'
    else:
        result_message = 'Ничья'

    await bot.send_message(chat_id=message.chat.id, text=result_message)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(game_dice, commands=['game'])
    dp.register_message_handler(PVE_game_dice, commands=['PVE'])

