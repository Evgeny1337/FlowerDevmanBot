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
from settings.handler import (start_handler,name_handler,address_handler,phone_handler,
                              create_order_handler,create_consultation_handler,pre_checkout_handler,successful_payment_handler)
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
    dp.message.register(name_handler, F.text, CreateOrder.choose_name)
    dp.message.register(address_handler, F.text, CreateOrder.choose_address)
    dp.message.register(phone_handler, F.text.regexp(r'^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'),CreateOrder.choose_phonenumber)
    dp.message.register(phone_handler, F.text.regexp(r'^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'),CreateOrder.choose_consultation)
    dp.message.register(create_order_handler, F.text == 'Создать заказ')
    dp.message.register(create_consultation_handler, F.text == 'Запросить консультацию')

    dp.pre_checkout_query.register(pre_checkout_handler)
    dp.message.register(successful_payment_handler,F.successful_payment,CreateOrder.choose_pay)

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