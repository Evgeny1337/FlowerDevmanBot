import asyncio
import logging
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from os import environ
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import F
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from settings.handler import start_handler
from settings.callback import (user_agreement_callback, choose_action_callback, exit_callback,
                               choose_money_callback, choose_color_callback, choose_flower_callback, 
                               swith_month_callback, switch_time_callback, choose_date_callback)
from settings.state import CreateOrder
load_dotenv()
TOKEN = environ['BOT_TOKEN']
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    dp = Dispatcher()
    dp.message.register(start_handler, CommandStart())

    dp.callback_query.register(exit_callback, F.data == 'exit')
    dp.callback_query.register(user_agreement_callback,F.data.startswith('agreement'))
    dp.callback_query.register(choose_action_callback,F.data.startswith('action'),CreateOrder.choose_action)
    dp.callback_query.register(choose_money_callback,F.data.startswith('money'), CreateOrder.choose_money)
    dp.callback_query.register(choose_color_callback,F.data.startswith('color'), CreateOrder.choose_color)
    dp.callback_query.register(choose_flower_callback,F.data.startswith('flower'), CreateOrder.choose_flower)

    dp.callback_query.register(
        swith_month_callback, F.data.startswith('month_'))

    dp.callback_query.register(
        switch_time_callback, F.data.startswith(
            'time_'), CreateOrder.choose_time
    )

    dp.callback_query.register(
        choose_date_callback, F.data.startswith(
            'day_'), CreateOrder.choose_date
    )

    await dp.start_polling(bot)   

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())