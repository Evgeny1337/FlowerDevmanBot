from aiogram import types
from aiogram.fsm.context import FSMContext
from .keyboard import user_agreement_keyboard
from .state import CreateOrder
from .message_helper import create_consultation, create_order_message

async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.delete()

    #Вывод pdf или текстом пользоватальеское соглашение
    consent_text = "Пользовательское соглашение"
    await message.answer(consent_text,reply_markup=user_agreement_keyboard())


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
    await message.delete()
    state_name = await state.get_state()
    await state.update_data({'phone':message.text})
    if state_name == 'CreateOrder:choose_phonenumber':
        await create_order_message(message,state)
    else:
        await create_consultation(message,state)
        

    
