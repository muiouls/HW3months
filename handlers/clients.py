from aiogram import Dispatcher, types
from config import bot, dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .client_kb import start_markup
from database.bot_db import sql_command_random
import random
from parser.site_parser import parser
from aiogram.types import ParseMode



# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f'Здравствуй, мой господин {message.from_user.full_name}!',
                           reply_markup=start_markup)


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="quiz_1_button")
    markup.add(button_1)

    question = "Каким был первый цветной фильм ужасов?"
    answer = [
        "Проклятие Франкенштейна",
        "Дом дьявола",
        "Тайна музея восковых фигур"
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation="выйди и больше никогда не заходи",
        open_period=15,
        reply_markup=markup
    )


# @dp.message_handler(commands=['mem'])
async def mem(message: types.Message):
    await message.answer_photo(photo=open('/Users/mac/Downloads/361a557a4442607d0bb5-1024x576.jpg', 'rb'))


async def dice_game(message: types.Message):
    dice_bot = await bot.send_dice(message.chat.id)
    dice_user = await bot.send_dice(message.chat.id)
    await message.answer("Сначала кинул кость бот, затем пользователь")
    if dice_bot.dice.value > dice_user.dice.value:
        await message.answer("Бот победил")
    elif dice_bot.dice.value == dice_user.dice.value:
        await message.answer("Ничья")
    else:
        await message.answer("Пользователь победил")


async def get_random_mentor(message: types.Message):
    random_user = await sql_command_random()
    await message.answer(
        f"id: {random_user[1]} \n"
        f"Имя: {random_user[2]} \n"
        f"Направление: {random_user[3]} \n"
        f"Возраст: {random_user[4]} \n"
        f"Группа: {random_user[5]}")


async def get_random_anime(message: types.Message):
    data = parser()
    anime_list = random.sample(data, 5)
    anime_message = "Список случайных 5 аниме весеннего сезона 2023 года:\n"
    for anime in anime_list:
        anime_message += f"*Название: {anime['title']}*\nТип: {anime['type']}\nОписание: {anime['description']}\nСсылка: {anime['url']}\n\n"
    await bot.send_message(chat_id=message.chat.id, text=anime_message, parse_mode=ParseMode.MARKDOWN, reply_markup=start_markup)


def register_handlers_clients(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(mem, commands=['mem'])
    dp.register_message_handler(dice_game, commands=['dice'])
    dp.register_message_handler(get_random_mentor, commands=['get'])
    dp.register_message_handler(get_random_anime, commands=['anime'])

