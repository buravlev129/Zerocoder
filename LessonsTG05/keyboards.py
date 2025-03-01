from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


keyboard = [
        [KeyboardButton(text='BTC'), KeyboardButton(text='ETH'), KeyboardButton(text='USDT'), KeyboardButton(text='XRP'), KeyboardButton(text='BNB'), KeyboardButton(text='SOL')],
        [KeyboardButton(text='USDC'), KeyboardButton(text='DOGE'), KeyboardButton(text='ADA'), KeyboardButton(text='TRX'), KeyboardButton(text='TON'), KeyboardButton(text='HEX')],
    ]


kbd_reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


