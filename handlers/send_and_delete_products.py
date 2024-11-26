from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import db_main
from aiogram.types import InputMediaPhoto

async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_all = types.InlineKeyboardButton('Вывести все товары', callback_data='all_delete_hand')
    button_one = types.InlineKeyboardButton('Вывести по одному', callback_data='one_delete_hand')
    keyboard.add(button_all, button_one)

    await message.answer('Выберите как отправить товары:', reply_markup=keyboard)

async def send_all_products(callback_query: types.CallbackQuery):
    print(f"Обработан callback с данными: {callback_query.data}")
    products = await db_main.fetch_all_products()
    if products:
        for product in products:
            caption = ( f'Заполненный товар: \n'
                        f'Артикул - {product["product_id"]} \n'
                        f'Название - {product["name"]} \n'
                        f'Размер - {product["size"]} \n'
                        f'Категория - {product["category"]} \n'
                        f'Цена - {product["price"]} \n'
                        f'Доп. информация - {product["info_product"]} \n'
                        f'Коллекция - {product["collection"]} \n')

            delete_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
            delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
            delete_keyboard.add(delete_button)

            await callback_query.message.answer_photo(
                photo=product['photo'],
                caption=caption,
                reply_markup=delete_keyboard
            )
    else:
        await callback_query.message.answer(text='В базе нет товаров')

async def delete_all_products(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split('_')[1])

    await db_main.delete_products(product_id)

    if callback_query.message.photo:
        new_caption = 'Товар удален из базы'

        photo_404 = open('media/photo_404.png', 'rb')

        await callback_query.message.edit_media(
            InputMediaPhoto(media=photo_404, caption=new_caption)
        )
    else:
        await callback_query.message.edit_text('Товар удален')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['send_delete_products'])
    dp.register_callback_query_handler(send_all_products, Text(equals='all_delete_hand'))
    dp.register_callback_query_handler(delete_all_products, Text(startswith='delete_'))