from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# QuoteModel --> dict --> JSON
class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    text = db.Column(db.String(255), unique=False)
    rating = db.Column(db.SmallInteger())

    def __init__(self, author, text):
        self.author = author
        self.text = text

    def __repr__(self):
        return f"Quote: {self.author} {self.text}"

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text
        }


# Сериализация: lis[quotes] --> list[dict] --> str(JSON)
@app.route("/quotes")
def get_all_quotes():
    quotes = QuoteModel.query.all()
    quotes_dict = []
    for quote in quotes:
        quotes_dict.append(quote.to_dict())
    return quotes_dict


@app.route("/quotes/<int:id>")
def get_quote(id):
    quote = QuoteModel.query.get(id)
    if quote is None:
        return {"error": f"Quote with id={id} not found"}, 404
    return quote.to_dict(), 200


@app.route("/quotes", methods=['POST'])
def create_quote():
    quote_data = request.json
    quote = QuoteModel(quote_data["author"], quote_data["text"])
    db.session.add(quote)
    db.session.commit()
    return quote.to_dict()


@app.route("/quotes/<int:id>", methods=['PUT'])
def edit_quote(id):
    quote_data = request.json
    quote = QuoteModel.query.get(id)
    if quote is None:
        return {"error": f"Quote with id={id} not found"}, 404
    # if quote_data.get("text"):
    #     quote.text = quote_data['text']
    # if quote_data.get("author"):
    #     quote.author = quote_data['author']
    for key, value in quote_data.items():
        setattr(quote, key, value)
    db.session.commit()
    return quote.to_dict(), 200


@app.route("/quotes/filter")
def get_quotes_filter():
    args = request.args
    print(args)
    # TODO: закончить реализацию
    return {}


@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id):
    quote = QuoteModel.query.get(id)
    if quote is None:
        return {"error": f"Quote with id={id} not found"}, 404
    db.session.delete(quote)
    db.session.commit()
    return {"message": f"Quote with id={id} deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True)
