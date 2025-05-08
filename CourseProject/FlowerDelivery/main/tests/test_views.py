from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from main.models import Product, Order, OrderDetail, OrderStatus


class OrderViewsTest(TestCase):
    """
    Проверяем ответы сервера на HTTP-запросы
    """
    
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username="testuser", password="password")
        self.status_new = OrderStatus.objects.get(id=1)

        self.order = Order.objects.create(
            user=self.user,
            status=self.status_new,
            delivery_address="ул. Кукрыниксы, 1",
            phone_number="322"
        )

        self.product1 = Product.objects.create(name="Розы", price=500)
        OrderDetail.objects.create(order=self.order, product=self.product1, quantity=1, price=500)

        self.product2 = Product.objects.create(name="Астры", price=500)
        OrderDetail.objects.create(order=self.order, product=self.product2, quantity=1, price=500)


    def test_anonymous_user_redirected(self):
        """
        Проверка перенаправления анонимного пользователя
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/product_list/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/order_list/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/order_list/')

        response = self.client.get('/order-in-work/1/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/order-in-work/1/')

        for url in 'process_order order_history order_list repeat_order+ order_confirmation+ order_details+ order_in_work+'.split():
            if url.endswith('+'):
                url = url[:-1]
                url = reverse(url, kwargs={'order_id': self.order.id})
            else:
                url = reverse(url)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)


    def test_anonymous_user_sees_login_page(self):
        """
        Проверка использования шаблона login.html при перенаправлении анонимного пользователя
        """
        response = self.client.get('/order_list/', follow=True)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что используется шаблон login.html
        self.assertTemplateUsed(response, 'main/login.html')
        self.assertContains(response, "Вход")


    def test_order_list_view(self):
        """
        Проверка получения страницы order_list
        """
        self.client.login(username="testuser", password="password")

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        url = reverse('order_list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Новый")


    def test_order_details_view(self):
        """
        Проверка отображения заказа на странице
        """
        self.client.login(username="testuser", password="password")

        response = self.client.get(f'/order-in-work/{self.order.id}/')
        self.assertEqual(response.status_code, 200)

        s_total = f'{self.order.total_price():.2f}' # руб.'

        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, f"{s_total}")
