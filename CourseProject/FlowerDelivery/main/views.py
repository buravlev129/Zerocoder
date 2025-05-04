
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import RegisterForm, CustomAuthenticationForm #, ProductForm, OrderForm, ReviewForm
from .models import UserProfile #, Product, Order, OrderDetail, OrderStatus, OrderReview, ProductRating


def index(request):
    return render(request, template_name="main/index.html")

def about(request):
    return render(request, template_name='main/about.html')


def register(request):
    """
    Регистрация покупателя
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    """
    Логин в систему
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('main')
