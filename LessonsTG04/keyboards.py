from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


keyboard = [
        [KeyboardButton(text='Привет 👋'), KeyboardButton(text='Как дела? 😊')],
        [KeyboardButton(text='Настройки ⚙️')],
        [KeyboardButton(text='Пока ✋🏼')]
    ]


kbd_reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url="https://dzen.ru/news?issue_tld=ru&itemId=464&ysclid=m7nd9633zp36480194")],
    [InlineKeyboardButton(text="Музыка", url="https://www.youtube.com/watch?v=oMd3cpr2cZk&list=RDQMk39cxbSYF6Y&start_radio=1")],
    [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/watch?v=glLZz-8Ud2A&pp=ygUd0YDQtdGG0LXQv9GC0Ysg0YHQsNC70LDRgtC-0LI%3D")],
])



salads_data = {
    'cucumbers': ('Огурцы 👾', ['Салат с огурцами и зеленью 🌿', 'Огуречный салат с луком 🧅']),
    'tomatoes': ('Помидоры 🍅', ['Салат из помидоров 🍃', 'Помидоры с сыром 🧀']),
    'carrots': ('Морковь 🤑', ['Морковный салат с чесноком 🧄', 'Морковь по-корейски 🥢']),
    'peppers': ('Перец 🌶', ['Салат из перца и баклажанов 🍆', 'Перец фаршированный 🍽']),
    'mayonnaise': ('Майонез ☠️', ['Салат Оливье 🥗', 'Салат Цезарь 🍞'])
}


def get_vegetable_name(key):
    name, _ = salads_data[key]
    return name


# Функция для создания клавиатуры первого уровня
def create_vegetable_keyboard():
    builder = InlineKeyboardBuilder()
    for key, (name, _) in salads_data.items():
        builder.button(text=name, callback_data=f"vegetable:{key}")
    builder.adjust(1)
    return builder.as_markup()


# Функция для создания клавиатуры второго уровня
def create_salad_keyboard(key):
    _, salads = salads_data[key]
    builder = InlineKeyboardBuilder()
    for salad in salads:
        builder.button(text=salad, callback_data=f"salad:{salad}")
    builder.button(text="<< Вернуться", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()

