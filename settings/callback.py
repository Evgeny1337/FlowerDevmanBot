from aiogram import types
from aiogram.fsm.context import FSMContext
import datetime
from .state import CreateOrder
from .keyboard import (choose_action_keyboard, choose_money_keyboard, choose_color_keyboard,
                       choose_flower_keyboard, create_calendar, create_time_control_keyboard,
                       user_agreement_keyboard, choose_start_keyboard)
from .db_helper import get_flowers_id, get_byid_flower, get_another_ids_flowers, create_user
from numpy import frombuffer, uint8
from .message_helper import edit_image_keyboard


async def exit_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await state.set_state(CreateOrder.choose_action) 
    await callback.message.answer('Вы отменили свои действия. Начнем сначала. К какому событию готовимся?', reply_markup= await choose_action_keyboard())

async def user_agreement_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    if data == 'yes':
        state_data = await state.get_data()
        await create_user(state_data['tg_id'], state_data['name'])
        await state.set_state(CreateOrder.choose_action)
        # await callback.message.answer('К какому событию готовимся?', reply_markup= await choose_action_keyboard())
        await callback.message.answer('Написать нормальное приветсвие', reply_markup=choose_start_keyboard())
    if data == 'no':
        user_agreement = types.FSInputFile("user_agreement.pdf")
        await callback.message.answer_document(user_agreement, caption="Для работы с Телеграм-ботом необходимо ваше согласие", reply_markup=user_agreement_keyboard())


async def choose_action_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'action':data})
    await state.set_state(CreateOrder.choose_money)
    await callback.message.answer(text='На какую сумму рассчитываете?',reply_markup= await choose_money_keyboard())

async def choose_money_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'money':data})
    await state.set_state(CreateOrder.choose_color)
    await callback.message.answer(text='Какую цветовую гамму предпочитаете?',reply_markup = await choose_color_keyboard())

async def choose_color_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'color':data})
    state_data = await state.get_data()
    bouquet_ids = await get_flowers_id(state_data['color'], state_data['money'], state_data['action'])
    if not bouquet_ids:
        #Сделать редирект на консульацию
        await callback.message.answer('По вашему запросы в данный момент мы ни чего не можем предложить')
    else:
        print("Проверка списка букетов",bouquet_ids)
        first_bouquet = await get_byid_flower(bouquet_ids[0])
        await state.set_state(CreateOrder.choose_flower)
        await state.update_data({'number':0,'amount':len(bouquet_ids),'bouquet_list':bouquet_ids, 'about':first_bouquet.description})
        await callback.message.answer_photo(photo=types.BufferedInputFile(file=frombuffer(first_bouquet.binary_photo,uint8), filename='image'),
                                            caption='Вот варианты ваших букетов',
                                            reply_markup=choose_flower_keyboard(len(bouquet_ids),0,first_bouquet.name,first_bouquet.price,first_bouquet.id)
                                            )
   

async def choose_flower_callback(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("_")[1]
    state_data = await state.get_data()
    number = state_data['number']
    amount = state_data['amount']
    about = state_data['about']
    bouquet_ids = state_data['bouquet_list']
    if data == 'back':
        if number - 1 < 0:
            number = amount - 1
        else:
            number -= 1
        await state.update_data({'number':number})
        await edit_image_keyboard(callback,state,'Вот варианты ваших букетов')
    if data == 'forward':
        if number + 1 > amount - 1:
            number = 0
        else:
            number += 1
        await state.update_data({'number':number})
        await edit_image_keyboard(callback,state,'Вот варианты ваших букетов')
    if data == 'check':
        await callback.answer(about)
    if data == 'consultation':
        await callback.message.answer(text='Введите контактный номер телефона для связи')
        await state.set_state(CreateOrder.choose_consultation)
        await callback.message.delete()
    if data == 'another':
        another_flowers_ids = await get_another_ids_flowers(bouquet_ids)
        if not another_flowers_ids:
            await edit_image_keyboard(callback,state,'В данный момент все, что есть(')
        else:
            first_bouquet = await get_byid_flower(another_flowers_ids[0])
            await state.update_data({'number':0,'amount':len(another_flowers_ids),'bouquet_list':another_flowers_ids, 'about':first_bouquet.description})
            await callback.message.answer_photo(photo=types.BufferedInputFile(file=frombuffer(first_bouquet.binary_photo,uint8), filename='image'),
                                    caption='Вот другие букеты',
                                    reply_markup=choose_flower_keyboard(len(another_flowers_ids),0,first_bouquet.name,first_bouquet.price,first_bouquet.id)
                                    )
    if data == 'choose':
        await callback.message.delete()
        id_bouquet = callback.data.split("_")[2]
        await state.update_data({'id_bouquet':id_bouquet})
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        await state.set_state(CreateOrder.choose_date)
        await state.update_data({'year': current_year, 'month': current_month})
        await callback.message.answer('Выберите дату доставки', reply_markup=create_calendar(current_year, current_month))


async def swith_month_callback(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("_")[1]
    state_data = await state.get_data()
    current_year = state_data['year']
    current_month = state_data['month']
    if data == 'prev':
        if current_month - 1 <= 0:
            current_year -= 1
            current_month = 12
        else:
            current_month -= 1
    if data == 'next':
        if current_month + 1 > 12:
            current_year += 1
            current_month = 1
        else:
            current_month += 1
    await state.update_data({'year': current_year, 'month': current_month})
    await callback.message.edit_text(text='Выберите к какого числа приготовить ваш букет', reply_markup=create_calendar(current_year, current_month))


async def choose_date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = int(callback.data.split("_")[3])
    await state.update_data({'day': data})
    await state.set_state(CreateOrder.choose_time)
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    await state.update_data({'hours': hour, "minutes": minute})
    await callback.message.answer(text='Выберите время когда хотите забрать букет', reply_markup=create_time_control_keyboard(hour, minute))


async def switch_time_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.split('_')[1] != 'choose':
        data = callback.data.removeprefix("time_")
        time_data = await state.get_data()
        current_hours = time_data['hours']
        current_minutes = time_data['minutes']
        if data == 'hour_decrease':
            if current_hours - 1 < 1:
                current_hours = 23
            else:
                current_hours -= 1
        elif data == 'hour_increase':
            if current_hours + 1 > 23:
                current_hours = 0
            else:
                current_hours += 1
        elif data == 'minute_decrease':
            if current_minutes - 1 < 1:
                current_minutes = 59
            else:
                current_minutes -= 1
        elif data == 'minute_increase':
            if current_minutes + 1 > 59:
                if current_hours + 1 > 23:
                    current_hours = 0
                    current_minutes = 0
                else:
                    current_hours += 1
                    current_minutes = 0
            else:
                current_minutes += 1
        await state.update_data({'hours': current_hours, "minutes": current_minutes})
        await callback.message.edit_text(text='Выберите время когда хотите забрать ваш букет', reply_markup=create_time_control_keyboard(current_hours, current_minutes))
    else:
        await callback.message.delete()
        await state.set_state(CreateOrder.choose_name)
        await callback.message.answer('Введите имя')
