from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange



class QueryForm(FlaskForm):
    searchtype = SelectField("Тип запроса", choices=[
        ("random_quotes", "random quotes"),
        ("list_quote", "list quote"),
        ("search_quotes", "search quotes")
    ])
    searchtext = StringField("Строка поиска")
    searchlimit = IntegerField("Ограничение (строк)", validators=[DataRequired(), NumberRange(min=1, max=25)])
    submit = SubmitField("Выполнить")

  