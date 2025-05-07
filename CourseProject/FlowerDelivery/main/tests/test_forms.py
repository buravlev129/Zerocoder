from django.contrib.auth.models import User
from django.test import TestCase

from main.forms import CustomAuthenticationForm, ReviewForm


class AuthenticationFormTests(TestCase):

    def setUp(self):
        User.objects.create_user(username="testuser_a", password="password", is_active=True)


    def test_login_user(self):
        """
        Проверка входа для пользователя
        """
        form_data = {'username': 'testuser_a', 'password': 'password'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_user_wrongpassword(self):
        """
        Проверка входа для пользователя с неправильным паролем
        """
        form_data = {'username': 'testuser_a', 'password': 'wrongpassword'}
        form = CustomAuthenticationForm(data=form_data)

        self.assertFalse(form.is_valid())

        expected_error_message = "Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова."
        self.assertIn(expected_error_message, form.errors.get('__all__', []))

    def test_login_inactive_user(self):
        """
        Проверка входа для неактивного пользователя
        """
        User.objects.create_user(username="testuser_n", password="password", is_active=False)

        user = User.objects.filter(username='testuser_n').first()
        self.assertFalse(user.is_active)

        form_data = {'username': 'testuser_n', 'password': 'password'}
        form = CustomAuthenticationForm(data=form_data)

        # Форма должна быть невалидной
        self.assertFalse(form.is_valid())
        
        expected_error_message = "Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова."
        self.assertIn(expected_error_message, form.errors.get('__all__', []))


class ReviewFormTest(TestCase):

    def test_valid_form(self):
        """
        Проверка добавления отзывов на форме
        """
        form_data = {'text': 'Отличный букет!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Проверка добавления отзывов (пустое поле)
        """
        form_data = {'text': ''}  # Пустое поле
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

