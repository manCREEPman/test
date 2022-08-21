from traceback import format_exc
from flask import Blueprint, jsonify, request, make_response, current_app
from Models.models import db, User
from VKApi.VkAccessStorage import vk_storage
import jwt

vk_auth = Blueprint('vk_auth', 'new1')

@vk_auth.route('/login', methods=['POST'])
def vk_login():
    # получаем параметры
    cookie = request.cookies.get('auth_token')
    vk_login_str = request.json.get('vk_login')
    vk_password = request.json.get('password')

    response_object = {
        'vk_auth': False,
        'message': ''
    }

    if cookie:
        cookie_obj = jwt.decode(cookie, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        login = cookie_obj.get('login', '')

        if vk_storage.init_new_vk_object(vk_login_str, vk_password):
            try:
                current_user = User.query.filter_by(login=login).first()
                current_user.vk_login = vk_login_str
                db.session.commit()
                response_object['vk_auth'] = True
                response_object['message'] = 'Авторизация ВК успешна'
            except:
                error_msg = 'Проблема с обновлением логина ВК'
                print(error_msg)
                print(format_exc())
                response_object['message'] = error_msg
        else:
            response_object['message'] = 'Не удалось инициалировать ВК объект'
    else:
        response_object['message'] = 'Нет авторизационного cookie'
        
    response = make_response(jsonify(response_object))
    return response

    