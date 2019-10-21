from Constants import Constants

from config import Actions as ActionEnum

from modules.Utils import Utils

import locale
import json

from Error.TimeError import TimeError
from Error.TelegramBotError import TelegramBotError


class TS:
    __TS = {}

    def __init__(self):
        __TS = {}

    @staticmethod
    def get_node_from_ep(telegram_id, task_list, date):
        result = []

        for task in task_list:
            node = {
                Constants.telegram_id: str(telegram_id),
                Constants.task_id: task.TaskId,
                Constants.cdate: date,
                Constants.role_id: task.RoleId,
                Constants.mission: task.Mission,
                Constants.sick: task.Sick,
                Constants.vacation: task.Vacation,
                Constants.presence: task.Presence,
                Constants.update: True,
                Constants.chours: task.CHours,
                Constants.proj_text: task.ProjText,
                Constants.task_text: task.TaskText
            }
            result.append(node)

        return result

    @staticmethod
    def __get_task_index_by_id(id, tasks: list):
        size = len(tasks)

        for i in range(0, size):
            if tasks[i][Constants.task_id] == id:
                return i

    @staticmethod
    def __rewrite_tasks(old_tasks: list, new_tasks: list):
        last_comp = -1

        size_old = len(old_tasks)
        size_new = len(new_tasks)

        for i in range(0, size_old - 1):
            for j in range(last_comp + 1, size_new - 1):
                if old_tasks[i][Constants.task_id] == new_tasks[j][Constants.task_id]:
                    new_tasks[j][Constants.chours] = old_tasks[i][Constants.chours]
                    new_tasks[j][Constants.vacation] = old_tasks[i][Constants.vacation]
                    new_tasks[j][Constants.sick] = old_tasks[i][Constants.sick]
                    new_tasks[j][Constants.mission] = old_tasks[i][Constants.mission]
                    new_tasks[j][Constants.update] = True
                    last_comp = j
                    break

    def check_mission(self, date):
        tasks = self.get_for_day(date)[Constants.task_list]
        return tasks[0][Constants.mission]

    def update(self, telegram_id, day, new_tasks: list):

        new_tasks = self.get_node_from_ep(telegram_id, new_tasks, day)

        if len(new_tasks) == 0:
            raise TelegramBotError("Отсутствуют задачи", "null_task")

        if self.check_day(day):
            old_tasks = self.__TS[day][Constants.task_list]
            self.__rewrite_tasks(old_tasks, new_tasks)
        else:

            absence = json.loads(json.dumps(new_tasks[0]))
            absence[Constants.chours] = '0'
            absence[Constants.role_id] = ''

            self.__TS[day] = {
                Constants.task_list: [],
                Constants.absence: absence
            }

        for task in new_tasks:
            if task[Constants.chours] == '':
                task[Constants.chours] = '0'

        self.__TS[day][Constants.task_list] = new_tasks

        if self.check_absence(Constants.sick, day) or self.check_absence(Constants.vacation, day):
            self.__TS[day][Constants.task_list][0][Constants.chours] = '0'

    def get_sum_hours_for_day(self, day):
        sum = 0

        tasks = self.get_for_day(day)[Constants.task_list]

        try:
            for task in tasks:
                sum += float(task[Constants.chours])
        except ValueError:
            args = {
                "Введите число"
            }
            raise ValueError(*args)

        return sum

    def change_time_in_task(self, day, taskid, time):
        tasks = self.get_for_day(day)[Constants.task_list]

        index = self.__get_task_index_by_id(taskid, tasks)

        cashed_time = tasks[index][Constants.chours]
        tasks[index][Constants.chours] = time
        tasks[index][Constants.presence] = True

        try:
            if self.get_sum_hours_for_day(day) > 21:
                tasks[index][Constants.chours] = cashed_time
                raise TimeError('bad_time', 'Суммарное время не может быть больше 21 часа. Введите корректное время!')
        except ValueError as e:
            raise e

    def write_absence(self, day, operation_type):
        node = self.get_for_day(day)

        # node[Constants.absence] = json.loads(json.dumps(node[Constants.task_list][0]))
        node[Constants.absence][Constants.task_id] = ''
        node[Constants.absence][Constants.presence] = False
        node[Constants.absence][Constants.update] = True
        node[Constants.absence][Constants.chours] = Constants.base_time
        if node[Constants.absence].get(Constants.role_id):
            node[Constants.absence].pop(Constants.role_id)

        if operation_type == ActionEnum.A_FILL_TYPE_SICK:
            node[Constants.absence][Constants.sick] = True
        elif operation_type == ActionEnum.A_FILL_TYPE_VACATION:
            node[Constants.absence][Constants.vacation] = True
        elif operation_type == ActionEnum.A_ACTIVE_MISSION:
            node[Constants.absence][Constants.mission] = True

    def get_string_status(self):
        result = ''

        for date in self.__TS:
            filled_flag = self.check_filled_day(date)

            if not filled_flag:
                continue

            result += self.get_string_status_for_date(date)

        return result

    def get_string_status_for_date(self, date):
        result = ""

        output_date = Utils.get_output_date(date)

        result += f"Данные за {output_date}\n"

        if self.check_absence(Constants.sick, date):
            result += f"За этот день выбрана болезнь\n\n"
            return result
        elif self.check_absence(Constants.vacation, date):
            result += f"За этот день выбран отпуск\n\n"
            return result
        elif self.check_absence(Constants.mission, date):
            result += f"За за этот день выбрана командировка\n\n"

        result += "Информация по задачам:\n"

        tasks_for_day = self.__TS[date][Constants.task_list]

        for task in tasks_for_day:
            result += f"На задачу {task[Constants.proj_text]}.{task[Constants.task_text]} записано {task[Constants.chours]} часов \n"

        result += "\n\n"

        return result

    def check_absence(self, absence_type, date):
        node = self.get_for_day(date)
        if node.get(Constants.absence):
            return node[Constants.absence][absence_type]
        return None

    def reset_absence(self, absence_type, date):
        node = self.get_for_day(date)
        node[Constants.absence][absence_type] = False
        # node[Constants.absence][Constants.chours] = '0'

    def reset_mission_node(self, date):
        node = self.get_for_day(date)
        # node[Constants.absence][Constants.chours] = '0'
        # node[Constants.absence][Constants.mission] = False
        self.reset_absence(Constants.mission, date)

    def drop_absence(self, date):
        node = self.get_for_day(date)
        node[Constants.absence] = None

    def absence_to_list(self):
        result_list = []

        for date in self.__TS:
            absence = json.loads(json.dumps(self.__TS[date][Constants.absence]))
            absence.pop(Constants.task_id)
            absence.pop(Constants.task_text)
            absence.pop(Constants.proj_text)

            # if self.check_absence(Constants.mission, date):
            #     absence.pop(Constants.sick)
            #     absence.pop(Constants.vacation)
            #
            # if self.check_absence(Constants.vacation, date):
            #     absence.pop(Constants.sick)
            #     absence.pop(Constants.mission)
            #
            # if self.check_absence(Constants.sick, date):
            #     absence.pop(Constants.vacation)
            #     absence.pop(Constants.mission)

            result_list.append(absence)

        return result_list

    def to_task_list(self):
        result_list = []

        for date in self.__TS:
            if self.check_absence(Constants.sick, date) or self.check_absence(Constants.vacation, date):
                task_list = self.__TS[date][Constants.task_list]
                for task in task_list:
                    result_list.append(task)
            else:
                continue
            # flag = self.check_sick(date) or self.check_vacation(date)
            # for task in task_list:
            #     result_list.append(task)
            #     if flag:
            #         break

        return result_list

    def to_empty_time_list(self):
        result_list = self.to_task_list()

        for task in result_list:
            task[Constants.chours] = '0'

        return result_list

    def check_any_absence(self, date):
        if self.check_absence(Constants.sick, date) or \
                self.check_absence(Constants.mission, date) or \
                self.check_absence(Constants.vacation, date):
            return True
        return False

    def check_filled_day(self, date):
        # if self.check_absence(Constants.sick, date) or \
        #         self.check_absence(Constants.mission, date) or \
        #         self.check_absence(Constants.vacation, date):
        #     return True

        if self.check_any_absence(date):
            return True

        sum = self.get_sum_hours_for_day(date)

        if sum != 0:
            return True
        return False

    def check_day(self, day):
        if self.__TS.get(day):
            return True
        return False

    def get_for_day(self, day):
        return self.__TS[day]

    def get(self):
        return self.__TS

    def clear(self):
        self.__TS = {}