from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(80),unique = True , nullable = False)
    description = db.Column(db.String(150))

    def __repr__(self):
        return f"{self.title} -> {self.description}"

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return {'name' :'hello guys'}

@app.route('/drinks/add')
def add():
    with app.app_context():
        drink = Drink(
            title='Tea',
            description = 'it wakes me up at morning'
        )

        db.session.add(drink)
        db.session.commit()

        return {
            "message":"added"
        }

@app.route('/drinks/read')
def read():
    drinks = Drink.query.all()

    output = []

    for drink in drinks :
        output.append({
            "id" : drink.id,
            "title" : drink.title,
            "desc" : drink.description
        })

    return output


@app.route('/drinks/read/<id>')
def get_drink_id(id):
    drink = Drink.query.get(id)
    return {
        "id" : drink.id,
        "name" : drink.title,
        "desc" : drink.description
    }

if __name__ == "__main__":
    app.run(debug=True)