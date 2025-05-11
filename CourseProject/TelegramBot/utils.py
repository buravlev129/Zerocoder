from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_orders_keyboard():
    """
    Кнопки для команды меню /orders
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новые", callback_data="new_orders"), 
         InlineKeyboardButton(text="В работе", callback_data="in_work_orders"),
         InlineKeyboardButton(text="Доставка", callback_data="delivery_orders"),
         InlineKeyboardButton(text="Выполненные", callback_data="completed_orders")],
    ])
    return keyboard

