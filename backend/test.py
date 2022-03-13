from flask import Flask, jsonify, request
from flask_cors import CORS
from vk_api import vk_api

app = Flask('new1')
CORS(app)


@app.route('/test/vk_test')
def vk_test():
    app_id = 8099115
    code = request.args.get('code')
    client_secret = 'r6ha68mgEhAB78JFh1zk'
    vk_session = vk_api.VkApi(app_id=app_id, client_secret=client_secret)
    redirect_url = 'http://91.132.102.83/test/vk_test'
    try:
        vk_session.code_auth(code, redirect_url)
        vk = vk_session.get_api()
        vk.wall.post(
            owner_id=-195146403,
            message='suck'
        )
        return jsonify({'success': 'it is alright'})
    except vk_api.AuthError as error_msg:
        return jsonify({'error': error_msg})


@app.route('/test')
def index():
    return jsonify({'data': '^____________^'})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
