from enum import Enum

import json

with open('config.json', 'r') as f:
    data = json.load(f)


class Config():
    TOKEN = data['token']
    PROXY_PROTOCOL = data['proxy']['protocol']
    PROXY_IP = data['proxy']['ip']
    DB_PATH = data['db_path']
    AUTH_LINK = data['auth_link']
    TS_LINK = data['ts_link']
    BOT_LINK = data['bot_link']
    SOCKET_LINK = data['socket_link']
    SUBPROTOCOLS = data["subprotocols"]
    HEADERS = data['headers']
    REMINDER_TIME = data['send_time']
    STICKER_CODE = data['sticker_code']
    POSTGRES_DB = data['postgres_info']['database']
    POSTGRES_USER = data['postgres_info']['user']
    POSTGRES_PASSWORD = data['postgres_info']['password']
    POSTGRES_HOST = data['postgres_info']['host']


class Statuses(Enum):
    S_START = 0
    S_ENTER_UNAME = 1
    S_ENTER_PASSWORD = 2
    S_READY_USER = 3
    S_SET_TIME = 4
    S_SEND_VSM = 5
    S_CHANGE_UNAME = 6
    S_CHANGE_PASSWORD = 7


class Actions():
    # A_GET_TASK_KEYBOARD = 1
    # A_CREATE_TASK_NOTE = 2
    # A_SEND_TIME = 3
    # A_CLEAR_TASKS = 4
    # A_GET_MAIN_KEYBOARD = 5
    # A_POST_CHANGES = 6
    # A_BACK_TO_TASKS = 7
    # A_VSM = 8
    # A_OPEN_CALENDAR = 9
    # A_GET_ACTION_KEYBOARD = 10
    # A_CHANGE_UNAME = 11
    # A_CHANGE_PASSWORD = 12
    A_MAIN_DELETE_INFOTYPE = 1
    A_MAIN_FILL = 2
    A_FILL_TODAY = 3
    A_FILL_YESTERDAY = 4
    A_FILL_ANOTHER_DAY = 5
    A_TO_START = 6
    A_CALENDAR_ACTION = 7
    A_FILL_FOR_DATE = 8
    A_FILL_TYPE_TIME = 9
    A_FILL_TYPE_SICK = 10
    A_FILL_TYPE_MISSION = 11
    A_FILL_TYPE_VACATION = 12
    A_FILL_TYPE_MISSION_TIME = 13
    A_MISSION_ACTION = 14
    A_APPROVE = 15
    A_RESET = 16
    A_CHANGE = 17
    A_RESET_MISSION = 18
    A_ACTIVE_MISSION = 19
    A_RESET_REQUEST = 20
    A_APPROVE_REQUEST = 21
    A_RESET_PASSWORD = 22
    A_CHOOSE_WAY = 23
    A_CHOOSE_SYSTEM = 24
    A_APPROVE_DROP = 25


class SocketActions():
    S_SEND_NOTIFY = 1
    S_SEND_STICKER = 2
    S_SEND_RESET_REQUEST = 3


