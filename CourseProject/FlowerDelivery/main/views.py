from datetime import datetime
from django.db.models import Sum, Count, F
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductRatingSerializer, OrderSerializer

from .forms import RegisterForm, CustomAuthenticationForm, ProductForm, OrderForm, ReviewForm
from .models import UserProfile, Product, Order, OrderDetail, OrderStatus, OrderReview, ProductRating

import main.telegram as bot



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


@login_required
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

        cart_total = sum([v['quantity'] for v in cart.values()])

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
            data = {}
            if form.is_valid():
                # Создаем новый заказ
                order = form.save(commit=False)
                order.user = request.user
                order.status = OrderStatus.objects.get_or_create(name="Новый")[0]
                order.save()

                data = {'order_id':order.id, 'username':order.user.username, 'phone':order.phone_number, 'address':order.delivery_address, 'status':order.status }
                data['details']=[]

                # Добавляем детали заказа
                for product_id, item in cart.items():
                    product = Product.objects.get(id=int(product_id))
                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    dt = {'product_id':product_id, 'name':product.name, 'price':item['price'], 'quantity':item['quantity'], 'image_path':product.thumbnail.name }
                    data['details'].append(dt)

                data['total_price'] = order.total_price()

                # Очищаем корзину
                request.session['cart'] = {}
                request.session['cart_total'] = 0

                bot.send_new_order_notification(order=data)
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
def repeat_order(request, order_id):
    """
    Страница повтора заказа
    """
    # Получаем старый заказ текущего пользователя
    old_order = get_object_or_404(Order, id=order_id, user=request.user)

    # Получаем или создаем корзину в сессии
    cart = request.session.get('cart', {})

    # Перебираем товары из старого заказа
    for detail in old_order.details.all():
        product = detail.product  # Получаем товар из базы данных
        product_key = str(product.id)

        # Обновляем цену товара из базы данных
        price = float(product.price)

        # Добавляем товар в корзину
        if product_key in cart:
            cart[product_key]['quantity'] += detail.quantity
        else:
            cart[product_key] = {
                'name': product.name,
                'price': price,
                'quantity': detail.quantity
            }

    # Сохраняем обновленную корзину в сессию
    request.session['cart'] = cart
    cart_total = len(cart)
    request.session['cart_total'] = cart_total

    # Перенаправляем пользователя на страницу оформления заказа
    return redirect('process_order')


@login_required
def order_confirmation(request, order_id):
    """
    Страница подтверждения заказа
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'main/order_confirmation.html', {'order': order})


@login_required
def order_history(request):
    """
    История заказов покупателя
    """
    # Получаем все заказы текущего пользователя, отсортированные по дате (самые новые сверху)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/order_history.html', {'orders': orders})


@login_required
def order_details(request, order_id):
    """
    Подробности заказа покупателя
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'repeat':
            # Логика повторения заказа (если уже реализована)
            return redirect('repeat_order', order_id=order.id)

        elif action == 'save_review':
            # Сохранение отзыва
            form = ReviewForm(request.POST)
            if form.is_valid():
                review_text = form.cleaned_data['text']

                OrderReview.objects.update_or_create(
                    order=order,
                    user=request.user,
                    defaults={'text': review_text}
                )

                messages.success(request, "Отзыв успешно сохранен.")
                return redirect('order_details', order_id=order.id)

    # Получаем все возможные статусы для комбобокса
    statuses = OrderStatus.objects.all()

    # Проверяем, есть ли уже отзыв для этого заказа
    review = getattr(order, 'review', None)

    return render(request, 'main/order_details.html', {
        'order': order,
        'statuses': statuses,
        'review': review,
        'review_form': ReviewForm()
    })


@login_required
def order_list(request):
    """
    Список заказов для обработки администратором
    """
    filter_type = request.GET.get('filter', 'working')

    # incomplete_orders = Order.objects.filter(status__in=[1, 2, 3]).order_by('-created_at')
    if filter_type == 'completed':
        orders = Order.objects.filter(status__name='Выполнен').order_by('-created_at')
    else:
        orders = Order.objects.filter(status__name__in=['Новый', 'В работе', 'Доставка']).order_by('-created_at')
    
    return render(request, 'main/order_list.html', {
        'orders': orders,
        'current_filter': filter_type
    })


