from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel, sizes_kb, confirm_kb
from aiogram.types import ReplyKeyboardRemove
from db import db_main

class fsm_store(StatesGroup):
    name = State()
    product_id = State()
    size = State()
    category = State()
    price = State()
    info_products = State()
    collection = State()
    photo = State()

async def start_fsm(message: types.Message):
    await message.answer('Введите название товара: ', reply_markup=cancel)
    await fsm_store.name.set()

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await fsm_store.next()
    await message.answer('Введите артикул товара:', reply_markup=cancel)

async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await fsm_store.next()
    await message.answer('Определите размер товара: ', reply_markup=sizes_kb)

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
        print(f"Saved size: {data['size']}")
    await fsm_store.next()
    await message.answer('Определите категорию товара: ', reply_markup=cancel)

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await fsm_store.next()
    await message.answer('Установите цену на товар: ', reply_markup=cancel)

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await fsm_store.next()
    await message.answer('Укажите дополнительную информацию о товаре: ', reply_markup=cancel)

async def load_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_products'] = message.text

    await fsm_store.next()
    await message.answer('Укажите коллекцию: ', reply_markup=cancel)

async def load_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text

    await fsm_store.next()
    await message.answer('Загрузите фото товара: ', reply_markup=cancel)

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    # await state.finish()
    await message.answer_photo(photo=data['photo'],
                               caption=f'Артикул - {data["product_id"]}'
                                       f'Название - {data["name"]} \n'
                                       f'Размер - {data["size"]} \n'
                                       f'Категория - {data["category"]} \n'
                                       f'Цена - {data["price"]} \n'
                                       f'Доп. информация - {data["info_products"]} \n'
                                       f'Коллекция - {data["collection"]} \n')

    await message.answer('Верны ли данные?', reply_markup=confirm_kb)

async def confirm_fsm(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await message.answer('Данные сохранены.', reply_markup=ReplyKeyboardRemove())
        async with state.proxy() as data:
            await db_main.sql_insert_store(
                name=data['name'],
                product_id=data['product_id'],
                size=data['size'],
                category=data['category'],
                price=data['price'],
                info_product=data['info_products'],
                collection=data['collection'],
                photo=data['photo']
            )
            await db_main.sql_insert_products(
                product_id=data['product_id'],
                category=data['category'],
                info_product=data['info_products'],
            )
            await db_main.sql_insert_collection(
                product_id=data['product_id'],
                collection=data['collection'],
            )
            await state.finish()
    elif message.text == 'Нет':
        await state.finish()
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Введите Да или Нет')
        await state.finish()


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb_remove = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено', reply_markup=kb_remove)


def reg_handler_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(confirm_fsm, Text(equals=['Да', 'Нет']), state="*")
    dp.register_message_handler(start_fsm, commands=['store'])
    dp.register_message_handler(load_name, state=fsm_store.name)
    dp.register_message_handler(load_product_id, state=fsm_store.product_id)
    dp.register_message_handler(load_size, state=fsm_store.size)
    dp.register_message_handler(load_category, state=fsm_store.category)
    dp.register_message_handler(load_price, state=fsm_store.price)
    dp.register_message_handler(load_info, state=fsm_store.info_products)
    dp.register_message_handler(load_collection, state=fsm_store.collection)
    dp.register_message_handler(load_photo, state=fsm_store.photo, content_types=['photo'])
