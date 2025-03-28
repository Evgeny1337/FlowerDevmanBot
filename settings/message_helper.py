from aiogram import types
from aiogram.fsm.context import FSMContext
from .db_helper import  get_byid_flower
from numpy import frombuffer, uint8
from .keyboard import choose_flower_keyboard
from .db_helper import get_ids_admins
import asyncio

async def edit_image_keyboard(callback: types.CallbackQuery, state: FSMContext, text:str):
    state_data = await state.get_data()
    bouquet_ids = state_data['bouquet_list']
    number = state_data['number']
    new_bouquet = await get_byid_flower(bouquet_ids[number])
    new_photo = types.BufferedInputFile(file=frombuffer(new_bouquet.binary_photo,uint8), filename='image')
    await callback.message.edit_media(media=types.InputMediaPhoto(media=new_photo, caption=text),
                                      reply_markup=choose_flower_keyboard(len(bouquet_ids),number,new_bouquet.name,new_bouquet.price,new_bouquet.id)
                                            )
    
async def create_consultation(callback: types.CallbackQuery):
    admins_ids = await get_ids_admins()
    #Исправить
    user_name = callback.message.from_user.full_name
    print("kek",user_name, admins_ids)
    #Добавить запись в бд
    for id in admins_ids:
        print('wtf',id)
        try:
            await callback.bot.send_message(chat_id=id,text=f'Пользователь {user_name} запросил консультацию')
        except:
            pass
        await asyncio.sleep(2)


async def create_order_message(callback: types.CallbackQuery, state: FSMContext):
    pass