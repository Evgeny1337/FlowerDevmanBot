from aiogram.fsm.state import StatesGroup, State



class CreateOrder(StatesGroup):
    choose_action = State()
    choose_money = State()
    choose_color = State()
    choose_flower = State()
    choose_date = State()
    choose_time = State()
    choose_name = State()
    choose_address = State()
    choose_phonenumber = State()
    choose_consultation = State()
    choose_pay = State()