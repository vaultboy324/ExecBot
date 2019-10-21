from helper.crypt_helper import Crypt_helper

from config import Statuses

from datetime import datetime, timedelta
import calendar

from Constants import Constants

from modules.Utils import Utils

from entities.TS import TS


class User:
    def __init__(self, id):
        self.set_id(id)
        self.set_uname("")
        self.set_role("")
        self.set_status(Statuses.S_ENTER_UNAME)
        self.set_task_list([])
        self.set_session(None)
        self.set_client(None)
        self.set_chosen_date(datetime.now())
        self.set_current_task({})

        timesheet = TS()
        self.set_TS(timesheet)

        self.set_reset_request({})

        pass

    def set_id(self, id):
        self.__id = id
        pass

    def set_uname(self, uname):
        self.__uname = uname
        pass

    def set_initial_password(self):
        self.__password = ""

    def set_password(self, password):
        self.__password = password
        pass

    def set_crypt_password(self, crypt_password):
        self.__password = crypt_password
        pass

    def set_status(self, status):
        self.__status = status

    def set_tabnr(self, tabnr):
        self.__tabnr = tabnr

    def set_current_task(self, current_task):
        self.__current_task = current_task

    def set_task_list(self, task_list):
        self.__task_list = task_list

    def set_current_day(self, current_day):
        self.__current_day = current_day

    def set_time_in_task(self, time):
        current_task = self.__find_task_in_list()
        current_task[Constants.chours] = str(time)

    def set_client(self, client):
        self.__client = client

    def set_TS(self, TS: TS):
        self.__TS = TS

    def set_chosen_date(self, chosen_date):
        if type(chosen_date) != str:
            self.__chosen_date = Utils.from_pydate_to_sapdate(chosen_date)
        else:
            self.__chosen_date = chosen_date

    def set_next_month(self):
        chosen_date = self.get_chosen_date()
        pydate = Utils.from_sapdate_to_pydate(chosen_date)
        days_in_month = calendar.monthrange(pydate.year, pydate.month)[1]

        new_date = pydate + timedelta(days=days_in_month)
        self.set_chosen_date(Utils.from_pydate_to_sapdate(new_date))

    def set_prev_month(self):
        chosen_date = self.get_chosen_date()
        pydate = Utils.from_sapdate_to_pydate(chosen_date)

        first_day = pydate.replace(day=1)
        # days_in_month = calendar.monthrange(pydate.year, pydate.month)[1]

        # new_date = pydate - timedelta(days=days_in_month)
        new_date = first_day - timedelta(days=1)
        self.set_chosen_date(Utils.from_pydate_to_sapdate(new_date))

    def set_session(self, session):
        self.__session = session

    def set_systems(self, systems):
        self.__systems = systems

    def set_ways(self, ways):
        self.__ways = ways

    def set_reset_request(self, request):
        self.__request = request

    def get_id(self):
        return self.__id

    def get_uname(self):
        return self.__uname

    def get_password(self):
        return self.__password

    def get_status(self):
        return self.__status

    def get_tabnr(self):
        return self.__tabnr

    def get_current_day(self):
        return self.__current_day

    def get_last_message(self):
        return self.__last_message

    def get_reset_request(self):
        return self.__request

    def get_request_text(self):
        result = ''

        if self.__request.get(Constants.way_id):
            way = self.__request.get(Constants.way_id)
            if way == Constants.email_reset:
                output_text = "Отправка подтверждения на почту\n"
            elif way == Constants.telegram_reset:
                output_text = "Отправка подтверждения в telegram\n"
            else:
                output_text = '\n'

            result += f"Выбранный способ сброса пароля: {output_text}"

        if self.__request.get(Constants.full_info):
            system = self.__request.get(Constants.full_info)
            result += f"Выбранная система: {system}"

        result += "\n\n\n"

        return result

    def create_new_user(self, id):
        self.set_id(id)
        self.set_uname("")
        self.set_status(Statuses.S_ENTER_UNAME)
        self.set_task_list([])
        pass

    def create_user_by_response(self, sap_user):
        self.set_uname(sap_user[0][1])
        self.__password = sap_user[0][2]
        self.__tabnr = sap_user[0][3]
        self.set_status(Statuses.S_READY_USER)

    def get_encode_password(self):
        return self.__decrypt(self.__password).decode()

    def set_role(self, role):
        self.__role = role
        pass

    def get_role(self):
        return self.__role

    def get_current_task(self):
        return self.__current_task

    def get_task_list(self):
        return self.__task_list

    def get_session(self):
        return self.__session

    def get_client(self):
        return self.__client

    def get_chosen_date(self):
        return self.__chosen_date

    def get_TS(self):
        return self.__TS

    def get_systems(self):
        return self.__systems

    def get_ways(self):
        return self.__ways

    def add_task_to_list(self, task):
        self.__task_list.append(task)

    def clear_tasks(self):
        self.set_current_day(None)
        self.set_current_task(None)
        self.set_task_list([])

    def clear(self):
        id = self.get_id()
        self.__init__(id)


    def check_task(self):
        return self.__current_task.get(Constants.task_id)

    def __encrypt(self, string):
        key = Crypt_helper.get_hash_key()
        code_string = Crypt_helper.encrypt_string(string.encode(), key.encode())
        return code_string.decode()

    def __decrypt(self, string):
        key = Crypt_helper.get_hash_key()
        encode_string = Crypt_helper.decrypt_string(string.encode(), key.encode())
        return encode_string

    def __find_task_in_list(self):
        for task in self.__task_list:
            if task[Constants.task_id] == self.get_current_task() and task[Constants.cdate] == self.get_current_day():
                return task