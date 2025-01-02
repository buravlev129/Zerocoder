import requests
from flask import render_template, flash
from app import app
from app.forms import QueryForm



def prepare_query(searchtype, text, limit=25):
    url = "https://api.quotable.io/"
    stype = "quotes/random"

    if searchtype == "list_quote":
        stype = f"quotes?limit={limit}"
    elif searchtype == "search_quotes":
        text = text.replace("  ", " ")
        text = text.replace(" ", "+")
        stype = f"search/quotes?query={text}&limit={limit}"
    elif searchtype == "random_quotes":
        stype = f"quotes/random?limit={limit}"

    return f"{url}{stype}"


@app.route('/', methods=['GET', 'POST'])
def search():
    reply = []
    form = QueryForm(searchlimit=5)
    if form.validate_on_submit():
        searchtype = form.searchtype.data
        text = form.searchtext.data
        limit = form.searchlimit.data
        url = prepare_query(searchtype, text, limit)
        flash(url)

        response = requests.get(url, verify=False)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                for qt in data:
                    quote = qt.get('content')
                    author = qt.get('author')
                    reply.append((author, quote))
            elif isinstance(data, dict):
                results = data.get("results")
                for qt in results:
                    quote = qt.get('content')
                    author = qt.get('author')
                    reply.append((author, quote))
        else:
            flash('Не удалось получить цитату. Попробуйте еще раз.', 'danger')

    return render_template("index.html", form=form, reply=reply)


