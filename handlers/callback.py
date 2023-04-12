from aiogram import Dispatcher, types
from config import bot, dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# @dp.callback_query_handler(text="quiz_1_button")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_2 = InlineKeyboardButton("NEXT", callback_data="quiz_2_button")
    markup.add(button_2)

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
        open_period=15,
        reply_markup=markup
    )


async def quiz_3(call: types.CallbackQuery):
    question = "В каком аниме-фильме был использован образ русской избушки на курьих ножках?"
    answer = [
        "Ветер крепчает",
        "Ходячий замок",
        "Унесенные призраками"
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="выйди и больше никогда не заходи",
        open_period=15
    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text="quiz_1_button")
    dp.register_callback_query_handler(quiz_3, text="quiz_2_button")
