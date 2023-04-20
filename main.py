from aiogram.utils import executor
import logging

from config import dp, bot, ADMINS
from handlers import clients, callback, extra, admin, fsmAdminMentor
from database.bot_db import sql_create
from handlers.client_kb import start_markup


clients.register_handlers_clients(dp)
callback.register_handlers_callback(dp)
fsmAdminMentor.register_handler_fsm(dp)
admin.register_handlers_admin(dp)
# extra.register_handlers_extra(dp)


async def on_startup(dp):
    sql_create()
    await bot.send_message(ADMINS[0], "HI!", reply_markup=start_markup)


async def on_shutdown(dp):
    await bot.send_message(ADMINS[0], "Bye(")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
