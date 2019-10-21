from entities.user import User
from entities.requests import Requests
from config import Statuses

from Constants import Constants


class ActiveUsers:
    users = {}

    @staticmethod
    def check_user(id):
        if ActiveUsers.users.get(id):
            return True
        return False

    @staticmethod
    def update_user(user: User):

        node = {
            Constants.chosen_date: user.get_chosen_date(),
            Constants.role_id: user.get_role(),
            Constants.task_list: user.get_task_list(),
            Constants.current_task: user.get_current_task(),
            Constants.reset_request: user.get_reset_request(),
            Constants.TS: user.get_TS()
        }

        ActiveUsers.users.update({
            user.get_id(): node
        })

        pass

    @staticmethod
    def get_user(id):
        data = ActiveUsers.users.get(id)

        user = User(id)
        user.set_chosen_date(data[Constants.chosen_date])
        user.set_role(data[Constants.role_id])
        user.set_task_list(data[Constants.task_list])
        user.set_current_task(data[Constants.current_task])
        user.set_reset_request(data[Constants.reset_request])
        user.set_TS(data[Constants.TS])

        return user

    @staticmethod
    def delete_user(user: User):
        ActiveUsers.users.pop(user.get_id())

    # @staticmethod
    # def update_dict(user: User):
    #
    #     node = {
    #         "uname": user.get_uname(),
    #         "status": user.get_status(),
    #         "session": user.get_session(),
    #         "client": user.get_client(),
    #         "chosen_date": user.get_chosen_date()
    #     }
    #
    #     status = user.get_status()
    #
    #     if status == Statuses.S_READY_USER or status == Statuses.S_SET_TIME or status == Statuses.S_SEND_VSM or status == Statuses.S_CHANGE_UNAME or status == Statuses.S_CHANGE_PASSWORD:
    #         node["password"] = user.get_password()
    #         node["tabnr"] = user.get_tabnr()
    #
    #     if status == Statuses.S_SET_TIME:
    #         node["task_list"] = user.get_task_list()
    #         node["current_task"] = user.get_current_task()
    #         node["current_day"] = user.get_current_day()
    #
    #     if status == Statuses.S_SEND_VSM:
    #         node["task_list"] = user.get_task_list()
    #         node["current_task"] = ""
    #         node["current_day"] = user.get_current_day()
    #
    #     ActiveUsers.users.update({
    #         user.get_id(): node
    #     })
    #
    #     pass
    #
    # @staticmethod
    # def __get_user_by_id(id):
    #     data = ActiveUsers.users.get(id)
    #
    #     if not data:
    #         return None
    #
    #     user = User(id)
    #
    #     if data:
    #         user.set_uname(data["uname"])
    #         user.set_status(data["status"])
    #         user.set_chosen_date(data["chosen_date"])
    #
    #         if data.get("password"):
    #             user.set_crypt_password(data["password"])
    #
    #         if data.get("tabnr"):
    #             user.set_tabnr(data["tabnr"])
    #
    #         if data.get("task_list"):
    #             user.set_task_list(data["task_list"])
    #
    #         if data.get("current_task"):
    #             user.set_current_task(data["current_task"])
    #         else:
    #             user.set_current_task("")
    #
    #         if data.get("current_day"):
    #             user.set_current_day(data["current_day"])
    #
    #         if data.get("session"):
    #             user.set_session(data["session"])
    #
    #         if data.get("client"):
    #             user.set_client(data["client"])
    #
    #     return user
    #
    # @staticmethod
    # def __create_active_user(id):
    #     user = User(id)
    #     sap_user = Requests.get_user(user)
    #
    #     if sap_user:
    #         user.create_user_by_response(sap_user)
    #     else:
    #         if ActiveUsers.check_user(id):
    #             return
    #
    #     ActiveUsers.update_dict(user)
    #
    # @staticmethod
    # def get_user_by_id(id):
    #     if not ActiveUsers.check_user(id):
    #         ActiveUsers.__create_active_user(id)
    #
    #     return ActiveUsers.__get_user_by_id(id)
    #
    # @staticmethod
    # def check_user(id):
    #     if ActiveUsers.__get_user_by_id(id):
    #         return True
    #     return False
    #
    # @staticmethod
    # def remove_user(id):
    #     ActiveUsers.users.pop(id)
