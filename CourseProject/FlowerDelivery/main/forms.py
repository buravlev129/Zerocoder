from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Регистрационная форма
    """
    phone = forms.CharField(max_length=60, required=True)
    address = forms.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'address')


class CustomAuthenticationForm(AuthenticationForm):
    """
    Вход с логином и паролем
    """
    error_messages = {
        'invalid_login': "Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.",
        'inactive': "Данный аккаунт заблокирован.",
    }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def clean(self):
        cleaned_data = super().clean()
        # Добавляем несколько глобальных ошибок
        # self.add_error(None, "Первая глобальная ошибка.")
        # self.add_error(None, "Вторая глобальная ошибка.")
        return cleaned_data


