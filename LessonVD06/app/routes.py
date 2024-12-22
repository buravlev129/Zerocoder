from flask import render_template, request, redirect, url_for
from app import app

anketa = {}

@app.route('/', methods=["GET", "POST"])
@app.route('/home')
@app.route('/home.html')
def index():
    global anketa
    user = { "name": "Sponge Bob" }
    active = { "home": "active", "about": ""}
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        hobby = request.form.get('hobby')
        age = request.form.get('age')

        if name and city and hobby and age:
            anketa = {'name': name, 'city': city, "hobby": hobby, "age": age}
            return redirect(url_for('index'))

    return render_template('home.html', title="Главная страница", user=user, active=active, anketa=anketa)

