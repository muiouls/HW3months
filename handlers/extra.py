from aiogram import Dispatcher, types
from config import bot, dp, ADMINS


# @dp.message_handler()
# async def echo(message: types.Message):
#     if message.text:
#         if message.text.isdigit():
#             await message.answer(int(message.text) ** 2)
#         else:
#             await message.answer(message.text)
#
#
# def register_handlers_extra(dp: Dispatcher):
#     dp.register_message_handler(echo)
