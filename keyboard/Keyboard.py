import telebot
import json

from config import Actions

from entities.calendar import Calendar
from entities.user import User

from Constants import Constants


class Keyboard:
    @staticmethod
    def __create_button(button_type=None, text="", params={}):
        callback_data = {
            Constants.type: button_type,
        }
        callback_data.update(params)

        json_string = json.dumps(callback_data)

        return telebot.types.InlineKeyboardButton(text=text, callback_data=json_string)

    @staticmethod
    def get_main_keyboard():
        markup = telebot.types.InlineKeyboardMarkup()

        fill_button = Keyboard.__create_button(Actions.A_MAIN_FILL, "Заполнить ТШ")
        markup.add(fill_button)

        reset_button = Keyboard.__create_button(Actions.A_RESET_PASSWORD, "Сбросить пароль")
        markup.add(reset_button)

        delete_button = Keyboard.__create_button(Actions.A_MAIN_DELETE_INFOTYPE, "Удалить telegram id из системы")
        markup.add(delete_button)

        return markup

    @staticmethod
    def get_fill_keyboard():
        markup = telebot.types.InlineKeyboardMarkup()

        fill_today_button = Keyboard.__create_button(Actions.A_FILL_TODAY, "Заполнить за сегодня")
        markup.add(fill_today_button)

        fill_yesterday_button = Keyboard.__create_button(Actions.A_FILL_YESTERDAY, "Заполнить за вчера")
        markup.add(fill_yesterday_button)

        fill_another_day_button = Keyboard.__create_button(Actions.A_FILL_ANOTHER_DAY, "Заполнить за другой день")
        markup.add(fill_another_day_button)

        back_button = Keyboard.__create_button(Actions.A_TO_START, "Перейти в главное меню")
        markup.add(back_button)

        return markup

    @staticmethod
    def get_fill_type_keyboard(user: User):
        markup = telebot.types.InlineKeyboardMarkup()

        params = {Constants.date: user.get_chosen_date()}

        fill_type_time = Keyboard.__create_button(Actions.A_FILL_TYPE_TIME, "Записать время", params)
        markup.add(fill_type_time)

        fill_type_sick = Keyboard.__create_button(Actions.A_FILL_TYPE_SICK, "Записать болезнь", params)
        markup.add(fill_type_sick)

        fill_type_presence = Keyboard.__create_button(Actions.A_FILL_TYPE_VACATION, "Записать отпуск", params)
        markup.add(fill_type_presence)

        if user.get_TS().check_absence(Constants.mission, user.get_chosen_date()):
            reset_mission = Keyboard.__create_button(Actions.A_RESET_MISSION, "Сбросить командировку", params)
            markup.add(reset_mission)
        else:
            choose_mission = Keyboard.__create_button(Actions.A_ACTIVE_MISSION, "Активировать командировку", params)
            markup.add(choose_mission)

        back_button = Keyboard.__create_button(Actions.A_MAIN_FILL, "Назад")
        markup.add(back_button)

        return markup

    @staticmethod
    def get_tasks_keyboard(user: User):
        markup = telebot.types.InlineKeyboardMarkup()

        params = {}

        task_list = user.get_TS().get_for_day(user.get_chosen_date())[Constants.task_list]

        for task in task_list:
            params[Constants.task_id] = task[Constants.task_id]
            params[Constants.cdate] = user.get_chosen_date()

            button_text = f"{task[Constants.proj_text]}.{task[Constants.task_text]} (Списано {task[Constants.chours]} часов)"

            button = Keyboard.__create_button(Actions.A_FILL_FOR_DATE, button_text, params)

            markup.add(button)

        button = Keyboard.__create_button(Actions.A_TO_START, "Перейти в главное меню")

        markup.add(button)

        return markup

    @staticmethod
    def get_action_keyboard():
        markup = telebot.types.InlineKeyboardMarkup()

        approve_button = Keyboard.__create_button(Actions.A_APPROVE, "Подтвердить изменения")
        markup.add(approve_button)

        reset_button = Keyboard.__create_button(Actions.A_RESET, "Отклонить изменения")
        markup.add(reset_button)

        continue_button = Keyboard.__create_button(Actions.A_MAIN_FILL, "Продолжить изменения")
        markup.add(continue_button)

        return markup

    @staticmethod
    def get_reset_keyboard(user):
        markup = telebot.types.InlineKeyboardMarkup()

        params = {}
        params[Constants.session_guid] = user.get_session()

        approve_button = Keyboard.__create_button(Actions.A_APPROVE_REQUEST, "Подтвердить сброс пароля", params)
        markup.add(approve_button)

        reset_button = Keyboard.__create_button(Actions.A_RESET_REQUEST, "Отклонить  сброс пароля", params)
        markup.add(reset_button)

        return markup

    @staticmethod
    def get_calendar(user: User):
        markup = telebot.types.InlineKeyboardMarkup()

        calendar = Calendar.get_calendar_by_chosen_date(user)

        week_buttons = []

        for i in range(1, 8):
            day = Calendar.get_day_by_num(i)
            button = Keyboard.__create_button(text=day)
            week_buttons.append(button)

        markup.row(*week_buttons)

        day_buttons = []

        for element in calendar:
            date = element.CDate
            day = date[6:8]

            if day == '00':
                button = Keyboard.__create_button(text=" ")
            else:

                params = {
                    Constants.cdate: date
                }
                button = Keyboard.__create_button(Actions.A_CALENDAR_ACTION, day, params)

            day_buttons.append(button)

            if element.WeekDayNumber == '7 ':
                markup.row(*day_buttons)
                day_buttons.clear()

        if len(day_buttons) != 0:
            markup.row(*day_buttons)
            day_buttons.clear()

        movement_buttons = []

        params = {
            Constants.movement: Constants.left
        }
        button = Keyboard.__create_button(Actions.A_FILL_ANOTHER_DAY, "<<", params)
        movement_buttons.append(button)

        params[Constants.movement] = Constants.right
        button = Keyboard.__create_button(Actions.A_FILL_ANOTHER_DAY, ">>", params)
        movement_buttons.append(button)

        markup.row(*movement_buttons)

        button = Keyboard.__create_button(Actions.A_TO_START, "Перейти в начало")
        markup.add(button)

        return markup

    @staticmethod
    def get_ways_keyboard(user: User):
        markup = telebot.types.InlineKeyboardMarkup()

        ways = user.get_ways()

        for way in ways:
            params = {
                Constants.way_id: way[Constants.way_id]
            }
            way_button = Keyboard.__create_button(Actions.A_CHOOSE_WAY, way[Constants.way_text], params)
            markup.add(way_button)

        back_button = Keyboard.__create_button(Actions.A_TO_START, "Перейти в начало")
        markup.add(back_button)

        return markup

    @staticmethod
    def get_system_keyboard(user: User):
        markup = telebot.types.InlineKeyboardMarkup()

        systems = user.get_systems()

        for system in systems:
            params = {
                Constants.full_info: system[Constants.full_info]
            }
            system_button = Keyboard.__create_button(Actions.A_CHOOSE_SYSTEM, system[Constants.full_info], params)
            markup.add(system_button)

        ways_button = Keyboard.__create_button(Actions.A_RESET_PASSWORD, "Изменить выбранный способ")
        markup.add(ways_button)

        back_button = Keyboard.__create_button(Actions.A_TO_START, "Перейти в начало")
        markup.add(back_button)

        return markup

    @staticmethod
    def get_reset_approve_keyboard(user: User):
        markup = telebot.types.InlineKeyboardMarkup()

        approve_button = Keyboard.__create_button(Actions.A_APPROVE_DROP, "Подтвердить сброс")
        markup.add(approve_button)

        change_button = Keyboard.__create_button(Actions.A_RESET_PASSWORD, "Изменить введённые данные")
        markup.add(change_button)

        start_button = Keyboard.__create_button(Actions.A_TO_START, "Вернуться в начало")
        markup.add(start_button)

        return markup
