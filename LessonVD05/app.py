from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/home.html')
def index():
    user = { "name": "Sponge Bob" }
    active = { "home": "active", "about": ""}
    return render_template('home.html', title="Главная страница", user=user, active=active)

@app.route('/about')
@app.route('/about.html')
def contacts():
    user = { "name": "Sponge Bob" }
    active = { "home": "", "about": "active"}
    return render_template('about.html', title="Полезная информация", user=user, active=active)

if __name__ == '__main__':
    app.run(debug=True)
