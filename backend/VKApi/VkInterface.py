import vk_api
from pprint import pprint
from traceback import print_exc
import requests
import os
import random
import json
import re
import time
from datetime import datetime

class AutoPoster:

    def __init__(self) -> None:
        tmp_dict = json.load(open('privates.json', encoding='utf-8'))
        self.__group_id = tmp_dict['group_id']
        auth_data = self._login_pass_get(tmp_dict)
        if auth_data[0] and auth_data[1]:
            self.__vk_session = vk_api.VkApi(
                auth_data[0],
                auth_data[1],
                auth_handler=self._two_factor_auth
            )
        self.__vk_session.auth(token_only=True)
        self.vk = self.__vk_session.get_api()
        self._init_tmp_dir()

    def _init_tmp_dir(self) -> None:
        if not os.path.isdir('./tmp'):
            os.mkdir('./tmp')

    def _two_factor_auth(self):
        key = input("Enter authentication code: ")
        remember_device = True
        return key, remember_device

    def _login_pass_get(self, privates: dict) -> tuple:
        """Получает пару логин и пароль Вконтакте из файла настроек доступа

        Args:
            privates (dict): Настройки доступа

        Returns:
            tuple: Пара - логин и пароль или (None, None)
        """
        try:
            login = privates.get('login', '')
            password = privates.get('password', '')

            #key = self._create_encrypt_key(privates)
            #privates.setdefault('secret_key', key)
            if login == '' and password == '':
                # Поменять по надобности
                # ======================
                print('login:')
                new_login = input()
                print('password:')
                new_pass = input()
                # ======================

                privates.setdefault('login', login)
                privates.setdefault('password', password)

                json.dump(privates, open('./privates.json', 'w'))
                return new_login, new_pass

            return login, password
        except:
            print_exc()
            return None, None


    def _get_image_extension(self, url):
        extensions = ['.png', '.jpg', '.jpeg', '.gif']
        for ext in extensions:
            if ext in url:
                return ext
        return '.jpg'

    def _local_image_upload(self, url: str) -> str:
        """Функция скачивает изображение по url и возвращает строчку с полученным именем файла

        Args:
            url (str): Ссылка на изображение

        Returns:
            str: Имя файла или пустая строка
        """
        try:
            extention = self._get_image_extension(url)
            filename = ''
            if extention != '':
                filename = 'new_image' + extention
                response = requests.get(url)
                image = open('./tmp/' + filename, 'wb')
                image.write(response.content)
                image.close()
            return filename
        except:
            return ''

    def _vk_image_upload(self, image_name: str, tag='#tag') -> dict:
        """Загружает локальное изображение на сервера Вконтакте

        Args:
            image_name (str): Имя файла с изображением

        Returns:
            dict: В случае успешного выполнения запроса вернёт словарь с представлением медиа Вконтакте
        """
        if image_name != '':
            vk_response = self.vk.photos.getWallUploadServer(
                group_id=self.__group_id
            )
            vk_url = vk_response['upload_url']
            try:
                vk_response = requests.post(
                    vk_url,
                    files={'photo': open('./src/VkApi/tmp/{}'.format(image_name), 'rb')}
                ).json()
                os.remove('./src/VkApi/tmp/' + image_name)
                if vk_response['photo']:
                    vk_image = self.vk.photos.saveWallPhoto(
                        group_id=self.__group_id,
                        photo=vk_response['photo'],
                        server=vk_response['server'],
                        hash=vk_response['hash'],
                        caption=tag
                    )
                    return vk_image[0]
            except:
                print_exc()
                return {}
        return {}

    def _form_images_request_signature(self, image_urls: list, tag='') -> str:
        """Получает строку для опубликования медиа-вложений

        Args:
            image_urls (list): Список url-ссылок на изображения

        Returns:
            str:  Возвращает пустую строку или строку вида <type><owner_id>_<media_id>
        """
        result = ''
        result_urls = []
        try:
            urls_count = len(image_urls)
            for i in range(urls_count):
                new_image = self._local_image_upload(image_urls[i])
                if new_image != '':
                    vk_image = self._vk_image_upload(new_image, tag)
                    if vk_image != {}:
                        result += 'photo{}_{}'.format(vk_image['owner_id'], vk_image['id']) + (
                            '' if i == urls_count - 1 else ',')
                        result_urls.append(vk_image['sizes'][-1]['url'])
            if result != '':
                if result[len(result) - 1] == ',':
                    result[:len(result) - 1:]
            return result, result_urls
        except:
            print_exc()
            return '', []

    def post_publication(self, group_id, message: str, img_urls=[], from_group=1, signed=1, tag='#tag'):
        """Позволяет создать запись на стене сообщества.

                Args:
                    message (str): Текст комментария
                    from_group (int, optional): От имени кого будет опубликована запись. 1 - от сообщества, 0 - от имени пользователя. По умолч. = 1
                    img_urls (list, optional): Список url картинок, которые необходимо прикрепить. По умолчанию = [].
                    tag (str, optional): Теги, проставляемые в описании изображения

                Returns:
                    tuple: Возвращает url созданного / изменённого комментария + список url прикреплённых к нему изображений
                """
        try:
            self.__group_id = group_id

            params = {
                'owner_id': f'-{self.__group_id}',
                'message': message,
                'from_group': from_group,
                'guid': random.randint(0, 1000000000),
                'signed': signed,
            }
            attachments = self._form_images_request_signature(img_urls, tag)
            if attachments != ('', []):
                params.setdefault('attachments', attachments[0])

            post_id = self.vk.wall.post(**params)

            res_url = 'https://vk.com/wall-{}_{}'.format(self.__group_id, post_id['post_id'])
            return res_url, attachments[1]
        except:
            print_exc()
            return '', []

    def get_num_id(self, id):
        '''
        Получить числовой айди пользователя

        :param id: ссылка на пользователя в произвольном формате
        :return:
        '''

        id = id.split('/')[-1]
        user = self.vk.users.get(user_ids = id)
        return user[0]['id']

    def get_group_list(self, id):
        '''
        Получение информации о группах, где пользователь является админом.

        :param id: ссылка на пользователя
        :return: список словарей вида
                 admin_type - тип дамина. ["moderator", "editor", "administrator"]
                 ava_url - ссылка на аватар группы в размере 100х100px
                 group_id - числовой индетификатор сообщества
                 group_type - тип группы. ["group", "page", "event"]
                 name - название сообщества
                 short_name - короткий адрес сообщества

        '''

        params = {
            'user_id': self.get_num_id(id),
            'filter': ['admin', 'editor', 'moder', 'advertiser']
        }

        group_list = self.vk.groups.get(**params)['items']

        params = {
            'group_ids': group_list,
        }

        group_info = self.vk.groups.getById(**params)

        admin_level = { 1: "moderator", 2: "editor", 3: "administrator"}

        res_info = []
        for info in group_info:
            res = {}
            res['group_id'] = info['id']
            res['name'] = info['name']
            res['short_name'] = info['screen_name']
            res['ava_url'] = info['photo_100']
            res['admin_type'] = admin_level[info['admin_level']]
            res['group_type'] = info['type']
            res_info.append(res)


        return res_info

    def get_publication(self, domain='', offset=0, count=1, post_id=''):
        '''
        Получение мерик:
             - По набору постов из группы
             - Поконкретному посту

        :param domain: короткий адрес на группу
        :param offset: шаг выборки
        :param count: количество
        :param post_id: по конкретному посту в виде "'-<group_id>_<post_id>'"
        :return:
        '''

        params = {
            'extended': 1
        }

        if post_id != '':
            params['posts'] = [post_id]
            result = self.vk.wall.getById(**params)
        else:
            params['offset'] = offset
            params['domain'] = domain
            params['count'] = count
            result = self.vk.wall.get(**params)

        metrics = {}

        metrics['comments'] = result['items'][0]['comments']['count']
        metrics['likes'] = result['items'][0]['likes']['count']
        metrics['reposts'] = result['items'][0]['reposts']['count']
        metrics['views'] = result['items'][0]['views']['count']

        return metrics

