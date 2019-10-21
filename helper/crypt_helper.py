from cryptography.fernet import Fernet
import json

class Crypt_helper:
    @staticmethod
    def create_hash_key():
        return Fernet.generate_key()

    @staticmethod
    def get_hash_key():
        f = open("key.txt", "r")
        key = f.read()
        return key

    @staticmethod
    def encrypt_string(string, key):
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(string)
        return cipher_text

    @staticmethod
    def decrypt_string(string, key):
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(string)
        return plain_text

    @staticmethod
    def get_tech_user_info():
        f = open("user_info.json", "r")
        json_string = f.read()
        return json.loads(json_string)