# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def adding_view(id):
    earthquake = Earthquake.query.filter_by(id=id).first()

    if earthquake:
        body = earthquake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(jsonify(body), status)


@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def getting_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)

    body = {
        'count': count,
        'quakes': [e.to_dict() for e in earthquakes] if count > 0 else [],
    }

    if count == 0:
        body['message'] = f'No earthquakes found with magnitude >= {magnitude}'
        status = 404
    else:
        status = 200

    return make_response(jsonify(body), status)


if __name__ == '__main__':
    app.run(port=5555, debug=True)