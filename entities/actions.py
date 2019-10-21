import telebot
import json

from datetime import datetime, timedelta

from entities.odata_requests import ODataRequests
from entities.user import User

from Constants import Constants

from entities.task import Task
from entities.active_users import ActiveUsers
from entities.calendar import Calendar
from entities.requests import Requests

from Error.TimeError import TimeError

from config import Statuses
from config import Actions as ActionsEnum


class Actions:
    @staticmethod
    def __choose_today(user: User):
        date = datetime.today()
        user.set_chosen_date(date)

    @staticmethod
    def __choose_yesterday(user: User):
        date = datetime.today() - timedelta(days=1)
        user.set_chosen_date(date)

    @staticmethod
    def move_calendar(action_data, user: User):
        if action_data.get(Constants.movement):
            if action_data[Constants.movement] == Constants.left:
                user.set_prev_month()
            else:
                user.set_next_month()

    @staticmethod
    def get_tasks_by_day(user: User):
        return ODataRequests.get_tasks_by_day(user)

    @staticmethod
    def create_task_for_user(user: User, task_id=''):
        task = {
            Constants.telegram_id: str(user.get_id()),
            Constants.task_id: task_id,
            Constants.cdate: user.get_chosen_date(),
            Constants.role_id: user.get_role()
        }

        user.set_current_task(task)

    @staticmethod
    def choose_day_by_action_type(action_type, user: User):
        if action_type == ActionsEnum.A_FILL_TODAY:
            Actions.__choose_today(user)
        elif action_type == ActionsEnum.A_FILL_YESTERDAY:
            Actions.__choose_yesterday(user)

    @staticmethod
    def approve_changes(user: User, err_list=[]):
        ODataRequests.post_time(user, err_list)
        user.clear()
        ActiveUsers.delete_user(user)

    @staticmethod
    def reset_changes(user: User):
        user.set_task_list([])
        user.clear()
        ActiveUsers.delete_user(user)

    @staticmethod
    def write_time(user: User, task_time, err_list=[]):
        role_id = ODataRequests.get_role_id(user)
        user.set_role(role_id)

        try:
            Actions.add_node(user, ActionsEnum.A_FILL_TYPE_TIME, task_time)
        except TimeError as e:
            raise e
        except ValueError as e:
            raise e

    @staticmethod
    def add_node(user: User, node_type=ActionsEnum.A_FILL_TYPE_TIME, time=Constants.base_time):
        current_task = user.get_current_task()

        chosen_date = user.get_chosen_date()

        TS = user.get_TS()

        if node_type == ActionsEnum.A_FILL_TYPE_TIME:
            current_task[Constants.presence] = True

            current_task[Constants.role_id] = user.get_role()
            current_task[Constants.chours] = time

            try:
                user.get_TS().change_time_in_task(current_task[Constants.cdate],
                                                  current_task[Constants.task_id],
                                                  current_task[Constants.chours])

                current_task[Constants.update] = True
                user.add_task_to_list(current_task)
                user.set_current_task({})
            except TimeError as e:
                raise e
            except ValueError as e:
                raise e
        else:
            user.get_TS().write_absence(chosen_date, node_type)

    @staticmethod
    def reset_pass(user: User, err_messages=[]):
        ODataRequests.post_reset_session(user, err_messages)

    @staticmethod
    def drop_reset_session(user: User):
        ODataRequests.post_drop_reset_session(user)

    @staticmethod
    def get_fill_status_text(user: User):
        return user.get_TS().get_string_status()

    @staticmethod
    def get_ways(user: User):
        ways = []
        ep_ways = ODataRequests.get_ways(user)

        for ep_way in ep_ways:
            way = {}
            way[Constants.telegram_id] = ep_way.TelegramId
            way[Constants.way_id] = str(ep_way.WayId)
            way[Constants.way_text] = ep_way.Text

            ways.append(way)

        return ways

    @staticmethod
    def get_systems(user: User):
        systems = []
        ep_systems = ODataRequests.get_systems(user)

        for ep_system in ep_systems:
            system = {}
            system[Constants.telegram_id] = ep_system.TelegramId
            system[Constants.full_info] = ep_system.FullInfo
            systems.append(system)

        return systems

    @staticmethod
    def create_request_for_user(user: User, way_id):
        request = {
            Constants.way_id: way_id
        }
        user.set_reset_request(request)

    @staticmethod
    def add_system_to_request(user: User, system):
        request = user.get_reset_request()
        request[Constants.full_info] = system
        # user.set_reset_request(request)

    @staticmethod
    def send_drop_request(user: User, err_messages):
        ODataRequests.post_reset_request(user, err_messages)

    @staticmethod
    def get_request_type(user: User):
        request = user.get_reset_request()

        return request[Constants.way_id]

    @staticmethod
    def clear_request(user: User):
        user.set_reset_request({})