import random
import sqlite3
from flask import Flask, abort, request
from flask import g
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / "testdatabase.db"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception): # эксепшн выдает исключение traceback
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Сериализация: list --> str
@app.route("/quotes")
def get_all_quotes():
    # Подключение в БД
    connection = get_db()
    cursor = connection.cursor()
    select_quotes = "SELECT * from quotes"
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchall()
    cursor.close()
    quotes = []
    keys = ["id", "author", "text"]
    for quote_db in quotes_db:
        quote = dict(zip(keys, quote_db)) # отработать зип на 2-х списках и сделать словарь
        quotes.append(quote)
    return quotes


@app.route("/quotes/<int:id>")
def get_quote(id):
    connection = get_db()
    cursor = connection.cursor()
    select_quotes = f"SELECT * FROM quotes WHERE id={id};"
    cursor.execute(select_quotes)
    quote_db = cursor.fetchone()
    # print("quote_db = ", quote_db)
    cursor.close()
    if quote_db is None:
        abort(404, f"Quote with id={id} not found")
    keys = ["id", "author", "text"]
    quote = dict(zip(keys, quote_db))
    return quote


@app.route("/quotes", methods=['POST'])
def create_quote():
    quote_data = request.json
    connection = get_db()
    cursor = connection.cursor()
    create_quote = "INSERT INTO quotes (author,text) VALUES (?, ?)"
    cursor.execute(create_quote, (quote_data["author"], quote_data["text"]))
    connection.commit()
    cursor.close()
    return {}, 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    quote_data = request.json
    connection = get_db()
    cursor = connection.cursor()
    new_quote_data = (quote_data["author"], quote_data["text"])
    update_quote = "UPDATE quotes SET author=?, text=? WHERE id=?"
    cursor.execute(update_quote, (*new_quote_data, quote_id))
    connection.commit()
    # print("cursor.rowcount = ", cursor.rowcount)
    cursor.close()
    if cursor.rowcount == 0:
        abort(404, f"Указанного id= {quote_id}, не существует")
    return {}, 200


@app.route("/quotes/filter")
def get_quotes_filter():
    args = request.args
    print(args)
    # TODO: закончить реализацию
    return {}


@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id):
    connection = get_db()
    cursor = connection.cursor()
    quote_db = cursor.fetchone()
    cursor.execute(quote_db)
    connection.commit()
    quotes = []
    keys = ["id", "author", "text"]
    quote = dict(zip(keys, quote_db))
    quotes.append(quote)
    for quote in quotes:
        if id == quote['id']:
            quotes.remove(quote)
            return f"Quote with id {id} is deleted.", 200
    abort(404, f"Указанного id= {id}, не существует")


if __name__ == "__main__":
    app.run(debug=True)