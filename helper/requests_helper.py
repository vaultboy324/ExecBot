from entities.user import User

from helper.db_helper import DBRequest


class RequestsHelper:

    @staticmethod
    def get_user(user: User, request: DBRequest):
        cursor = request.get_cursor()
        cursor.execute(f"SELECT * FROM users WHERE _id = '{user.get_id()}'")
        return cursor.fetchall()

    @staticmethod
    def insert_user(user: User, request: DBRequest):
        cursor = request.get_cursor()
        cursor.execute(f"INSERT INTO users VALUES ('{user.get_id()}', '{user.get_uname()}', '{user.get_password()}')")

    @staticmethod
    def insert_user_v2(user: User, request: DBRequest):
        cursor = request.get_cursor()
        cursor.execute(f"INSERT INTO users VALUES ('{user.get_id()}', '{user.get_uname()}',  '{user.get_password()}', '{user.get_tabnr()}')")

    @staticmethod
    def check_user(user: User, request: DBRequest):
        users = RequestsHelper.get_user(user, request)

        if len(users) == 0:
            return False

        return True

    @staticmethod
    def update_uname(user:  User, request: DBRequest):
        cursor = request.get_cursor()
        cursor.execute(f"UPDATE users SET uname = '{user.get_uname()}' WHERE _id = '{user.get_id()}'")

    @staticmethod
    def update_password(user: User, request: DBRequest):
        cursor = request.get_cursor()
        cursor.execute(f"UPDATE users SET password = '{user.get_password()}' WHERE _id = '{user.get_id()}'")

    @staticmethod
    def delete_user(user: User, request: DBRequest):
        cursor = request.get_cursor()
        cursor.execute(f"DELETE FROM users WHERE _id = '{user.get_id()}'")

    @staticmethod
    def get_all_users(request: DBRequest):
        cursor = request.get_cursor()
        cursor.execute(f"SELECT * FROM users")
        return cursor.fetchall()

    @staticmethod
    def create_status(request: DBRequest, user: User, start_status):
        cursor = request.get_cursor()
        cursor.execute(f"INSERT INTO user_statuses VALUES('{user.get_id()}', '{start_status}')")

    @staticmethod
    def change_status(request: DBRequest, user: User, new_status):
        cursor = request.get_cursor()
        cursor.execute(f"UPDATE user_statuses SET status = '{new_status}' WHERE _id = '{user.get_id()}'")

    @staticmethod
    def set_tabnr(request: DBRequest, user: User):
        cursor = request.get_cursor()
        cursor.execute(f"UPDATE users SET tabnr = '{user.get_tabnr()}' WHERE _id = '{user.get_id()}'")

    @staticmethod
    def get_status(request: DBRequest, user: User):
        cursor = request.get_cursor()
        cursor.execute(f"SELECT status FROM user_statuses WHERE _id = '{user.get_id()}'")