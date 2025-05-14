from django.core.management.base import BaseCommand
from main.models import Order, OrderDetail, SalesReport
import datetime
from decimal import Decimal
import json


    

class Command(BaseCommand):
    """
    Команда для генерации отчета по продажам
    """

    help = 'Генерация отчета по продажам'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='Дата для генерации отчета')
        #parser.add_argument('--verbose', action='store_true', help='Вывести подробную информацию')

    def handle(self, *args, **options):

        dt = self.get_report_date(options['date'])
        if not dt:
            return

        self.stdout.write(f'Формирование отчета на дату: {dt:%d.%m.%Y}')

        orders = Order.objects.filter(created_at__date=dt)

        for order in orders:
            # Считаем общую сумму продаж
            total_sales = sum(
                detail.price * detail.quantity for detail in order.details.all()
            )

            # Считаем расходы 1/3 от стоимости заказа
            expenses = total_sales / Decimal(3.33)

            # Считаем прибыль
            profit = total_sales - expenses

            # Формируем данные по продажам
            sales_data = [
                {
                    "product_name": detail.product.name,
                    "quantity": detail.quantity,
                    "price": float(detail.price) * detail.quantity,
                }
                for detail in order.details.all()
            ]

            try:
                existing_report = SalesReport.objects.get(order=order)
                existing_report.delete()
            except SalesReport.DoesNotExist:
                pass

            # Создаем запись в таблице SalesReport
            SalesReport.objects.create(
                date=order.created_at.date(),
                order=order,
                total_sales=total_sales,
                profit=profit,
                expenses=expenses,
                sales_data=json.dumps(sales_data),
            )

        nn = len(orders)
        if nn:
            self.stdout.write(self.style.SUCCESS(f'Обработано заказов: {nn}'))
            self.stdout.write(self.style.SUCCESS('Отчет успешно создан'))
        else:
            self.stdout.write(self.style.SUCCESS('Нет заказав на указанную дату'))


    def get_report_date(self, s_dt):
        if not s_dt:
            return datetime.datetime.today()
        return self.parse_date(s_dt, '%Y-%m-%d')

    def parse_date(self, s_dt, format):
        try:
            dt = datetime.datetime.strptime(s_dt, format)
            return dt
        except:
            self.stdout.write(self.style.ERROR(f'Ошибка в формате даты {s_dt}'))
        return None

