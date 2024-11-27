from dataclasses import field

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import db_main

class edit_products_fsm(StatesGroup):
    for_field = State()
    for_new_field = State()
    for_photo = State()

async def start_send_products(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_all = InlineKeyboardButton('Вывести все товары', callback_data='all_edit')
    btn_one = InlineKeyboardButton('Вывести по одному товару', callback_data='one_edit')
    keyboard.add(btn_all, btn_one)

    await message.answer(text='Выберите как отправить товары', reply_markup=keyboard)

async def send_all_products(callback_query: types.CallbackQuery):
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

            edit_product = InlineKeyboardMarkup(resize_keyboard=True)
            edit_product.add(InlineKeyboardButton('Редактировать',
                                                  callback_data=f'edit_{product["product_id"]}'))

            await callback_query.message.answer_photo(
                photo=product['photo'],
                caption=caption,
                reply_markup=edit_product
            )
    else:
        await callback_query.message.answer(text='В базе нет товаров')

async def edit_product(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = callback_query.data.split('_')[1]

    await state.update_data(product_id=product_id)

    keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    name_btn = InlineKeyboardButton(text='Название', callback_data='field_name')
    category_btn = InlineKeyboardButton(text='Категория', callback_data='field_category')
    price_btn = InlineKeyboardButton(text='Цена', callback_data='field_price')
    size_btn = InlineKeyboardButton(text='Размер', callback_data='field_size')
    photo_btn = InlineKeyboardButton(text='Фото', callback_data='field_photo')
    info_btn = InlineKeyboardButton(text='Инфо о товаре', callback_data='field_info_product')

    keyboard.add(name_btn, category_btn, price_btn, size_btn, photo_btn, info_btn)

    await callback_query.message.answer(text='Выберите поле для редактирования', reply_markup=keyboard)

    await edit_products_fsm.for_field.set()

async def select_field_product(callback_query: types.CallbackQuery, state: FSMContext):

    field_map = {
        "field_name": "name",
        "field_category": "category",
        "field_price": "price",
        "field_size": "size",
        "field_photo": "photo",
        "field_info_product": "info_product",
    }

    field = field_map.get(callback_query.data)

    if not field:
        await callback_query.message.answer('Недопустимое поле')
        return

    await state.update_data(field=field)

    if field == 'photo':
        await callback_query.message.answer('Отправьте новое фото')
        await edit_products_fsm.for_photo.set()
    else:
        await callback_query.message.answer('Отправьте новое значение')
        await edit_products_fsm.for_new_field.set()

async def set_new_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']

    field = user_data['field']

    new_value = message.text

    await db_main.update_product_field(product_id, field, new_value)

    await message.answer(f'{field} Успешно изменено')
    await state.finish()

async def set_new_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']

    photo_id = message.photo[-1].file_id

    await db_main.update_product_field(product_id, 'photo', photo_id)

    await message.answer('Фото заменено')
    await state.finish()


def register_edit_handler(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['edit_product'])
    dp.register_callback_query_handler(send_all_products, Text(equals='all_edit'))
    dp.register_callback_query_handler(edit_product, Text(startswith='edit_'), state='*')
    dp.register_callback_query_handler(select_field_product, Text(startswith='field_'), state=edit_products_fsm.for_field)
    dp.register_message_handler(set_new_value, state=edit_products_fsm.for_new_field)
    dp.register_message_handler(set_new_photo, state=edit_products_fsm.for_photo, content_types=['photo'])

