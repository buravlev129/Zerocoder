"""
Функции для отправки сообщений в телеграм
"""
import os
import json
import requests
from io import BytesIO
from django.conf import settings

BOT_TOKEN = getattr(settings, 'BOT_TOKEN', 'XXX')
NOTIFICATION_CHAT_ID = getattr(settings, 'NOTIFICATION_CHAT_ID', '0000')
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', 'media_root')



def format_order_header(order, caption=None):
    lst = [f'<b><u>{caption}</u></b>'] if caption else []
    lst.extend([
        f"<b>Заказ №:</b> {order['order_id']} <b>Статус:</b> {order['status']}",
        f"<b>Имя клиента:</b> {order['username']}",
        f"<b>Телефон:</b> {order['phone']}",
        f"<b>Адрес:</b> {order['address']}",
    ])
    return '\n'.join(lst)

def format_order_details(order):
    details = order['details']
    lst = []
    if details:
        lst.append(f"<pre>")
        lst.append(f"ID       Название                     Цена       Кол-во")
        lst.append(f"{'-' * 56}")
        for dt in details:
            name = f'{dt["name"][:26]}'
            lst.append(f'{dt["product_id"]:<8} {name:<28} {dt["price"]:>10.2f} {dt["quantity"]:>6}')
        lst.append(f"{'-' * 56}")
        lst.append(f'ИТОГО: {order['total_price']:.2f}')
        lst.append(f"</pre>")
    return '\n'.join(lst)


def send_new_order_notification(order):
    """
    Отправляет уведомление о новом заказе через Telegram API

    :param order: Словарь с параметрами заказа
    """

    header = format_order_header(order)
    body = format_order_details(order)
    media = []
    files = {}

    for i, item in enumerate(order['details']):
        image_path = os.path.normpath(os.path.join(MEDIA_ROOT, item['image_path']))
        file_key = None
        if os.path.isfile(image_path):

            with open(image_path, 'rb') as photo:
                photo_bytes = photo.read()
            
            file_key = f'photo_{i}'
            files[file_key] = BytesIO(photo_bytes)

        caption = f'{header}\n{body}' if i == 0 else ""

        dt = {'type': 'photo', 'caption': caption, 'parse_mode': 'HTML'}
        if file_key:
            dt['media'] = f'attach://{file_key}'
        media.append(dt)

    payload = {
        'chat_id': NOTIFICATION_CHAT_ID,
        'media': json.dumps(media),
        'parse_mode': 'HTML',
        #'text': message
    }

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMediaGroup'

    response = requests.post(url, files=files, data=payload)
    if response.status_code != 200:
        print("[new_order] Ошибка при отправке уведомления:", response.text)


def send_order_status_notification(order):
    """
    Отправляет уведомление об изменении статуса заказа через Telegram API

    :param order: Словарь с параметрами заказа
    """
    text = format_order_header(order, 'Изменение статуса заказа')

    payload = {
        'chat_id': NOTIFICATION_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML',
    }

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("[order_status] Ошибка при отправке уведомления:", response.text)

