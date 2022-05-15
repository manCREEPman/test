from json import load
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Test
import traceback


app = Flask('new1')
CORS(app)
debug_state = False

try:
    f = open('./config.json', 'r')
    config_settings = load(f)
    f.close()
    debug_state = config_settings.get('debug')
    if debug_state:
        db_str = config_settings.get('db_local_connection')
    else:
        db_str = config_settings.get('db_connection')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_str
    db.init_app(app)
except:
    print(traceback.format_exc())

@app.route('/api/init_debug_db')
def init_debug_db():
    try:
        if debug_state:
            db.create_all()
            rec1 = Test(1, 'suck')
            rec2 = Test(2, 'fuck')
            db.session.add(rec1)
            db.session.add(rec2)
            db.session.commit()
        return jsonify({'success': 'initialization has completed'})
    except:
        # traceback_log()
        return jsonify({'error': 'fuck'})


@app.route('/api/test_db_api')
def test_db_api():
    test = Test.query.all()[0].to_dict()
    return jsonify(test)

@app.route('/api/first')
def index():
    return jsonify({'data': '^____________^'})


@app.route('/api/register')
def register():
    pass


@app.route('/api/login')
def login():
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0')
