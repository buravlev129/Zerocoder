from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    dt = datetime.now()
    return dt.strftime("%d.%m.%Y %H:%M:%S")


if __name__ == '__main__':
    app.run(debug=True)    