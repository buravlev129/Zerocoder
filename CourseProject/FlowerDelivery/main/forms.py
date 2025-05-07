from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Product, Order


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


class ProductForm(forms.ModelForm):
    """
    Добавление нового продукта (букета)
    """
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'thumbnail', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 100px;',
                }),

            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'id_image'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название',
            'price': 'Цена',
            'image': 'Фотография',
            'thumbnail': 'Миниатюра',
            'tags': 'Список тегов',
        }


class OrderForm(forms.ModelForm):
    """
    Обработка заказа
    """
    class Meta:
        model = Order
        fields = ['delivery_address', 'phone_number']
        widgets = {
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес доставки'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
        }



class ReviewForm(forms.Form):
    """
    Отзыв покупателя
    """
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        label="Отзыв",
        required=True
    )

