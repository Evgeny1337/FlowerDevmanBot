from aiogram import types
from aiogram.fsm.context import FSMContext
from .db_helper import  get_byid_flower
from numpy import frombuffer, uint8
from .keyboard import choose_flower_keyboard
from .db_helper import get_ids_admins,save_consultations,save_order
import asyncio
from datetime import datetime

async def edit_image_keyboard(callback: types.CallbackQuery, state: FSMContext, text:str):
    state_data = await state.get_data()
    bouquet_ids = state_data['bouquet_list']
    number = state_data['number']
    new_bouquet = await get_byid_flower(bouquet_ids[number])
    new_photo = types.BufferedInputFile(file=frombuffer(new_bouquet.binary_photo,uint8), filename='image')
    await callback.message.edit_media(media=types.InputMediaPhoto(media=new_photo, caption=text),
                                      reply_markup=choose_flower_keyboard(len(bouquet_ids),number,new_bouquet.name,new_bouquet.price,new_bouquet.id)
                                            )
    
async def create_consultation(message: types.Message, state: FSMContext):
    admins_ids = await get_ids_admins()
    user_name = message.from_user.full_name
    await message.delete()
    for id in admins_ids:
        try:
            await message.bot.send_message(chat_id=id,text=f'Пользователь {user_name} запросил консультацию')
        except:
            pass
        await asyncio.sleep(2)
    else:
        state_data = await state.get_data()
        await save_consultations(phone_number=state_data['phone'])
        await message.answer('Вы оставили заявку на консультацию. В ближайшее время с вами свяжется флорист')


async def create_order_message(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    print("TEST",state_data.keys())
    dt =  datetime(state_data['year'], state_data['month'], state_data['day'], state_data['hours'], state_data['minutes'])
    order = await save_order(bouquet_id=state_data['id_bouquet'],
                       address=state_data['address'],
                       datetime=dt,
                       phone_number=state_data['phone'],
                       )
    await message.answer('Мы приняли заказ, скоро с вами свяжется флорист, для подтверждения заказа')