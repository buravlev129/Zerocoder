from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from main.models import Product, Order, OrderDetail, OrderStatus


class OrderProcessIntegrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password", is_staff=True)
        self.status_new = OrderStatus.objects.get(id=1)
        self.product = Product.objects.create(name="Розы", price=500)

        self.order = Order.objects.create(
            user=self.user,
            status=self.status_new,
            delivery_address="ул. Кукрыниксы, 1, к. 2, стр. 2",
            phone_number="322-322-322"
        )

        self.detail = OrderDetail.objects.create(order=self.order, product=self.product, quantity=2, price=500)

        # Авторизуем пользователя
        self.client = Client()
        self.client.login(username="testuser", password="password")


    def test_order_creation(self):
        """
        Проверяем, что заказ создается через форму
        """
        # Добавляем товар в корзину через сессию
        session = self.client.session
        session['cart'] = {str(self.product.id): {'price': 500, 'quantity': 2}}
        session.save()

        url = reverse('process_order')

        # Отправляем POST-запрос для оформления заказа
        response = self.client.post(url, {
            'delivery_address': 'ул. Центральная, д. 1',
            'phone_number': '+79991234567',
            'action': 'confirm'
        })

        # Проверяем, что заказ создан
        self.assertEqual(Order.objects.count(), 2)
        self.assertTrue(Order.objects.filter(phone_number="+79991234567").exists())

        order = Order.objects.filter(phone_number="+79991234567").first()
        self.assertEqual(order.delivery_address, "ул. Центральная, д. 1")
        self.assertEqual(order.details.count(), 1)

        detail = order.details.first()
        self.assertEqual(detail.product, self.product)
        self.assertEqual(detail.quantity, 2)

