from config import Config

from entities.user import User

from Error.TelegramBotError import TelegramBotError
from Error.ErrorParser import ErrorParser

from Constants import Constants

import pyodata
from pyodata.v2.service import GetEntitySetFilter
import json


class ODataHelper:
    # client = None

    @staticmethod
    def __get_metadata(session):

        # client = user.get_client()

        # if client:
        #     return client.entity_sets

        client = pyodata.Client(Config.BOT_LINK, session)

        # user.set_client(client)

        # ActiveUsers.update_dict(user)

        return client.entity_sets

    @staticmethod
    def _post_time_request(session, body: dict, err_messages: list):
        create_request = ODataHelper.__get_metadata(session).TelegramFillSet.create_entity()
        try:
            create_request.set(**body)
            create_request.execute()
        except TelegramBotError as e:
            raise e

    @staticmethod
    def get_created_flag(session, user: User):
        get_request = ODataHelper.__get_metadata(session).TelegramCheckUserSet.get_entity(TelegramId=user.get_id())
        result = get_request.execute()
        return result.IsCreated

    @staticmethod
    def get_calendar(session, date):
        get_request = ODataHelper.__get_metadata(session).TelegramCalendarSet.get_entities()

        month = date[4:6]
        year = date[0:4]

        get_request = get_request.filter(GetEntitySetFilter.and_(get_request.Year == year, get_request.Month == month))
        return get_request.execute()

    @staticmethod
    def get_tasks_by_day(session, user: User):
        get_request = ODataHelper.__get_metadata(session).TelegramTasksSet.get_entities()
        get_request = get_request.filter(GetEntitySetFilter.and_(get_request.TelegramId == user.get_id(), get_request.BegDa == user.get_chosen_date(),
                                                                 get_request.EndDa == user.get_chosen_date(), get_request.StatusId == Constants.base_status))

        return get_request.execute()

    @staticmethod
    def get_role_id(session, user: User):
        current_task = user.get_current_task()

        get_request = ODataHelper.__get_metadata(session).TelegramRoleOnTaskSet.get_entities()
        get_request = get_request.filter(GetEntitySetFilter.and_(get_request.TelegramId == user.get_id(),
                                                                 get_request.TaskId == current_task[Constants.task_id]))

        result = get_request.execute()
        return result[0].RoleId

    @staticmethod
    def get_ways(session, user:User):
        get_request = ODataHelper.__get_metadata(session).TelegramWaysSet.get_entities()
        get_request = get_request.filter(get_request.TelegramId == str(user.get_id()))

        result = get_request.execute()
        return result

    @staticmethod
    def get_systems(session, user: User):
        get_request = ODataHelper.__get_metadata(session).TelegramSystemsSet.get_entities()
        get_request = get_request.filter(get_request.TelegramId == str(user.get_id()))

        result = get_request.execute()
        return result

    @staticmethod
    def post_session_request(session, user: User, err_messages: list):

        create_request = ODataHelper.__get_metadata(session).TelegramSessionSet.create_entity()
        results = {Constants.telegram_id: str(user.get_id()),
                   Constants.uname: user.get_uname()}
        try:
            create_request.set(**results)
            result = create_request.execute()
        except TelegramBotError as e:
            err_messages.append(ErrorParser.args_parse(e.args))

    @staticmethod
    def post_delete_request(session, user: User):
        create_request = ODataHelper.__get_metadata(session).TelegramDeleteInfoSet.create_entity()
        results = {Constants.telegram_id: str(user.get_id())}
        create_request.set(**results)
        create_request.execute()

    @staticmethod
    def post_time(session, user: User, err_messages=[]):

        try:
            TS = user.get_TS()
            telegram_id = str(user.get_id())

            absence_list = user.get_TS().absence_to_list()
            tasks_list = user.get_task_list()

            result = {
                Constants.telegram_timsheet_set: absence_list + tasks_list,
                Constants.telegram_id: telegram_id
            }

            print(result)

            ODataHelper._post_time_request(session, result, err_messages)
        except TelegramBotError as e:
            err_messages.append(ErrorParser.args_parse(e.args))

    @staticmethod
    def post_reset_session(session, user:User, err_messages=[]):
        try:
            create_request = ODataHelper.__get_metadata(session).TelegramResetSet.create_entity()
            result = {
                Constants.session_id: str(user.get_session()),
                Constants.password: ""
            }
            create_request.set(**result)
            new_password = create_request.execute().Password

            user.set_password(new_password)

        except TelegramBotError as e:
            err_messages.append(ErrorParser.args_parse(e.args))

    @staticmethod
    def post_drop_reset_session(session, user: User):
        create_request = ODataHelper.__get_metadata(session).TelegramDropResetSet.create_entity()
        result = {
            Constants.session_id: str(user.get_session())
        }
        create_request.set(**result)
        create_request.execute()

    @staticmethod
    def post_reset_request(session, user:User, err_messages=[]):
        try:
            create_request = ODataHelper.__get_metadata(session).TelegramResetRequestSet.create_entity()
            request = user.get_reset_request()
            result = {
                Constants.telegram_id: str(user.get_id()),
                Constants.way_id: request[Constants.way_id],
                Constants.system: request[Constants.full_info]
            }
            create_request.set(**result)
            create_request.execute()

        except TelegramBotError as e:
            err_messages.append(ErrorParser.args_parse(e.args))
