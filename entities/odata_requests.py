import requests

from config import Config

from entities.user import User
from entities.active_users import ActiveUsers
from entities.tech_user import TechUser
from modules.Utils import Utils

from helper.odata_helper import ODataHelper

import json


class ODataRequests:
    # session = None
    @staticmethod
    def create_user_session():

        # session = user.get_session()
        #
        # if session:
        #     return session

        tech_user = TechUser()

        session = requests.Session()
        session.auth = (tech_user.get_uname(), tech_user.get_decrypt_password())
        session.headers = json.loads(json.dumps(Config.HEADERS))

        response = session.get(Config.BOT_LINK)

        session.headers['Authorization'] = response.request.headers['Authorization']
        # session.headers['x-csrf-token'] = response.headers['x-csrf-token']

        return session

        # user.set_session(session)
        # ActiveUsers.update_dict(user)

    # @staticmethod
    # def get_projects(user:User):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_projects(user)
    #
    # @staticmethod
    # def get_tasks(user:User):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_tasks(user)
    #
    # @staticmethod
    # def get_tasks_names_by_day(user:User):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_tasks_names_by_day(user)
    #
    # @staticmethod
    # def get_tasks_by_day(user:User, day):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_tasks_by_day(day, user)
    #
    # @staticmethod
    # def check_user_role(user:User):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.check_user_role(user)
    #
    # @staticmethod
    # def get_user_tabnr(user:User):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_user_tabnr(user)
    #
    # @staticmethod
    # def check_holiday(user:User, day):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.check_holiday(day, user)
    #
    # @staticmethod
    # def get_user_time(user:User, day):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_user_time(day, user)
    #
    # @staticmethod
    # def get_TS_by_day(user:User, day):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_TS_by_day(day, user)
    #
    # @staticmethod
    # def get_role_id(user:User):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_role_id(user)
    #
    # @staticmethod
    # def get_calendar(user:User, date):
    #     ODataRequests.__create_user_session(user)
    #     return ODataHelper.get_calendar(user, date)
    #
    # @staticmethod
    # def post_time(user:User):
    #     ODataRequests.__create_user_session(user)
    #     ODataHelper.post_time(user.get_task_list(), user)

    @staticmethod
    def get_created_flag(user: User):
        session = ODataRequests.create_user_session()
        return ODataHelper.get_created_flag(session, user)

    @staticmethod
    def get_calendar(user: User):
        session = ODataRequests.create_user_session()
        return ODataHelper.get_calendar(session, user.get_chosen_date())

    @staticmethod
    def get_tasks_by_day(user: User):
        session = ODataRequests.create_user_session()
        return ODataHelper.get_tasks_by_day(session, user)

    @staticmethod
    def get_role_id(user: User):
        session = ODataRequests.create_user_session()
        return ODataHelper.get_role_id(session, user)

    @staticmethod
    def get_ways(user: User):
        session = ODataRequests.create_user_session()
        return ODataHelper.get_ways(session, user)

    @staticmethod
    def get_systems(user: User):
        session = ODataRequests.create_user_session()
        return ODataHelper.get_systems(session, user)

    @staticmethod
    def post_session_request(user: User, err_messages: list):
        session = ODataRequests.create_user_session()
        ODataHelper.post_session_request(session, user, err_messages)

    @staticmethod
    def post_delete_request(user: User):
        session = ODataRequests.create_user_session()
        ODataHelper.post_delete_request(session, user)

    @staticmethod
    def post_time(user: User, err_messages=[]):
        session = ODataRequests.create_user_session()
        ODataHelper.post_time(session, user, err_messages)

    @staticmethod
    def post_reset_session(user: User, err_messages=[]):
        session = ODataRequests.create_user_session()
        ODataHelper.post_reset_session(session, user, err_messages)

    @staticmethod
    def post_drop_reset_session(user: User):
        session = ODataRequests.create_user_session()
        ODataHelper.post_drop_reset_session(session, user)

    @staticmethod
    def post_reset_request(user: User, err_messages=[]):
        session = ODataRequests.create_user_session()
        ODataHelper.post_reset_request(session, user, err_messages)
