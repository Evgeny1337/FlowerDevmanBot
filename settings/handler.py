from aiogram import types
from aiogram.fsm.context import FSMContext
import datetime
from .keyboard import user_agreement_keyboard

async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.delete()

    #Вывод pdf или текстом пользоватальеское соглашение
    consent_text = "Пользовательское соглашение"
    await message.answer(consent_text,reply_markup=user_agreement_keyboard())