@login_required
def order_in_work(request, order_id):
    """
    Обработка заказа администратором
    """
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status_id = request.POST.get('status')
        new_status = get_object_or_404(OrderStatus, id=new_status_id)

        order.status = new_status
        order.save()

        messages.success(request, f"Статус заказа № {order.id} успешно изменен на '{new_status.name}'.")
        return redirect('order_list')

    statuses = OrderStatus.objects.all()
    review = getattr(order, 'review', None)

    return render(request, 'main/order_in_work.html', {
        'order': order, 
        'statuses': statuses,
        'review': review
        })


class RateProductView(APIView):
    """
    Обработка рейтинга (оценки) товара
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        rating = request.data.get('rating')

        if not product_id or not rating:
            return Response({'error': 'Необходимо указать product_id и rating'}, status=400)

        try:
            product_rating, created = ProductRating.objects.update_or_create(
                product_id=product_id,
                user=request.user,
                defaults={'rating': rating}
            )
            serializer = ProductRatingSerializer(product_rating)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


@login_required
def report_list(request):
    """
    Страница со списком доступных отчетов
    """
    return render(request, template_name="main/report_list.html")


@login_required
def sales_report(request):
    """
    Отчет по продажам
    """
    # Получаем параметры из GET-запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    grouping = request.GET.get('grouping', 'month')  # По умолчанию группировка по дням

    # Преобразуем даты в объекты datetime
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
    except ValueError:
        return render(request, 'main/sales_report.html', {'error': 'Неверный формат даты'})

    # Фильтруем заказы по периоду
    orders = Order.objects.filter(created_at__date__range=(start_date, end_date)) if start_date and end_date else Order.objects.all()

    # Группируем данные
    if grouping == 'day':
        group_by = 'order__created_at__date'
    elif grouping == 'week':
        group_by = 'order__created_at__week'
    elif grouping == 'month':
        group_by = 'order__created_at__month'
    elif grouping == 'year':
        group_by = 'order__created_at__year'

    # Агрегация данных
    grouped_data = (
        OrderDetail.objects.filter(order__in=orders)
        .values(group_by)
        .annotate(
            total_revenue=Sum(F('price') * F('quantity')),
            total_orders=Count('order', distinct=True),
            total_items=Sum('quantity')
        )
        .order_by(group_by)
    )

    MONTH_NAMES = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь' }
    for item in grouped_data:
        item['month_name'] = MONTH_NAMES[item['order__created_at__month']]    

    # Популярные товары
    top_products = (
        OrderDetail.objects.filter(order__in=orders)
        .values('product__name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:5]
    )

    # Общие метрики
    total_revenue = sum(item['total_revenue'] for item in grouped_data if item['total_revenue'])
    total_orders = sum(item['total_orders'] for item in grouped_data if item['total_orders'])
    average_check = total_revenue / total_orders if total_orders else 0

    return render(request, 'main/sales_report.html', {
        'grouped_data': grouped_data,
        'total_revenue': total_revenue,
        'average_check': average_check,
        'total_orders': total_orders,
        'top_products': top_products,
        'start_date': start_date,
        'end_date': end_date,
        'grouping': grouping,
    })


class NewOrdersList(generics.ListAPIView):
    """
    Обработчик запроса новых заказов
    """
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.filter(status__name='Новый').annotate(username=F('user__username'))
        return queryset

class InworkOrdersList(generics.ListAPIView):
    """
    Обработчик запроса для заказов в обработке
    """
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.filter(status__name='В работе').annotate(username=F('user__username'))
        return queryset

class DeliveryOrdersList(generics.ListAPIView):
    """
    Обработчик запроса для заказов, переданных в доставку
    """
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.filter(status__name='Доставка').annotate(username=F('user__username'))
        return queryset

class CompletedOrdersList(generics.ListAPIView):
    """
    Обработчик запроса выполненных заказов
    """
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.filter(status__name='Выполнен').annotate(username=F('user__username'))
        return queryset


