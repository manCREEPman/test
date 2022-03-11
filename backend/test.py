from flask import Flask, jsonify
from flask_cors import CORS

app = Flask('new1')
CORS(app)

@app.route('/test')
def index():
    return jsonify({'data': '^____________^'})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
