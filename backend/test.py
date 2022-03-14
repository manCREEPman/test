from flask import Flask, jsonify, request
from flask_cors import CORS
from vk_api import vk_api
import sys
import traceback

app = Flask('new1')
CORS(app)


@app.route('/test/vk_test')
def vk_test():
    app_id = 8099115
    code = request.args.get('code')
    client_secret = 'r6ha68mgEhAB78JFh1zk'
    vk_session = vk_api.VkApi(app_id=app_id, client_secret=client_secret)
    redirect_url = 'http://91.132.102.83'
    try:
        vk_session.code_auth(code, redirect_url)
        vk = vk_session.get_api()
        vk.wall.post(
            owner_id=-195146403,
            message='suck'
        )
        f = open('./log.txt', 'w')
	f.write('success')
	f.close()
    except:
	tb = sys.exc_info()[2]
    	tbinfo = traceback.format_tb(tb)[0]
    	# Concatenate information together concerning the error into a message string
    	pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        f = open('./log.txt', 'w')
        f.write(pymsg)
	f.close()

@app.route('/test')
def index():
    return jsonify({'data': '^____________^'})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
