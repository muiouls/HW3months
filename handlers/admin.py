from aiogram import Dispatcher, types
from config import bot, ADMINS
import random
from database.bot_db import sql_command_delete, sql_command_all
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def pin(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.answer("Ты не мой господин!")
        elif not message.reply_to_message:
            await message.answer('Команда должна быть ответом на сообщение!')
        else:
            await bot.pin_chat_message(
                message.chat.id,
                message.reply_to_message.message_id
            )
    else:
        await message.answer("Пиши в группе!")


async def game(message: types.Message):
    if message.from_user.id in ADMINS and message.text.startswith('game'):
        emoji_list = ['⚽', '🏀', '🎲', '🎯', '🎳', '🎰']
        r = random.choice(emoji_list)
        await bot.send_dice(message.chat.id, emoji=r)
    else:
        await bot.send_message(message.chat.id, 'Ты не мой господин')


async def delete_data(message: types.Message):
    users = await sql_command_all()
    for user in users:
        await message.answer(
            f"id: {user[1]} \n" \
            f"Имя: {user[2]} \n" \
            f"Направление: {user[3]} \n" \
            f"Возраст: {user[4]} \n" \
            f"Группа: {user[5]}",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"DELETE {user[2]}", callback_data=f"delete {user[1]}")
            )
        )


async def complete_delete(call: types.CallbackQuery):
    user_id = call.data.replace('delete ', '')
    await sql_command_delete(user_id)
    await call.answer(text=f"Удалена запись с id: {user_id}", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!/')
    dp.register_message_handler(delete_data, commands=['delete'])
    dp.register_callback_query_handler(
        complete_delete,
        lambda call: call.data and call.data.startswith("delete ")
    )
    dp.register_message_handler(game)
