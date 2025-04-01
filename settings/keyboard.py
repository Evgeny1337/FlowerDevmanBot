from aiogram import types
from datetime import datetime
import calendar
from .db_helper import get_actions, get_colors, get_money

def create_time_control_keyboard(hours=0, minutes=0):
    def wrap_time(h, m):
        return h % 24, m % 60

    hours, minutes = wrap_time(hours, minutes)

    keyboard_buttons = [
        [
            types.InlineKeyboardButton(
                text="-", callback_data='time_hour_decrease'),
            types.InlineKeyboardButton(
                text=f"{str(hours).zfill(2)} ч.", callback_data='ignore'),
            types.InlineKeyboardButton(
                text="+", callback_data='time_hour_increase')
        ],
        [
            types.InlineKeyboardButton(
                text="-", callback_data='time_minute_decrease'),
            types.InlineKeyboardButton(
                text=f"{str(minutes).zfill(2)} м.", callback_data='ignore'),
            types.InlineKeyboardButton(
                text="+", callback_data='time_minute_increase')
        ],
        [types.InlineKeyboardButton(
            text='Подтвердить', callback_data='time_choose')],
        [types.InlineKeyboardButton(text="Отмена", callback_data="exit")]
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def create_calendar(year, month):
    keyboard_buttons = [[types.InlineKeyboardButton(
        text='<<', callback_data=f'month_prev_{year}_{month}'),
        types.InlineKeyboardButton(
            text="{} - {}".format(calendar.month_name[month], year), callback_data='ignore'),
        types.InlineKeyboardButton(
            text='>>', callback_data=f'month_next_{year}_{month}')],]

    month_days = calendar.monthcalendar(year, month)
    print("test", year, month)
    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(
                    text=' ', callback_data='ignore'))
            else:
                row.append(types.InlineKeyboardButton(text=str(day),
                           callback_data=f'day_{year}_{month}_{day}'))
        keyboard_buttons += [row]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")]]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def user_agreement_keyboard():
    keyboard_buttons = [
        [types.InlineKeyboardButton(text='Не даю согласие',callback_data='agreement_no')],
        [types.InlineKeyboardButton(text='Даю согласие',callback_data='agreement_yes')],
        ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_action_keyboard():
    keyboard_buttons = []
    actions = await get_actions()
    for action in actions:
        keyboard_buttons.append([types.InlineKeyboardButton(text=action.name, callback_data=f'action_{action.id}')])
    else:
        keyboard_buttons.append([types.InlineKeyboardButton(text='Отмена', callback_data='exit')])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_money_keyboard():
    keyboard_buttons = []
    moneys = await get_money()
    for money in moneys:
        keyboard_buttons.append([types.InlineKeyboardButton(text=f'{money}р', callback_data=f'money_{money}')])
    else:
        keyboard_buttons.append([types.InlineKeyboardButton(text='Отмена', callback_data='exit')])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_color_keyboard():
    keyboard_buttons = []
    colors = await get_colors()
    for color in colors:
        keyboard_buttons.append([types.InlineKeyboardButton(text=color.name, callback_data=f'color_{color.id}')])
    else:
        keyboard_buttons.append([types.InlineKeyboardButton(text='Отмена', callback_data='exit')])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)    

def exit_keyboard():
    keyboard_button = [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_button)

def choose_flower_keyboard(amount, number, name, price, id):
    if amount > 1:
        keyboard_button = [[types.InlineKeyboardButton(text='<=',callback_data='flower_back'),
                            types.InlineKeyboardButton(text=f'{number + 1}/{amount}',callback_data=f'flower_check'),
                            types.InlineKeyboardButton(text='=>',callback_data='flower_forward')],
                            [types.InlineKeyboardButton(text=f'Выбрать {name} за {price}р.',callback_data=f'flower_choose_{id}')],
                            [types.InlineKeyboardButton(text='Заказать консультацию',callback_data='flower_consultation')],
                            [types.InlineKeyboardButton(text='Предложить другие варианты',callback_data='flower_another')],
                            [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]
                        ]
    else:
        keyboard_button = [[types.InlineKeyboardButton(text=f'{number + 1}/{amount}',callback_data=f'flower_check'),],
                            [types.InlineKeyboardButton(text=f'Выбрать {name} за {price}р.',callback_data=f'flower_choose_{id}')],
                            [types.InlineKeyboardButton(text='Закзать консультацию',callback_data='flower_consultation')],
                            [types.InlineKeyboardButton(text='Предложить другие варианты',callback_data='flower_another')],
                            [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]
                        ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_button)

def choose_start_keyboard():
    keyboard_buttons = [
        [types.KeyboardButton(text='Создать заказ')],
        [types.KeyboardButton(text='Запросить консультацию')]
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True, one_time_keyboard=True)

