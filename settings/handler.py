from aiogram import types
from aiogram.fsm.context import FSMContext
from .keyboard import user_agreement_keyboard, choose_start_keyboard, choose_action_keyboard
from .state import CreateOrder
from .message_helper import create_consultation, create_order_message
from .db_helper import check_user
from os import environ

async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.delete()
    tg_id = message.from_user.id
    user_name = message.from_user.full_name
    await state.update_data({'name':user_name,'tg_id':tg_id})
    exist_user = await check_user(tg_id)
    if not exist_user:
        user_agreement = types.FSInputFile("user_agreement.pdf")
        await message.answer_document(user_agreement, caption="Пользовательское соглашение", reply_markup=user_agreement_keyboard())
    else:
        await message.answer('Написать нормальное приветсвие', reply_markup=choose_start_keyboard())


async def name_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data({'name':message.text})
    await state.set_state(CreateOrder.choose_address)
    await message.answer('Введите адрес доставки')

async def address_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data({'address':message.text})
    await state.set_state(CreateOrder.choose_phonenumber)
    await message.answer('Введите контактный номер телефона')


async def phone_handler(message: types.Message, state: FSMContext):
    # await message.delete()
    state_name = await state.get_state()
    await state.update_data({'phone':message.text})
    if state_name == 'CreateOrder:choose_phonenumber':
        await create_order_message(message,state)
    else:
        await create_consultation(message,state)


async def pay_handler(message: types.Message, state: FSMContext):
    prices = [types.LabeledPrice(label='Оплата', amount=1000)]
    pay_token = environ['PAYMENT_PROVIDER_TOKEN']
    await message.bot.send_invoice(
        message.chat.id,
        title="Заказ букета",
        description="Выберите способ оплаты.",
        payload="order_id",
        provider_token=pay_token,  
        currency="USD",
        prices=prices,
        start_parameter="time-to-pay",
        is_flexible=False
    )

async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def successful_payment_handler(message: types.Message, state:FSMContext):
    payment_info = message.successful_payment
    await message.answer(
        f"Спасибо бро что отдал свои {payment_info.total_amount / 100} {payment_info.currency}!\n"
        "Ждем еще"
    )
    print(f"Payment payload: {payment_info.invoice_payload}")
    print(f"Telegram payment charge ID: {payment_info.telegram_payment_charge_id}")
    print(f"Provider payment charge ID: {payment_info.provider_payment_charge_id}")


async def create_order_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await state.set_state(CreateOrder.choose_action)
    await message.answer('К какому событию готовимся?', reply_markup= await choose_action_keyboard())

async def create_consultation_handler(message: types.Message, state: FSMContext):
    await state.set_state(CreateOrder.choose_consultation)
    await message.answer(text='Введите контактный номер телефона для связи')
       

    
