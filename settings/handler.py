from aiogram import types
from aiogram.fsm.context import FSMContext
from .keyboard import user_agreement_keyboard, choose_start_keyboard, choose_action_keyboard
from .state import CreateOrder
from .message_helper import create_consultation, create_order_message
from .db_helper import check_user

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


async def create_order_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await state.set_state(CreateOrder.choose_action)
    await message.answer('К какому событию готовимся?', reply_markup= await choose_action_keyboard())

async def create_consultation_handler(message: types.Message, state: FSMContext):
    await state.set_state(CreateOrder.choose_consultation)
    await message.answer(text='Введите контактный номер телефона для связи')
       

    
