from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=3
)

start_button = KeyboardButton("/start")
quiz_button = KeyboardButton("/quiz")
mem_button = KeyboardButton("/mem")
reg_button = KeyboardButton("/reg")
delete_button = KeyboardButton("/delete")
dice_button = KeyboardButton("/dice")
anime_button = KeyboardButton("/anime")

start_markup.add(start_button, quiz_button, mem_button, reg_button, delete_button, dice_button, anime_button)

cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2
).add(
    KeyboardButton("CANCEL")
)

direction_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2
).add(
    KeyboardButton("BACK"),
    KeyboardButton("FRONT"),
    KeyboardButton("ANDROID"),
    KeyboardButton("IOS"),
    KeyboardButton("CANCEL")
)

submit_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2
).add(
    KeyboardButton("ДА"),
    KeyboardButton("ЗАНОВО"),
    KeyboardButton("CANCEL")
)
