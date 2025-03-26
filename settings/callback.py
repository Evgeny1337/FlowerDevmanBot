from aiogram import types
from aiogram.fsm.context import FSMContext
import asyncio
import datetime
from .state import CreateOrder
from .keyboard import (choose_action_keyboard, choose_money_keyboard, choose_color_keyboard,
                       choose_flower_keyboard, create_calendar, create_time_control_keyboard)


async def exit_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer('Вы отменили свои действия')

async def user_agreement_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    if data == 'yes':
        await state.set_state(CreateOrder.choose_action)
        await callback.message.answer('К какому событию готовимся?', reply_markup=choose_action_keyboard())
    if data == 'no':
        await callback.message.answer('Вы не дали согласие')


async def choose_action_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'action':data})
    await state.set_state(CreateOrder.choose_money)
    await callback.message.answer(text='На какую сумму рассчитываете?',reply_markup=choose_money_keyboard())

async def choose_money_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'money':data})
    await state.set_state(CreateOrder.choose_color)
    await callback.message.answer(text='Какую цветовую гамму предпочитаете?',reply_markup=choose_color_keyboard())

async def choose_color_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'color':data})
    await state.set_state(CreateOrder.choose_flower)
    #Тут делаю запрос к бд
    # await callback.message.answer_photo
    await callback.message.answer('Вот варианты ващих букетов', reply_markup=choose_flower_keyboard())

async def choose_flower_callback(callback: types.CallbackQuery, state: FSMContext):
    #Переписать полностью логику
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'color':data})
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await state.update_data({"year": current_year, "month": current_month})
    await state.set_state(CreateOrder.choose_date)
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
        await callback.message.answer('Дальше больше')