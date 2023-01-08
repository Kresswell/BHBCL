from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def start_button():
    m = InlineKeyboardMarkup(resize_keyboard=True)
    m.insert(InlineKeyboardButton('Start', callback_data='strt'))
    return m


def admin_menu():
    m = InlineKeyboardMarkup(resize_keyboard=True)
    m.insert(InlineKeyboardButton('Рассылка', callback_data='mssndd'))
    m.insert(InlineKeyboardButton('GET SIGNAL', callback_data='gtsgn'))
    return m


def menu():
    m = InlineKeyboardMarkup(resize_keyboard=True)
    m.insert(InlineKeyboardButton('INSTRUCTIONS ⚙', callback_data='instr'))
    m.add(InlineKeyboardButton('GET SIGNAL ✅', callback_data='gtsgn'))
    return m


def get_signal():
    m = InlineKeyboardMarkup(resize_keyboard=True)
    m.insert(InlineKeyboardButton('GET SIGNAL ✅', callback_data='gtsgn'))
    return m


def cancel():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.add(KeyboardButton('Отмена'))
    return m
