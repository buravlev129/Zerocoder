from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, EditForm
from app.models import User



def prepare_user():
    if current_user:
        if current_user.is_anonymous:
            return "[Anonymous]"
        else:
            return f"Привет, {current_user.username}"
    else:
        return "[Anonymous]"


@app.route('/', methods=["GET", "POST"])
@app.route('/home.html')
def home():
    hello = prepare_user()
    return render_template("home.html", title='Home', hello=hello, is_anonymous=current_user.is_anonymous)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))

    hello = prepare_user()
    return render_template("register.html", form=form, title='Register', hello=hello, is_anonymous=current_user.is_anonymous)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('account'))
        else:
            flash('Введены неверные данные', 'error')

    hello = prepare_user()
    return render_template("login.html", form=form, title='Login', hello=hello, is_anonymous=current_user.is_anonymous)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def editdata():
    form = EditForm(obj=current_user)
    form.userid.data = current_user.id

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = hashed_password
        try:
            db.session.commit()
            flash('Данные успешно сохранены', 'success')
        except Exception as ex:
            flash(f"ERROR: {str(ex)}", 'error')
        
        return redirect(url_for('account'))

    hello = prepare_user()
    return render_template("edit.html", form=form, title='Edit', hello=hello, is_anonymous=current_user.is_anonymous)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    hello = prepare_user()
    return render_template("account.html", title='Account', hello=hello, is_anonymous=current_user.is_anonymous)

