from json import load
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Test
from .Models.models import db as db1
import traceback

app = Flask('new1')
CORS(app)

try:
    f = open('./config.json', 'r')
    db_str = load(f).get('db_connection')
    f.close()
    app.config['SQLALCHEMY_DATABASE_URI'] = db_str
    db.init_app(app)
except:
    traceback.print_exc()
    tb = traceback.format_exc()
    with open('./log.txt', 'w') as f:
        f.write(tb)
        f.close()

@app.route('/api/test_db_api')
def test_db_api():
    test = Test.query.all().first().to_dict()
    return jsonify(test)

@app.route('/api/first')
def index():
    return jsonify({'data': '^____________^'})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
