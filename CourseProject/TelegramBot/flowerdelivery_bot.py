import asyncio
import aiohttp
import datetime
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from aiohttp import ClientConnectorError, ClientError

from config import BOT_TOKEN, NOTIFICATION_CHAT_ID, DJANGO_API_ORDERS_URL, DJANGO_API_REPORTS_URL
import utils



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



@dp.message(CommandStart())
async def start(message: Message):
    bf = """
    Бот помогает обрабатывать заказы, полученные на сайте магазина www.FlowerDelivery.ru
    /start    - Старт приложения
    /orders   - Список заказов за день
    /reports  - Список отчетов
    """
    await message.answer(bf)


@dp.message(Command("chatid"))
async def echo(message: Message):
    print(f"Chat ID: {message.chat.id}")
    await message.answer(f"chat_id={message.chat.id}")


#
# Обработка заказов
#

@dp.message(Command("orders"))
async def orders(message: Message):
    text = ('*Выберите категорию заказов*\n'
    '`*Новые*       - все новые заказы\n`'
    '`*В работе*    - заказы, взятые в работу\n`'
    '`*Доставка*    - заказы, переданные в отдел доставки\n`'
    '`*Выполненные* - выполненные заказы\n`'
    )
    await message.answer(text, reply_markup=utils.get_orders_keyboard(), parse_mode=ParseMode.MARKDOWN_V2)


async def fetch_order_list(status=None):
    headers = {
        #'Authorization': f'Token {DJANGO_AUTH_TOKEN}'
    }

    api_url = f'{DJANGO_API_ORDERS_URL}{status}/'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except ClientConnectorError as e:
        print(f"Connection error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

@dp.callback_query(lambda query: query.data == "new_orders")
async def process_new_orders(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка списка новых заказов...')
    # await query.answer(f"Вы выбрали new_orders!", show_alert=True)

    orders = await fetch_order_list('new')
    if not orders:
        await bot.send_message(query.from_user.id, 'Нет новых заказов')
        return

    text = utils.format_order_list(orders, 'Новые заказы')
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda query: query.data == "in_work_orders")
async def process_inwork_orders(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка списка заказов в обработке...')

    orders = await fetch_order_list('inwork')
    if not orders:
        await bot.send_message(query.from_user.id, 'Нет заказов в обработке')
        return

    text = utils.format_order_list(orders, 'Заказы в обработке')
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda query: query.data == "delivery_orders")
async def process_inwork_orders(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка списка заказов, переданных в доставку...')

    orders = await fetch_order_list('delivery')
    if not orders:
        await bot.send_message(query.from_user.id, 'Нет заказов, переданных в доставку')
        return

    text = utils.format_order_list(orders, 'Заказы, переданные в доставку')
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda query: query.data == "completed_orders")
async def process_inwork_orders(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка списка выполненных заказов...')

    orders = await fetch_order_list('completed')
    if not orders:
        await bot.send_message(query.from_user.id, 'Нет выполненных заказов')
        return

    text = utils.format_order_list(orders, 'Выполненные заказы')
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)


#
# Обработка отчетов
#

@dp.message(Command("reports"))
async def reports(message: Message):
    text = ('*Список доступных отчетов*\n')
    await message.answer(text, reply_markup=utils.get_reports_keyboard(), parse_mode=ParseMode.MARKDOWN_V2)


async def fetch_report_data(report='', filter=None):
    headers = {
        #'Authorization': f'Token {DJANGO_AUTH_TOKEN}'
    }

    api_url = f'{DJANGO_API_REPORTS_URL}' + report+'/' if report else ''
    if filter:
        api_url += filter

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except ClientConnectorError as e:
        print(f"Connection error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


@dp.callback_query(lambda query: query.data == "sales-report")
async def process_sales_report(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка отчета по продажам...')

    filter = utils.prepare_month_filter(datetime.datetime.today())

    report = await fetch_report_data('sales', filter)
    if not report:
        await bot.send_message(query.from_user.id, 'Нет данных для отчета по продажам')
        return
    
    sales = report[0]
    
    text = utils.format_sales_report(sales)
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda query: query.data == "popular-goods-report")
async def process_popular_goods_report(query: CallbackQuery):
    await bot.answer_callback_query(query.id, 'Подготовка отчета по товарам...')

    filter = utils.prepare_month_filter(datetime.datetime.today())

    report = await fetch_report_data('popular-goods', filter)
    if not report:
        await bot.send_message(query.from_user.id, 'Нет данных для отчета по товарам')
        return
    
    text = utils.format_popular_goods_report(report)
    await bot.send_message(query.from_user.id, text, parse_mode=ParseMode.HTML)



@dp.message()
async def any_message(message: Message):
    await message.answer("Нераспознанное сообщение. См. /help для получения списка команд")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

