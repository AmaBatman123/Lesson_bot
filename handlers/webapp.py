from idlelib.editor import keynames

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

async def reply_webapp(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)

    geeks_online = KeyboardButton('Geeks Omline', web_app=WebAppInfo(url='https://online.geeks.kg/'))
    youtube = KeyboardButton('YouTube', web_app=WebAppInfo(url='https://www.youtube.com/'))
    oc_kg = KeyboardButton('Oc_kg', web_app=WebAppInfo(url='https://oc.kg/'))
    jutsu = KeyboardButton('jutsu', web_app=WebAppInfo(url='https://jut.su/'))
    netflix = KeyboardButton('NetFlix', web_app=WebAppInfo(url='https://netflix.com/'))
    whats_app = KeyboardButton('whatsapp', web_app=WebAppInfo(url='https://web.whatsapp.com/'))
    tiktok = KeyboardButton('TikTok', web_app=WebAppInfo(url='https://www.tiktok.com/'))

    keyboard.add(geeks_online, youtube, oc_kg, jutsu, netflix, whats_app, tiktok)


    await message.answer(text='WebApp кнопки', reply_markup=keyboard)

async def inline_webapp(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)

    geeks_online = InlineKeyboardButton('Geeks Online', web_app=WebAppInfo(url='https://online.geeks.kg/'))
    youtube = InlineKeyboardButton('YouTube', web_app=WebAppInfo(url='https://www.youtube.com/'))
    oc_kg = InlineKeyboardButton('Oc_kg', web_app=WebAppInfo(url='https://oc.kg/'))
    jutsu = InlineKeyboardButton('jutsu', web_app=WebAppInfo(url='https://jut.su/'))
    netflix = InlineKeyboardButton('NetFlix', web_app=WebAppInfo(url='https://netflix.com/'))
    whats_app = InlineKeyboardButton('whatsapp', web_app=WebAppInfo(url='https://web.whatsapp.com/'))
    tiktok = InlineKeyboardButton('TikTok', web_app=WebAppInfo(url='https://www.tiktok.com/'))

    keyboard.add(geeks_online, youtube, oc_kg, jutsu, netflix, whats_app, tiktok)


    await message.answer(text='WebApp кнопки', reply_markup=keyboard)

def register_webapp(dp: Dispatcher):
    dp.register_message_handler(reply_webapp, commands='webapp_r')
    dp.register_message_handler(inline_webapp, commands='webapp_i')