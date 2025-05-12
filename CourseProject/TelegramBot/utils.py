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


def get_reports_keyboard():
    """
    Кнопки для команды меню /reports
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отчет по продажам", callback_data="sales-report")],
         [InlineKeyboardButton(text="Отчет по популярным товарам", callback_data="popular-goods-report")],
         [InlineKeyboardButton(text="Отчет по статусам заказов", callback_data="order-status-report")],
         [InlineKeyboardButton(text="Отчет по источникам заказов", callback_data="order-sources-report")],
         [InlineKeyboardButton(text="Отчет по скидкам и акциям", callback_data="discounts-report")],
    ])
    return keyboard


def format_order_header(order):
    """
    Форматирование заголовка для заказа (HTML)
    """
    lst = [
        f"<b>Заказ №:</b> {order['id']}",
        f"<b>Имя клиента:</b> {order['username']}",
        f"<b>Телефон:</b> {order['phone_number']}",
        f"<b>Адрес:</b> {order['delivery_address']}",
        f"<b>Дата:</b> {order['created_at']}",
    ]
    return '\n'.join(lst)

def format_order_list(orders, header):
    """
    Форматирование данных заказа в виде таблицы (HTML)
    """
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


def format_sales_report(sales):
    """
    Форматирование для отчета по продажам (HTML)
    """
    lst = [
        f"<b>Аналитический отчет по продажам</b>",
        f"<b>За период:</b> {sales['month']}",
        f"<b>Общая выручка:</b> {sales['total_revenue']}",
        f"<b>Средний чек:</b> {sales['average_check']}",
        f"<b>Количество заказов:</b> {sales['total_orders']}",
    ]
    return '\n'.join(lst)

def format_popular_goods_report(goods):
    """
    Форматирование для отчета по популярным товарам (HTML)
    """
    lst = [f"<b>Аналитический отчет - Топ-5 популярных товаров</b>"]
    lst.append(f"<pre>")
    lst.append(f"ID      Наименование                            Кол-во")
    lst.append(f"{'-' * 55}")
    for g in goods:
        name = f'{g['product_name'][:35]}'
        lst.append(f'{g["product_id"]:<8}{name:<36} {g['total_quantity']:>9}')

    lst.append(f"{'-' * 55}")
    lst.append(f"</pre>")
    return '\n'.join(lst)

