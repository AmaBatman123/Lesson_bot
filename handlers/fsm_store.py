
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel
from aiogram.types import ReplyKeyboardRemove

class fsm_store(StatesGroup):
    name = State()
    size = State()
    category = State()
    price = State()
    photo = State()

async def start_fsm(message: types.Message):
    await message.answer('Введите название товара: ', reply_markup=cancel)
    await fsm_store.name.set()

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await fsm_store.next()
    await message.answer('Определите размеры товара: ')

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await fsm_store.next()
    await message.answer('Определите категорию товара: ')

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await fsm_store.next()
    await message.answer('Установите цену на товар: ')

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await fsm_store.next()
    await message.answer('Отправьте фото товара: ')

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await state.finish()
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название - {data["name"]} \n'
                                       f'Размеры - {data["size"]} \n'
                                       f'Категория - {data["category"]} \n'
                                       f'Цена - {data["price"]} \n')

async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb_remove = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено', reply_markup=kb_remove)

def reg_handler_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(start_fsm, commands=['store'])
    dp.register_message_handler(load_name, state=fsm_store.name)
    dp.register_message_handler(load_size, state=fsm_store.size)
    dp.register_message_handler(load_category, state=fsm_store.category)
    dp.register_message_handler(load_price, state=fsm_store.price)
    dp.register_message_handler(load_photo, state=fsm_store.photo, content_types=['photo'])