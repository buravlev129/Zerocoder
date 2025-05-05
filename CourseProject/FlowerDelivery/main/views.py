
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, CustomAuthenticationForm, ProductForm, OrderForm
from .models import UserProfile, Product, Order, OrderDetail, OrderStatus


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
    Логин в приложение
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


@login_required
def custom_logout(request):
    """
    Выход из приложения
    """
    logout(request)
    return redirect('main')


def add_product(request):
    """
    Добавление товаров
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            redirect('main')
    else:
        form = ProductForm()
    return render(request, 'main/add_product.html', {'form': form})


def product_list(request):
    """
    Список букетов и цветов
    """
    products = Product.objects.all().order_by('id')

    # Создаем объект Paginator с 12 карточками на странице (4 колонки * 3 ряда)
    paginator = Paginator(products, 12)

    # Получаем номер текущей страницы из GET-параметра 'page'
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cart_total = 0
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Получаем корзину из сессии или создаем новую
        cart = request.session.get('cart', {})
        product_key = str(product.id)

        # Добавляем товар в корзину
        if product_key in cart:
            cart[product_key]['quantity'] += 1
        else:
            cart[product_key] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': 1
            }

        cart_total = len(cart)

        # Сохраняем корзину в сессию
        request.session['cart'] = cart
        request.session['cart_total'] = cart_total

    return render(request, 'main/product_list.html', {'page_obj': page_obj})


@login_required
def process_order(request):
    """
    Добавление нового заказа
    """
    # Получаем корзину из сессии
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')

    # Получаем товары из корзины
    cart_items = []
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total_price': item['price'] * item['quantity']
            })
        except Product.DoesNotExist:
            continue

    if not cart_items:
        # Если корзина пуста или товары недоступны, перенаправляем на главную
        return redirect('product_list')

    if request.method == 'POST':
        action = request.POST.get('action')  # Определяем действие (confirm или cancel)

        if action == 'cancel':
            # Если нажата кнопка "Отменить заказ"
            request.session['cart'] = {}
            request.session['cart_total'] = 0
            return redirect('product_list')

        elif action == 'confirm':
            # Если нажата кнопка "Оформить заказ"
            form = OrderForm(request.POST)
            if form.is_valid():
                # Создаем новый заказ
                order = form.save(commit=False)
                order.user = request.user
                order.status = OrderStatus.objects.get_or_create(name="Новый")[0]  # Статус "Новый"
                order.save()

                # Добавляем детали заказа
                for product_id, item in cart.items():
                    product = Product.objects.get(id=int(product_id))
                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        price=item['price'],
                        quantity=item['quantity']
                    )

                # Очищаем корзину
                request.session['cart'] = {}
                request.session['cart_total'] = 0

                return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderForm()

    total_cart_price = sum(item['total_price'] for item in cart_items)

    return render(request, 'main/process_order.html', {
        'form': form,
        'cart_items': cart_items,  # Передаем товары корзины в шаблон
        'total_cart_price': total_cart_price
    })


@login_required
def order_confirmation(request, order_id):
    """
    Страница подтверждения заказа
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'main/order_confirmation.html', {'order': order})



