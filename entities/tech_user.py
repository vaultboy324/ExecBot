from helper.crypt_helper import Crypt_helper
import json


class TechUser:

    def __init__(self):
        self.__user_info = Crypt_helper.get_tech_user_info()

    def get_uname(self):
        return self.__user_info['login']

    def get_password(self):
        return self.__user_info['password'].encode()

    def get_decrypt_password(self):
        return Crypt_helper.decrypt_string(self.get_password(), Crypt_helper.get_hash_key()).decode("utf-8")