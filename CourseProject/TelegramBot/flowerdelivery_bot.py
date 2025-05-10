import asyncio
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

from config import BOT_TOKEN, NOTIFICATION_CHAT_ID



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
    await message.answer(bf) #, reply_markup=kbd_reply_markup)


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


# @dp.message(F.text.startswith('order_details!'))
# async def order_detailes(message: Message):
#     nn = len('order_details!')
#     bf = message.text[nn:]
#     try:
#         data = json.loads(bf)
#         text = (
#             f"<b>Новый заказ!</b>\n"
#             f"<b>Заказ №:</b> <code>{data['order_id']}</code>\n"
#             f"<b>Имя клиента:</b> {data['username']}\n"
#             f"<b>Телефон:</b> {data['phone']}\n"
#             f"<b>Адрес:</b> {data['address']}\n"
#             f"Содержимое заказа:\n"
#         )

#         for product in data['details']:
#             text += f" - {product['product_id']} {product['name']} {product['price']} {product['quantity']}\n"
#         text += f"Итого: {data['total_price']:.2f}"

#         await message.answer(text)
#     except json.JSONDecodeError as ex:
#         await message.answer(f'Ошибка: {str(ex)}')


# @dp.message()
# async def order_detailes(message: Message):
#     nn = len('order_details!')
#     bf = message.text[nn:]
#     try:
#         data = json.loads(bf)
#         text = (
#             f"<b>Новый заказ!</b>\n"
#             f"<b>Заказ №:</b> <code>{data['order_id']}</code>\n"
#             f"<b>Имя клиента:</b> {data['username']}\n"
#             f"<b>Телефон:</b> {data['phone']}\n"
#             f"<b>Адрес:</b> {data['address']}\n"
#             f"Содержимое заказа:\n"
#         )

#         for product in data['details']:
#             text += f" - {product['product_id']} {product['name']} {product['price']} {product['quantity']}\n"
#         text += f"Итого: {data['total_price']:.2f}"

#         await message.answer(text)
#     except json.JSONDecodeError as ex:
#         await message.answer(f'Ошибка: {str(ex)}')

@dp.message(Command("process_order"))
async def echo(message: Message):
    await message.answer(f"process_order!")


@dp.message()
async def any_message(message: Message):
    await message.answer("Нераспознанное сообщение. См. /help для получения списка команд")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

