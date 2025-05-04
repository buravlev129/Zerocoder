from django.contrib.auth.models import User
from django.db import models


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


