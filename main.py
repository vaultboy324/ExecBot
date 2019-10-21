import telebot
import json

from threading import Thread

from entities.user import User
from entities.tech_user import TechUser
from entities.active_users import ActiveUsers
from entities.actions import Actions

from Error.ErrorParser import ErrorParser
from Error.TimeError import TimeError
from Error.TelegramBotError import TelegramBotError

from keyboard.Keyboard import Keyboard

from modules.Registration import Registration
from modules.Utils import Utils
from modules.WebSocket import WebSocket

from config import Config
from config import Actions as ActionsEnum

from Constants import Constants

bot = telebot.TeleBot(Config.TOKEN)
telebot.apihelper.proxy = {Config.PROXY_PROTOCOL: Config.PROXY_IP}

tech_user = TechUser()

WebSocket.create_connection()
WebSocket.set_bot(bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = User(message.from_user.id)

    if Registration.check_user(user):
        keyboard = Keyboard.get_main_keyboard()
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Введите uname:")
    pass


@bot.message_handler(commands=['check'])
def check_user(message):
    user = User(message.from_user.id)

    if Registration.check_user(user):
        bot.send_message(user.get_id(), "Id привязан")
    else:
        bot.send_message(user.get_id(), "Id не привязан")
        pass


@bot.message_handler()
def parser(message):
    user = User(message.from_user.id)

    if not Registration.check_user(user):
        user.set_uname(message.text)

        err_messages = []

        Registration.create_request(user, err_messages)

        if len(err_messages) != 0:
            bot.send_message(message.chat.id, ErrorParser.from_list_to_string(err_messages))
        else:
            bot.send_message(message.chat.id, "Для подтверждения регистрации проверьте почту")
    else:
        if ActiveUsers.check_user(user.get_id()):
            user = ActiveUsers.get_user(user.get_id())

            if user.check_task():

                try:
                    user.get_TS().reset_absence(Constants.sick, user.get_chosen_date())
                    user.get_TS().reset_absence(Constants.vacation, user.get_chosen_date())

                    task_time = message.text
                    Actions.write_time(user, task_time)

                    ActiveUsers.update_user(user)

                    status_text = user.get_TS().get_string_status()

                    keyboard = Keyboard.get_action_keyboard()
                    bot.send_message(user.get_id(), f"{status_text}\nВыберите действие", reply_markup=keyboard)

                except TimeError as e:
                    bot.send_message(user.get_id(), e.message)

                except ValueError as e:
                    bot.send_message(user.get_id(), e.args[0])
            else:
                bot.send_message(user.get_id(), "Не выбрана задача")
        else:
            bot.send_message(user.get_id(), "Не выбрано действие")

    pass


@bot.callback_query_handler(func=lambda c: True)
def callback(callback_data):
    data = json.loads(callback_data.data)

    id = callback_data.from_user.id

    if ActiveUsers.check_user(id):
        user = ActiveUsers.get_user(id)
    else:
        user = User(id)

    err_list = []

    bot.delete_message(chat_id=callback_data.message.chat.id, message_id=callback_data.message.message_id)

    keyboard = None
    text = ''

    if data[Constants.type] == ActionsEnum.A_MAIN_DELETE_INFOTYPE:
        Registration.delete_request(user)
        text = "Id удалён из системы"

    elif data[Constants.type] == ActionsEnum.A_MAIN_FILL:

        status_text = Actions.get_fill_status_text(user)

        keyboard = Keyboard.get_fill_keyboard()
        text = f"{status_text}Выберите действие"

    elif data[Constants.type] == ActionsEnum.A_TO_START:
        keyboard = Keyboard.get_main_keyboard()
        text = "Выберите действие"

    elif data[Constants.type] == ActionsEnum.A_FILL_TODAY or \
            data[Constants.type] == ActionsEnum.A_FILL_YESTERDAY or \
            data[Constants.type] == ActionsEnum.A_CALENDAR_ACTION:

        if data.get(Constants.cdate):
            user.set_chosen_date(data[Constants.cdate])
        else:
            Actions.choose_day_by_action_type(data[Constants.type], user)

        task_list = Actions.get_tasks_by_day(user)

        try:
            user.get_TS().update(user.get_id(), user.get_chosen_date(), task_list)

            status_text = Actions.get_fill_status_text(user)

            keyboard = Keyboard.get_fill_type_keyboard(user)
            text = f"{status_text}\nВыберите действие"
        except TelegramBotError:
            keyboard = Keyboard.get_main_keyboard()
            text = "У вас нет задач!"

    elif data[Constants.type] == ActionsEnum.A_FILL_TYPE_SICK or \
            data[Constants.type] == ActionsEnum.A_FILL_TYPE_VACATION or \
            data[Constants.type] == ActionsEnum.A_FILL_TYPE_MISSION:
        TS = user.get_TS()

        TS.reset_absence(Constants.sick, user.get_chosen_date())
        TS.reset_absence(Constants.vacation, user.get_chosen_date())
        TS.reset_absence(Constants.mission, user.get_chosen_date())

        Actions.add_node(user, data[Constants.type])

        status_text = TS.get_string_status_for_date(user.get_chosen_date())

        keyboard = Keyboard.get_action_keyboard()
        text = f"{status_text}\nВыберите действие"

    elif data[Constants.type] == ActionsEnum.A_FILL_ANOTHER_DAY:
        Actions.move_calendar(data, user)

        month = Utils.get_month_by_chosen_date(user.get_chosen_date())

        keyboard = Keyboard.get_calendar(user)
        text = f"Выбранный месяц: {month}\nВыберите день"

    elif data[Constants.type] == ActionsEnum.A_FILL_TYPE_TIME:
        task_list = Actions.get_tasks_by_day(user)

        user.get_TS().update(user.get_id(), user.get_chosen_date(), task_list)

        keyboard = Keyboard.get_tasks_keyboard(user)
        text = "Выберите задачу"

    elif data[Constants.type] == ActionsEnum.A_FILL_FOR_DATE:
        Actions.create_task_for_user(user, data[Constants.task_id])
        text = "Введите время отведённое на задачу"

    elif data[Constants.type] == ActionsEnum.A_APPROVE:
        Actions.approve_changes(user, err_list)

        if len(err_list) != 0:
            text = ErrorParser.from_list_to_string(err_list)
        else:
            text = "Изменения выполнены"

        keyboard = Keyboard.get_main_keyboard()

    elif data[Constants.type] == ActionsEnum.A_RESET:
        Actions.approve_changes(user)

        keyboard = Keyboard.get_main_keyboard()
        text = "Изменения отклонены"

    elif data[Constants.type] == ActionsEnum.A_RESET_MISSION:
        TS = user.get_TS()
        chosen_date = user.get_chosen_date()
        TS.reset_mission_node(chosen_date)

        status_text = Actions.get_fill_status_text(user)

        keyboard = Keyboard.get_fill_type_keyboard(user)
        text = f"{status_text}\nВыберите действие"

    elif data[Constants.type] == ActionsEnum.A_ACTIVE_MISSION:
        user.get_TS().write_absence(user.get_chosen_date(), data[Constants.type])

        status_text = Actions.get_fill_status_text(user)

        keyboard = Keyboard.get_fill_type_keyboard(user)
        text = f"{status_text}\nВыберите действие"

    elif data[Constants.type] == ActionsEnum.A_APPROVE_REQUEST:
        user.set_session(data[Constants.session_guid])
        Actions.reset_pass(user, err_list)

        if len(err_list) != 0:
            text = ErrorParser.from_list_to_string(err_list)
        else:
            text = f"Ваш временный пароль: {user.get_password()}"

        keyboard = Keyboard.get_main_keyboard()

    elif data[Constants.type] == ActionsEnum.A_RESET_REQUEST:
        user.set_session(data[Constants.session_guid])
        Actions.drop_reset_session(user)

        text = "Запрос на сброс пароля отменён"
        keyboard = Keyboard.get_main_keyboard()

    elif data[Constants.type] == ActionsEnum.A_RESET_PASSWORD:
        ways = Actions.get_ways(user)
        user.set_ways(ways)

        keyboard = Keyboard.get_ways_keyboard(user)
        text = f"{user.get_request_text()}Выберите способ сброса пароля"

    elif data[Constants.type] == ActionsEnum.A_CHOOSE_WAY:
        way_id = data[Constants.way_id]
        Actions.create_request_for_user(user, way_id)

        systems = Actions.get_systems(user)
        user.set_systems(systems)

        keyboard = Keyboard.get_system_keyboard(user)
        text = f"{user.get_request_text()}Выберите систему"

    elif data[Constants.type] == ActionsEnum.A_CHOOSE_SYSTEM:
        system = data[Constants.full_info]
        Actions.add_system_to_request(user, system)

        keyboard = Keyboard.get_reset_approve_keyboard(user)
        text = f"{user.get_request_text()}"

    elif data[Constants.type] == ActionsEnum.A_APPROVE_DROP:
        Actions.send_drop_request(user, err_list)

        if len(err_list):
            text = ErrorParser.from_list_to_string(err_list)
            keyboard = Keyboard.get_main_keyboard()
        else:
            text = "Запрос на сброс пароля отправлен"

            request_type = Actions.get_request_type(user)

            if request_type == Constants.email_reset:
                keyboard = Keyboard.get_main_keyboard()

            Actions.clear_request(user)

    bot.send_message(user.get_id(), text, reply_markup=keyboard)

    ActiveUsers.update_user(user)


def listen_bot():
    bot.polling(none_stop=True, timeout=300)


Thread(target=listen_bot).start()
Thread(target=WebSocket.listen).start()
