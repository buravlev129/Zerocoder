import asyncio
import aiohttp
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from config import BOT_TOKEN, NOTIFICATION_CHAT_ID
from utils import get_orders_keyboard



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



@dp.message(CommandStart())
async def start(message: Message):
    bf = """
    Бот помогает обрабатывать заказы, полученные на сайте магазина www.FlowerDelivery.ru
    /start    - Старт приложения
    /orders   - Список заказов за день
    /order=NN - Информация о заказе номер NN
    /reports  - Список отчетов
    """
    await message.answer(bf)


@dp.message(Command("chatid"))
async def echo(message: Message):
    print(f"Chat ID: {message.chat.id}")
    await message.answer(f"chat_id={message.chat.id}")


@dp.message(Command('test'))
async def send_test_notification(message: Message):
    """
    TEST. Отправляет уведомление о новом заказе в Telegram.
    """
    order_details = {
        'order_id': 123,
        'customer_name': 'Иван Иванов',
        'phone': '+79991234567',
        'address': 'ул. Пушкина, д. 10',
        'flowers': '- Розы (5 шт)\n- Тюльпаны (10 шт)'
    }
    message = (
        f"<b>Новый заказ!</b>\n"
        f"Заказ №: {order_details['order_id']}\n"
        f"Имя клиента: {order_details['customer_name']}\n"
        f"Телефон: {order_details['phone']}\n"
        f"Адрес: {order_details['address']}\n"
        f"Цветы:\n{order_details['flowers']}"
    )
    await bot.send_message(chat_id=NOTIFICATION_CHAT_ID, text=message, parse_mode=ParseMode.HTML)



@dp.message(Command("orders"))
async def orders(message: Message):
    text = ('*Выберите категорию заказов*\n'
    '`*Новые*       - все новые заказы\n`'
    '`*В работе*    - заказы, взятые в работу\n`'
    '`*Доставка*    - заказы, переданные в отдел доставки\n`'
    '`*Выполненные* - выполненные заказы\n`'
    )
    await message.answer(text, reply_markup=get_orders_keyboard(), parse_mode=ParseMode.MARKDOWN_V2)



def format_order_header(order):
    lst = [
        f"<b>Заказ №:</b> {order['id']}",
        f"<b>Имя клиента:</b> {order['username']}",
        f"<b>Телефон:</b> {order['phone_number']}",
        f"<b>Адрес:</b> {order['delivery_address']}",
        f"<b>Дата:</b> {order['created_at']}",
    ]
    return '\n'.join(lst)

def format_order_list(orders, header):
    lst = [f'<b>{header}</b>']
    if orders:
        lst.append(f"<pre>")
        lst.append(f"ID     Имя клиента           Телефон       Адрес                       Стоимость")
        lst.append(f"{'-' * 80}")
        for dt in orders:
            name = f'{dt["username"][:20]}'
            address = f'{dt["delivery_address"][:27]}'
            phone = f'{dt["phone_number"][:12]}'
            lst.append(f'{dt["id"]:<6} {name:<21} {phone:<13} {address:<28} {dt['total_price']:<9.2f}')
        lst.append(f"{'-' * 80}")
        lst.append(f"</pre>")
    return '\n'.join(lst)


DJANGO_API_ORDERS_URL = 'http://127.0.0.1:8000/api/orders/'

async def fetch_order_list(status=None):
    headers = {
        #'Authorization': f'Token {DJANGO_AUTH_TOKEN}'
    }

    api_url = f'{DJANGO_API_ORDERS_URL}{status}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            return None


@dp.callback_query(lambda query: query.data == "new_orders")
async def process_new_orders(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка списка новых заказов...')
    # await query.answer(f"Вы выбрали new_orders!", show_alert=True)

    orders = await fetch_order_list('new')
    if not orders:
        await bot.send_message("Нет новых заказов")
        return

    text = format_order_list(orders, 'Новые заказы')
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda query: query.data == "in_work_orders")
async def process_inwork_orders(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка списка заказов в обработке...')

    orders = await fetch_order_list('inwork')
    if not orders:
        await bot.send_message("Нет заказов в обработке")
        return

    text = format_order_list(orders, 'Заказы в обработке')
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda query: query.data == "delivery_orders")
async def process_inwork_orders(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка списка заказов, переданных в доставку...')

    orders = await fetch_order_list('delivery')
    if not orders:
        await bot.send_message("Нет заказов, переданных в доставку")
        return

    text = format_order_list(orders, 'Заказы, переданные в доставку')
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda query: query.data == "completed_orders")
async def process_inwork_orders(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка списка выполненных заказов...')

    orders = await fetch_order_list('completed')
    if not orders:
        await bot.send_message("Нет выполненных заказов")
        return

    text = format_order_list(orders, 'Выполненные заказы')
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)



@dp.message()
async def any_message(message: Message):
    await message.answer("Нераспознанное сообщение. См. /help для получения списка команд")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

