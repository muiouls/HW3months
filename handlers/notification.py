import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import config
from config import bot


async def time_to_watch(bot: Bot):
    for admin_id in config.ADMINS:
        await bot.send_message(chat_id=admin_id, text="Вышла новая серия клинкааа🤭!!!")


async def set_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Bishkek")

    scheduler.add_job(
        time_to_watch,
        kwargs={"bot": bot},
        trigger=CronTrigger(
            day_of_week=6,
            hour=23,
            minute=0,
            start_date=datetime.datetime.now(),
            end_date='2023-06-19'
        )
    )

    scheduler.start()