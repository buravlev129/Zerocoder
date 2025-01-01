
Есть такая формочка для входа на сайт с помощью логина и пароля.
Форма сделана с использованием шаблонов Flask

{% block content %}
<div class="login-form">
    <h3 class="text-center">Вход</h3>
    <form method="post" action="{{ url_for('login') }}">
        {{ form.hidden_tag() }}
        <table>
            <tr><td>{{ form.email.label }}:</td>
                <td>{{ form.email(size=32) }}</td>
            </tr>
            <tr><td>{{ form.password.label }}:</td>
                <td>{{ form.password(size=32) }}</td>
            </tr>
            <tr><td>&nbsp;</td>
                <td>{{ form.remember() }} &nbsp; {{ form.remember.label }}</td>
            </tr>
            <tr><td>&nbsp;</td>
                <td>{{ form.submit() }}</td>
            </tr>
        </table>
    </form>
</div>
{% endblock %}

Для размещения компонентов формы здесь используется таблица.
Переделай этот код, чтобы вместо таблицы использовался современный подход с помощью div и bootstrap.
Сделай красивое размещение контролов на форме.
Форма должна иметь ширину 420px, высоту 250px.
У формы должна быть рамка и тень.
Между контролами на форме должны быть отступы по вертикали 3px


    <style>
        .login-form {
            width: 420px;
            height: 250px;
            border: 1px solid #ccc;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin: auto;
            margin-top: 50px;  /* Для центрирования по вертикали */
        }
    </style>


Напиши простое приложение на Flask по следующим требованиям:
Приложение содержит четыре страницы
1) Стартовая страница с кнопками "Логин" и "Регистрация"
   Кнопка "Логин" открывает страницу с формочкой для ввода логина и пароля
   Кнопка "Регистрация" открывает форму регистрации
2) Страница с формочкой для ввода логина и пароля
3) Страница с формочкой для регистрации
   После регистрации в базу (Sqlite) добавляется новый пользователь
4) Страница с формочкой для редактирования данных пользователя
   На этой странице можно изменить имя пользователя и пароль.
   После редактирования данные сохраняются в базу Sqlite

Для работы создай класс User с полями id, username, email и password
При редактировании данных пользователя на форме эти данные сохраняются в базе по id пользователя


- 

с помощью FlaskForm создается класс

class EditForm(FlaskForm):
    userid = StringField('ID', validators=[DataRequired()])
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])

Для этого класса есть форма редактирования данных.
Напиши метод editdata для файла route.py, который будет отображать данные пользователя на форме редактирования и сохранять отредактированные данные в базу



Есть такая Flask форма

class EditForm(FlaskForm):
    userid = StringField('ID', validators=[DataRequired()], render_kw={'readonly': True})
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повтор пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сохранить')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такая почта уже используется')

Эта форма вызывается в модуле routes.py

@app.route('/edit', methods=['GET', 'POST'])
def editdata():
    form = EditForm(obj=current_user)

Допиши метод editdata, чтобы в нем сохранялись данные с формы после редактирования.
Добавь в этом методе обработку ошибок, которые генерируются в классе EditForm


