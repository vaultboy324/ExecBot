from entities.user import User

from helper.requests_helper import RequestsHelper
from helper.db_helper import DBRequest


class Requests:

    @staticmethod
    def get_user(user: User):
        request = DBRequest()

        data = RequestsHelper.get_user(user, request)

        request.close()

        return data

    @staticmethod
    def insert_user(user: User):
        request = DBRequest()

        RequestsHelper.insert_user(user, request)

        request.complete()
        request.close()

    @staticmethod
    def insert_user_v2(user: User):
        request = DBRequest()

        RequestsHelper.insert_user_v2(user, request)

        request.complete()
        request.close()

    @staticmethod
    def check_user(user: User):
        request = DBRequest

        result = RequestsHelper.check_user(user, request)

        request.complete()
        request.close()

        return result

    @staticmethod
    def check_password(user: User):
        request = DBRequest()

        data = RequestsHelper.get_user(user, request)

        request.complete()
        request.close()

        # Здесь добавить проверку на корректность пароля
        if not data[0][2]:
            return False
        return True

    @staticmethod
    def update_name(user: User):
        request = DBRequest()

        RequestsHelper.update_uname(user, request)

        request.complete()
        request.close()

    @staticmethod
    def update_password(user: User):
        request = DBRequest()

        RequestsHelper.update_password(user, request)

        request.complete()
        request.close()

    @staticmethod
    def delete_user(user: User):
        request = DBRequest()

        RequestsHelper.delete_user(user, request)

        request.complete()
        request.close()

    @staticmethod
    def get_all_users():
        request = DBRequest()

        data = RequestsHelper.get_all_users(request)

        request.complete()
        request.close()

        return data

    @staticmethod
    def create_status(user: User, start_status):
        request = DBRequest()

        RequestsHelper.create_status(request, user, start_status)

        request.complete()
        request.close()

    @staticmethod
    def change_status(user: User, new_status):
        request = DBRequest()

        RequestsHelper.change_status(request, user, new_status)

        request.complete()
        request.close()

    @staticmethod
    def get_status(user: User):
        request = DBRequest()

        status = RequestsHelper.get_status(user)

        request.complete()
        request.close()

        return status

    @staticmethod
    def set_tabnr(user: User):
        request = DBRequest()

        RequestsHelper.set_tabnr(request, user)

        request.complete()
        request.close()
