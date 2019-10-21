

class Task:
    def __init__(self, date, tabnr):
        self.set_task_id("")
        self.set_date(date)
        self.set_hours(None)
        self.set_tabnr(tabnr)
        self.set_role_id("")
        self.set_presence(False)
        self.set_vacation(False)
        self.set_mission(False)
        self.set_sick(False)
        self.set_update(True)

    def set_task_id(self, TaskId):
        self.__id = TaskId

    def set_date(self, date):
        self.__date = date

    def set_hours(self, hours):
        self.__hours = hours

    def set_tabnr(self, tabnr):
        self.__tabnr = tabnr

    def set_role_id(self, role_id):
        self.__role_id = role_id

    def set_presence(self, presence):
        self.__presence = presence

    def set_vacation(self, vacation):
        self.__vacation = vacation

    def set_sick(self, sick):
        self.__sick = sick

    def set_mission(self, mission):
        self.__mission = mission

    def set_update(self, update):
        self.__update = update

    def get_task_id(self):
        return self.__id

    def get_date(self):
        return self.__date

    def get_hours(self):
        return self.__hours

    def get_tabnr(self):
        return self.__tabnr

    def get_role_id(self):
        return self.__role_id

    def get_presence(self):
        return self.__presence

    def get_vacation(self):
        return self.__vacation

    def get_sick(self):
        return self.__sick

    def get_mission(self):
        return self.__mission

    def get_update(self):
        return self.__update

    def to_dict(self):
        task = {
            "TaskId": self.get_task_id(),
            "Cdate": self.get_date(),
            "TabNr": self.get_tabnr(),
            "Presence": self.get_presence(),
            "Vacation": self.get_vacation(),
            "Sick": self.get_sick(),
            "Mission": self.get_mission(),
            "Update": self.get_update(),
            "RoleId": self.get_role_id()
        }

        hours = self.get_hours()

        if hours:
            task["Chours"] = hours

        return task

    def from_dict(self, dict: dict):
        self.set_task_id(dict["TaskId"])
        self.set_date(dict["Cdate"])
        self.set_tabnr(dict["TabNr"])
        self.set_presence(dict["Presence"])
        self.set_vacation(dict["Vacation"])
        self.set_sick(dict["Sick"])
        self.set_mission(dict["Mission"])
        self.set_update(dict["Update"])
        self.set_role_id(dict["RoleId"])

        if dict.get("Chours"):
            self.set_hours(dict["Chours"])

    def from_odata_entity(self, entity):
        self.set_task_id(entity.TaskId)
        self.set_tabnr(entity.TabNr)
        self.set_date(entity.Cdate)
        self.set_hours(entity.Chours)
        self.set_presence(entity.Presence)
        self.set_vacation(entity.Vacation)
        self.set_mission(entity.Mission)
        self.set_sick(entity.Sick)
        self.set_update(entity.Update)
        self.set_role_id(entity.RoleId)