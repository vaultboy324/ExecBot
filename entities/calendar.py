from entities.user import User
from datetime import datetime, timedelta

from entities.odata_requests import ODataRequests


class Calendar:

    @staticmethod
    def from_pydate_to_sapdate(day):
        return day.strftime("%Y%m%d")

    @staticmethod
    def check_holiday(user: User):
        day = Calendar.from_pydate_to_sapdate(datetime.today())
        return ODataRequests.check_holiday(user, day)

    @staticmethod
    def get_user_time(user: User):
        day = Calendar.from_pydate_to_sapdate(datetime.today())
        return ODataRequests.get_user_time(user, day)

    @staticmethod
    def get_calendar_by_chosen_date(user: User):
        date = user.get_chosen_date()
        return ODataRequests.get_calendar(user)

    @staticmethod
    def get_month_by_chosen_date(user: User):
        month = user.get_chosen_date().month
        if month == 1:
            return "Январь"
        elif month == 2:
            return "Февраль"
        elif month == 3:
            return "Март"
        elif month == 4:
            return "Апрель"
        elif month == 5:
            return "Май"
        elif month == 6:
            return "Июнь"
        elif month == 7:
            return "Июль"
        elif month == 8:
            return "Август"
        elif month == 9:
            return "Сентябрь"
        elif month == 10:
            return "Октябрь"
        elif month == 11:
            return "Ноябрь"
        elif month == 12:
            return "Декабрь"
        else:
            return None

    @staticmethod
    def get_day_by_num(num):
        if num == 1:
            return "Пн"
        elif num == 2:
            return "Вт"
        elif num == 3:
            return "Ср"
        elif num == 4:
            return "Чт"
        elif num == 5:
            return "Пт"
        elif num == 6:
            return "Сб"
        elif num == 7:
            return "Вс"
        else:
            return None

    @staticmethod
    def get_year_by_chosen_date(user: User):
        return user.get_chosen_date().year