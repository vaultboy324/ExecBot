from entities.user import User
from entities.odata_requests import ODataRequests

from Error.ErrorParser import ErrorParser


class Registration:
    @staticmethod
    def check_user(user: User):
        return ODataRequests.get_created_flag(user)

    @staticmethod
    def create_request(user: User, err_messages):
        ODataRequests.post_session_request(user, err_messages)

    @staticmethod
    def delete_request(user: User):
        ODataRequests.post_delete_request(user)
        # ODataRequests.delete_telegram_id(user)