from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMINS
from . import client_kb
from .client_kb import start_markup
from database.bot_db import sql_command_insert


class FSMAdmin(StatesGroup):
    telegram_id = State()
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private' and message.from_user.id in ADMINS:
        await FSMAdmin.telegram_id.set()
        await message.answer(f'Здравствуй, мой господин {message.from_user.full_name}')
        await message.answer('Введите id ментора :', reply_markup=client_kb.cancel_markup)
    elif message.from_user.id not in ADMINS:
        await message.answer('Вы не являетесь админом(')
    else:
        await message.answer('Пиши в личку')


async def load_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Не забывайте, что  id состоит только из цифр')
    else:
        async with state.proxy() as data:
            data['telegram_id'] = message.text
        await FSMAdmin.next()
        await message.answer('Как зовут ментора?')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('Какое у него направление?', reply_markup=client_kb.direction_markup)


async def load_direction(message: types.Message, state: FSMContext):
    if message.text not in ["BACK", "FRONT", "ANDROID", "IOS"]:
        await message.answer("Используй кнопки")
    else:
        async with state.proxy() as data:
            data['direction'] = message.text
        await FSMAdmin.next()
        await message.answer('Сколько лет ментору ?', reply_markup=client_kb.cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пишите только числа')
    elif not 12 < int(message.text) < 60:
        await message.answer('Упс, кажется, возраст не подходит 👉👈')
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer('Напишите из какой группы ментор?')


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
        await message.answer(
            f"id: {data['telegram_id']} \n"
            f"Имя: {data['name']} \n"
            f"Направление: {data['direction']} \n"
            f"Возраст: {data['age']} \n"
            f"Группа: {data['group']}")
        await FSMAdmin.next()
        await message.answer('Проверьте все ли верно?', reply_markup=client_kb.submit_markup)


async def submit_state(message: types.Message, state: FSMContext):
    if message.text == 'ДА':
        await sql_command_insert(state)
        await state.finish()
        await message.answer('Вы успешно зарегистрировали ментора!', reply_markup=start_markup)
    elif message.text == 'ЗАНОВО':
        await FSMAdmin.telegram_id.set()
        await message.answer('Введите id ментора :')


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer('До встречи 😓', reply_markup=start_markup)


def register_handler_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_reg, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_id, state=FSMAdmin.telegram_id)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit_state, state=FSMAdmin.submit)
