from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from decouple import config
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = config("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f'Здравствуй, мой господин {message.from_user.full_name}!')


@dp.message_handler(commands=['quiz'])
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


@dp.callback_query_handler(text="quiz_1_button")
async def quiz_2(call: types.CallbackQuery):
    question = "Назовите аниме-сериал, известный многим советским детям."
    answer = [
        "Евангелион",
        "Сейлор Мун",
        "Приключения пчелки Майи",
        "Винни-Пух и все-все-все"
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="выйди и больше никогда не заходи",
        open_period=15
    )


@dp.message_handler(commands=['mem'])
async def mem(message: types.Message):
    await message.answer_photo(photo=open('/Users/mac/Downloads/361a557a4442607d0bb5-1024x576.jpg', 'rb'))


@dp.message_handler()
async def echo(message: types.Message):
    if message.text:
        if message.text.isdigit():
            await message.answer(int(message.text) ** 2)
        else:
            await message.answer(message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
