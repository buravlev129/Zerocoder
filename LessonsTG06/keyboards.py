from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


keyboard = [
        [KeyboardButton(text='Регистрация'), KeyboardButton(text='Курс валют')], 
        [KeyboardButton(text='Советы по экономии'), KeyboardButton(text='Личные финансы')]
    ]


kbd_reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


