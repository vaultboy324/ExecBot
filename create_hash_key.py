from helper.crypt_helper import Crypt_helper

key = Crypt_helper.create_hash_key()


try:
    f = open('key.txt', 'x')
    f.write(key.decode("utf-8"))
except Exception as e:
    print(Crypt_helper.get_hash_key())

