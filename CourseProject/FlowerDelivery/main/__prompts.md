
У меня есть такая модель django для Обработки заказов.

Order - таблица заказов
OrderStatus - статус заказа: Новый, В работе, Доставка, Выполнен

```python
class OrderStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name="Статус")
    ...

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    delivery_address = models.CharField(max_length=250, verbose_name="Адрес доставки")
    phone_number = models.CharField(max_length=100, verbose_name="Телефон")
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, verbose_name="Статус заказа")
    ...
```

Все заказы, полученные от покупателей выводятся сотруднику магазина на странице order_list.html
```html
{% extends "main/layout.html" %}
{% load static %}

{% block content %}
<div class="container mt-5">
    {% if orders %}
        <table class="table table-bordered">
            <tbody>
                {% for order in orders %}
                <tr>
                    <td>{{ order.id }}</td>
                    <td>{{ order.created_at }}</td>
                    <td>{{ order.status.name }}</td>
                    <td>{{ order.user.username }}</td>
                    <td>{{ order.delivery_address }}</td>
                    <td>{{ order.phone_number }}</td>
                    <td>
                        <a href="{% url 'order_in_work' order.id %}" class="btn btn-sm btn-primary">Подробности</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Нет заказов для обработки.</p>
    {% endif %}
</div>
{% endblock %}
```

Для этого используется такое представление:
```python
@login_required
def order_list(request):
    incomplete_orders = Order.objects.filter(status__in=[1, 2, 3]).order_by('-created_at')
    return render(request, 'main/order_list.html', {'orders': incomplete_orders})
```

Мне нужно на странице order_list.html добавить комбобокс для фильтрации списка заказов:
В комбобоксе должны быть два варианта выбора:
- Рабочие заказы
- Выполненные заказы

Рабочие заказы - это заказы со статусом "Новый", "В работе" и "Доставка".
Выполненные заказы - это заказы со статусом "Выполнен" - такой список нужен сотруднику магазина, чтобы посмотреть отзывы по выполненным заказам.
Когда сотрудник магазина выбирает опцию из комбобокса, нужно сразу же обновлять список заказов на странице.

Можно ли сделать этот функционал без использования AJAX? 
Можно просто получать значение из комбобокса и перезагружать всю страницу.




####################################################

вот моя html страница с комбобоксом.
```html
{% extends "main/layout.html" %}
{% load static %}

{% block content %}
<div class="container mt-5">
    <h3>Обработка заказов</h3>

    <!-- Комбобокс для фильтрации -->
    <div class="mb-3">
        <label for="orderFilter" class="form-label">Фильтр заказов:</label>
        <select id="orderFilter" class="form-select">
            <option value="incomplete">Рабочие заказы</option>
            <option value="complete">Выполненные</option>
        </select>
    </div>
    ...

</div>
{% endblock %}
```

Эта страница использует шаблоны django и наследуется от страницы layout.html

Я добавил проверочный скрипт в файл layout.html

```html
{% load static %}

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    <link href="{% static 'main/css/main.css' %}" rel="stylesheet">
    <script src="{% static 'main/js/layout.js' %}"></script>
    <script>
        $(document).on('change', '#orderFilter', function () {
            console.log("Событие change сработало!");
            const filterType = $(this).val();
            console.log("Выбран фильтр:", filterType);
        });
    </script>    
</head>
<body>
{% include 'main/menu.html' %}

<main class="main-content container mt-4">
    {% block content %}
    {% endblock %}    
</main>

{% include 'main/footer.html' %}
</body>
</html>
```

вот сам скрипт:
```javascript
    <script>
        $(document).on('change', '#orderFilter', function () {
            console.log("Событие change сработало!");
            const filterType = $(this).val();
            console.log("Выбран фильтр:", filterType);
        });
    </script>    
```

Но скрипт не срабатывает.
В консоли браузера никаких сообщений нет

#########################################################################

Я нашел причину, почему мой скрипт на срабатывал.
Изначально я добавил это объявление в конец блока <body>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
В этом случае мой AJAX скрипт не срабатывал

Псле того, как я перенес вот это объявление 
```html
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
```

в блок <head>, скрипт заработал.
Вопрос:
Почему так?
Мы же можем добавлять объявление скриптов javascript в конец блока <body>.
Почему это в данном случае не работает?


#########################################################################

вот это скрипт сейчас вызывает ошибку:
```javascript
    <script>
        $(document).ready(function () {
            $('#orderFilter').change(function () {
                const filterType = $(this).val();  // Получаем выбранное значение
    
                $.ajax({
                    url: "{% url 'filter_orders' %}",  // URL для фильтрации
                    type: "GET",
                    data: { filter_type: filterType },  // Передаем тип фильтра
                    success: function (response) {
                        const orders = JSON.parse(response);  // Парсим JSON-ответ
                        let tableBody = $('#orderTable tbody');
                        tableBody.empty();  // Очищаем текущую таблицу
    
                        if (orders.length === 0) {
                            tableBody.append('<tr><td colspan="7">Нет заказов для отображения.</td></tr>');
                            return;
                        }
    
                        // Заполняем таблицу новыми данными
                        orders.forEach(order => {
                            const row = `
                                <tr>
                                    <td>${order.fields.id}</td>
                                    <td>${new Date(order.fields.created_at).toLocaleString()}</td>
                                    <td>${order.fields.status_name}</td>
                                    <td>${order.fields.user_username}</td>
                                    <td>${order.fields.delivery_address}</td>
                                    <td>${order.fields.phone_number}</td>
                                    <td>
                                        <a href="/order/${order.pk}/" class="btn btn-sm btn-primary">Подробности</a>
                                    </td>
                                </tr>
                            `;
                            tableBody.append(row);
                        });
                    },
                    error: function () {
                        alert("Ошибка при загрузке заказов.");
                    }
                });
            });
        });
    </script>
```

ОШИБКА:
Uncaught TypeError: $.ajax is not a function

