from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import traceback
from flask import Blueprint, jsonify, request, make_response, current_app
from Models.models import db, User

auth = Blueprint('auth', 'new1') 


@auth.route('/register', methods=['POST'])
def register():
    try:
        db.create_all()
        login = request.json.get('login')
        # нужна валидация эмейла
        password = generate_password_hash(request.json.get('password'), method='sha256')
        new_user = User(login=login, password=password)
        db.session.add(new_user)
        db.session.commit()

        response_object = {
            'registration': True,
            'message': 'Registration successful'
        }

        response = make_response(jsonify(response_object))
        cookie_starts = datetime.datetime.utcnow()
        cookie_expires = datetime.datetime.utcnow() + datetime.timedelta(weeks=3)

        auth_cookie = jwt.encode(
            {
                'login': login,
                'cookie_starts': cookie_starts.strftime("%H:%M:%S %d.%m./%Y"),
                'cookie_expires': cookie_expires.strftime("%H:%M:%S %d.%m./%Y")
            },
            current_app.config['SECRET_KEY']
        )

        print(auth_cookie)
        response.set_cookie('auth_token', auth_cookie, expires=cookie_expires)

        # здесь нужно выбрать все сообщества вк пользователя
        return response
    except:
        print(traceback.format_exc())

        response_object = {
            'registration': False,
            'message': 'Registration failed'
        }
        return jsonify(response_object)


@auth.route('/login', methods=['POST'])
def login():
    response_object = {
            'auth': True,
            'vk_auth': False,
            'message': 'Login successful'
    }
    
    try:
        login = request.json.get('login')
        password = request.json.get('password')
        logging_user = User.query.filter_by(login=login).first()
        
        if not logging_user or not check_password_hash(logging_user.password, password):
            response_object['auth'] = False
            response_object['message'] = 'Login failed'
            return jsonify(response_object)
        else:
            
            cookie_starts = datetime.datetime.utcnow()
            cookie_expires = datetime.datetime.utcnow() + datetime.timedelta(weeks=3)

            auth_cookie = jwt.encode(
                {
                    'login': login,
                    'cookie_starts': cookie_starts.strftime("%H:%M:%S %d.%m./%Y"),
                    'cookie_expires': cookie_expires.strftime("%H:%M:%S %d.%m./%Y")
                },
                current_app.config['SECRET_KEY']
            )
            
            # получаем статус авторизации ВК
            if logging_user.vk_login is not None:
                response_object['vk_auth'] = True
            
            response = make_response(jsonify(response_object))
            response.set_cookie('auth_token', auth_cookie, expires=cookie_expires)
            return response
    except:
        print(traceback.format_exc())
        response_object['auth'] = False
        response_object['message'] = 'Server error'
        return jsonify(response_object)


@auth.route('/check_auth')
def check_auth():
    response_object = {
        'auth': False,
        'vk_auth': False,
        'message': ''
    }

    try:
        cookie = request.cookies.get('auth_token')
     
        if cookie:
            cookie_obj = jwt.decode(cookie, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            cookie_starts = datetime.datetime.utcnow() 
            cookie_expires = datetime.datetime.utcnow() + datetime.timedelta(weeks=3)
            login = cookie_obj['login']
            cookie_obj['cookie_starts'] = cookie_starts
            cookie_obj['cookie_expires'] = cookie_expires
            
            logging_user = User.query.filter_by(login=login).first()
            # получаем статус авторизации ВК
            if logging_user.vk_login is not None:
                response_object['vk_auth'] = True

            response_object['auth'] = True
            new_cookie = jwt.encode(
                {
                    'login': login,
                    'cookie_starts': cookie_starts.strftime("%H:%M:%S %d.%m./%Y"),
                    'cookie_expires': cookie_expires.strftime("%H:%M:%S %d.%m./%Y")
                },
                current_app.config['SECRET_KEY']
            )
            response = make_response(jsonify(response_object))
            response.set_cookie('auth_token', new_cookie, expires=cookie_expires)
            return response
        else:  
            response_object['message'] = 'С запросом не переданы cookie'
            return jsonify(response_object)
    except:
        print()
        print()
        print(traceback.format_exc())
        print()
        return jsonify(response_object)
