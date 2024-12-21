from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    user = { "name": "Sponge Bob" }
    return render_template('index.html', title="Главная страница", user=user)

@app.route('/blog')
def blog():
    user = { "name": "Sponge Bob" }
    return render_template('blog.html', title="Блог", user=user)

@app.route('/contacts')
def contacts():
    user = { "name": "Sponge Bob" }
    return render_template('contacts.html', title="Контакты", user=user)

if __name__ == '__main__':
    app.run(debug=True)
