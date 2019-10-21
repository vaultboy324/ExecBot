from datetime import datetime, date


class Utils:
    @staticmethod
    def from_pydate_to_sapdate(pydate):
        return pydate.strftime("%Y%m%d")

    @staticmethod
    def from_sapdate_to_pydate(sapdate):
        day = int(Utils.__get_day_from_sapdate(sapdate))
        month = int(Utils.__get_month_from_sapdate(sapdate))
        year = int(Utils.__get_year_from_sapdate(sapdate))
        return datetime(year, month, day)

    @staticmethod
    def get_output_date(date):
        day = int(Utils.__get_day_from_sapdate(date))
        month = int(Utils.__get_month_from_sapdate(date))
        year = int(Utils.__get_year_from_sapdate(date))

        return f"{day}/{month}/{year}"

    @staticmethod
    def __get_year_from_sapdate(date):
        return date[0:4]

    @staticmethod
    def __get_month_from_sapdate(date):
        return date[4:6]

    @staticmethod
    def __get_day_from_sapdate(date):
        return date[6:8]

    @staticmethod
    def get_month_by_chosen_date(date):
        month = Utils.__get_month_from_sapdate(date)

        if month == '01':
            return "Январь"
        elif month == '02':
            return "Февраль"
        elif month == '03':
            return "Март"
        elif month == '04':
            return "Апрель"
        elif month == '05':
            return "Май"
        elif month == '06':
            return "Июнь"
        elif month == '07':
            return "Июль"
        elif month == '08':
            return "Август"
        elif month == '09':
            return "Сентябрь"
        elif month == '10':
            return "Октябрь"
        elif month == '11':
            return "Ноябрь"
        elif month == '12':
            return "Декабрь"
        else:
            return None