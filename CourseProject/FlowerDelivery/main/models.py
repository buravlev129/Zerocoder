import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import F, Sum
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from io import BytesIO
from PIL import Image



# Таблица пользователей (ID, имя, email, телефон, адрес).
# В django уже есть встроенная система аутентификации (таблицы auth_*)
# Поэтому мы создаем таблицу UserProfile с дополнительными полями соссылкой на auth_user
class UserProfile(models.Model):
    """
    Профайл пользователя (дополнение к таблице auth_user)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=60, verbose_name="Телефон")
    address = models.CharField(max_length=200, verbose_name="Адрес", null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


# Таблица товаров (ID, название, цена, изображение).
class Product(models.Model):
    """
    Товар (букет)
    """
    name = models.CharField(max_length=60, verbose_name="Название")
    price = models.FloatField(verbose_name="Цена")
    image = models.ImageField(upload_to='product_images/', max_length=230, verbose_name="Фотография", blank=True, null=True)
    thumbnail = models.ImageField(upload_to='product_images/', max_length=230, verbose_name="Фотография", blank=True, null=True)
    tags = models.CharField(max_length=300, verbose_name="Теги")

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            width = getattr(settings, 'PRODUCT_THUMBNAIL_WIDTH', 250)
            height = getattr(settings, 'PRODUCT_THUMBNAIL_HEIGHT', 250)
            img.thumbnail((width, height))
            
            original_name = os.path.basename(self.image.name)
            name, ext = os.path.splitext(original_name)
            thumb_name = f"{name}_thumbnail{ext}"
            
            thumb_io = BytesIO()
            img.save(thumb_io, format=img.format)
            
            self.thumbnail.save(
                thumb_name,
                ContentFile(thumb_io.getvalue()),
                save=False
            )
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        if self.thumbnail:
            self.thumbnail.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def average_rating(self):
        ratings = self.ratings.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        return round(ratings, 1) if ratings else 0

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"


#
# Обработка заказов (ID, пользователь, товары, статус, дата заказа).
#
class OrderStatus(models.Model):
    """
    Статус заказа
    """
    name = models.CharField(max_length=50, verbose_name="Статус", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказа"


class Order(models.Model):
    """
    Заказ
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    delivery_address = models.CharField(max_length=250, verbose_name="Адрес доставки")
    phone_number = models.CharField(max_length=100, verbose_name="Телефон")
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, verbose_name="Статус заказа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    
    def __str__(self):
        return f"Заказ #{self.id} от {self.created_at.strftime('%d.%m.%Y')}"
    
    def total_price(self):
        return self.details.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderDetail(models.Model):
    """
    Подробная информация о заказе
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена товара")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    class Meta:
        verbose_name = "Подробная информация о заказе"
        verbose_name_plural = "Подробная информация о заказе"


#
# Поддержка отзывов и рейтингов.
#
class ProductRating(models.Model):
    """
    Оценка продукта
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Оценка от 1 до 5

    class Meta:
        unique_together = ('product', 'user')  # Один пользователь может оставить только одну оценку для продукта
        verbose_name = "Оценка продукта"
        verbose_name_plural = "Оценка продукта"

    def __str__(self):
        return f"{self.product.name} - {self.user.username}: {self.rating}"


class OrderReview(models.Model):
    """
    Отзыв покупателя
    """
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Отзыв")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв к заказу #{self.order.id} от {self.user.username}"

    class Meta:
        verbose_name = "Отзывы покупателя"
        verbose_name_plural = "Отзывы покупателя"


#
# Поддержка аналитики и отчетов
#

class SalesReport(models.Model):
    """
    Отчеты по продажам
    """
    # report_id = models.AutoField(primary_key=True, verbose_name="ID отчета")
    date = models.DateField(verbose_name="Дата отчета")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name="Заказ")

    total_sales = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма продаж")
    profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Прибыль")
    expenses = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Расходы")

    sales_data = models.JSONField(verbose_name="Данные по продажам", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания отчета")

    def __str__(self):
        return f"Отчет #{self.id} за {self.date}"
    
    class Meta:
        verbose_name = "Отчеты по продажам"
        verbose_name_plural = "Отчеты по продажам"
