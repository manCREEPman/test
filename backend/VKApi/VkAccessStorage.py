import traceback
import vk_api
from Models.models import db, User

class VkStorage:
    def __init__(self) -> None:
        self.__objects = {}

    def init_new_vk_object(self, login: str, password: str = None) -> bool:
        try:
            print('Внутри инициализация объекта вк')
            print(f'login: {login}, password: {password}')
            vk_session = vk_api.VkApi(
                login=login,
                password=password if password is not None else None
            )
            vk_session.auth(token_only=True)
            vk = vk_session.get_api()
            self.__objects.setdefault(login, vk)
            return True
        except:
            print('Не удалось инициализировать')
            print(traceback.format_exc())
            return False

    def vk_object_exist(self, login: str) -> bool:
        return not (self.__objects.get(login, None) is None)

    def server_vk_objects_init(self):
        for user in User.query.all():
            try:
                if user.vk_login is not None:
                    self.init_new_vk_object(user.vk_login)
            except:
                print(f'Ошибка в инициализации vk для {user.login}')

vk_storage = VkStorage()