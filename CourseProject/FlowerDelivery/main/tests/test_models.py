from django.contrib.auth.models import User
from django.test import TestCase
from main.models import Product, ProductRating, UserProfile, Order, OrderDetail, OrderStatus, OrderReview


class UserProfileModelTests(TestCase):

    def test_userprofile(self):
        """
        Проверка создания пользователя и профайла
        """
        user1 = User.objects.create_user(username="testuser1", password="password1")
        UserProfile.objects.create(user=user1, address='Кукрыниксы, 2 к1', phone='322-322')

        p = UserProfile.objects.get(user__username='testuser1')
        self.assertEqual(p.phone, '322-322')
        self.assertEqual(p.address, 'Кукрыниксы, 2 к1')


class ProductModelTests(TestCase):

    def test_product_creation(self):
        """
        Проверка создания продукта
        """
        product = Product.objects.create(name='Розы', price=500, tags='розы красные')
        p1 = Product.objects.get(id=product.id)
        self.assertEqual(p1.name, "Розы")
        self.assertEqual(p1.price, 500)
        print('---')

    def test_product_raiting(self):
        """
        Проверка работы рейтинга продукта
        """
        product = Product.objects.create(name='Розы', price=500, tags='розы красные')
        user1 = User.objects.create_user(username="testuser1", password="password1")
        user2 = User.objects.create_user(username="testuser2", password="password2")

        ProductRating.objects.create(product=product, user=user1, rating=2)
        p1 = Product.objects.get(id=product.id)
        self.assertEqual(p1.average_rating(), 2)

        ProductRating.objects.update(product=product, user=user1, rating=3)
        self.assertEqual(p1.average_rating(), 3)

        ProductRating.objects.create(product=product, user=user2, rating=1)
        self.assertEqual(p1.average_rating(), 2)
        print('---')


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

        # Проверяет наличие статусов
        statuses = OrderStatus.objects.all()
        self.assertEqual(len(statuses), 4)
        
        self.status_new = statuses.filter(name="Новый").first()
        self.status_in_progress = statuses.filter(name="В работе").first()

    def test_order_creation(self):
        """
        Тест создания заказа
        """
        order = Order.objects.create(
            user=self.user,
            status=self.status_new,
            delivery_address="ул. Кукрыниксы",
            phone_number="322"
        )

        self.assertEqual(order.status.name, "Новый")
        self.assertEqual(order.delivery_address, "ул. Кукрыниксы")
        self.assertEqual(order.phone_number, "322")

    def test_order_review_creation(self):
        """
        Тест создания отзыва на заказ
        """
        order = Order.objects.create(
            user=self.user,
            status=self.status_new,
            delivery_address="ул. Кукрыниксы",
            phone_number="322"
        )

        OrderReview.objects.create(
            order=order, 
            user=self.user, 
            text='Ок.'
        )

        review = OrderReview.objects.get(order=order, user=self.user)
        self.assertEqual(review.text, "Ок.")


class OrderDetailModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

        self.status_new = OrderStatus.objects.filter(name="Новый").first()
        self.status_in_progress = OrderStatus.objects.filter(name="В работе").first()

        self.product = Product.objects.create(name="Розы", price=500)

        self.order = Order.objects.create(
            user=self.user,
            status=self.status_new,
            delivery_address="ул. Кукрыниксы",
            phone_number="322"
        )

    def test_order_detail_creation(self):
        """
        Проверка добавления продуктов в заказ и работы вычисляемых полей
        """

        detail = OrderDetail.objects.create(order=self.order, product=self.product, quantity=2, price=500)
        self.assertEqual(detail.quantity, 2)
        self.assertEqual(detail.price, 500)
        self.assertEqual(detail.total_price(), 1000)

        self.assertEqual(self.order.total_price(), 1000)

        OrderDetail.objects.create(order=self.order, product=self.product, quantity=2, price=500)
        OrderDetail.objects.create(order=self.order, product=self.product, quantity=1, price=500)
        self.assertEqual(self.order.total_price(), 2500)

