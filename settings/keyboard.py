from aiogram import types
from datetime import datetime
import calendar


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


def choose_action_keyboard():
    #Наполнение из бд
    keyboard_buttons = [
        [types.InlineKeyboardButton(text='свадьба',callback_data='action_1')],
        [types.InlineKeyboardButton(text='в школу', callback_data='action_2')],
        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def choose_money_keyboard():
    keyboard_buttons = [
        [types.InlineKeyboardButton(text='500',callback_data='money_1')],
        [types.InlineKeyboardButton(text='1000', callback_data='money_2')],
        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

def choose_color_keyboard():
    keyboard_buttons = [
        [types.InlineKeyboardButton(text='синий',callback_data='color_1')],
        [types.InlineKeyboardButton(text='зеленый', callback_data='color_2')],
        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)    

def exit_keyboard():
    keyboard_button = [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_button)

def choose_flower_keyboard():
    keyboard_button = [[types.InlineKeyboardButton(text='<=',callback_data='flower_back'),
                        types.InlineKeyboardButton(text='<=',callback_data='flower_choose'),
                        types.InlineKeyboardButton(text='<=',callback_data='flower_forward')],
                        [types.InlineKeyboardButton(text='Закзать консультацию',callback_data='flower_forward')],
                        [types.InlineKeyboardButton(text='Предложить другие варианты',callback_data='flower_forward')],
                        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]
                       ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_button)