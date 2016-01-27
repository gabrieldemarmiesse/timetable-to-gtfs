from calendar import Service


class Calendar:
    jour_ferie = list()

    def __init__(self):
        self.services = list()
        self.services.append(Service.Service("W", [1, 1, 1, 1, 1, 0, 0], 20160101, 20180101))
        self.services.append(Service.Service("WS", [1, 1, 1, 1, 1, 1, 0], 20160101, 20180101))
        self.services.append(Service.Service("WSD", [1, 1, 1, 1, 1, 1, 1], 20160101, 20180101))
        self.services.append(Service.Service("S", [0, 0, 0, 0, 0, 1, 0], 20160101, 20180101))
        self.services.append(Service.Service("D", [0, 0, 0, 0, 0, 0, 1], 20160101, 20180101))
        self.services.append(Service.Service("SD", [0, 0, 0, 0, 0, 1, 1], 20160101, 20180101))
        self.services.append(Service.Service("SDV", [0, 0, 0, 0, 0, 1, 1], 20160101, 20180101))
        self.services.append(Service.Service("DV", [0, 0, 0, 0, 0, 0, 1], 20160101, 20180101))

        self.holidays = list()
        self.public_holiday = list()
        self.calendar_dates = list()

    def init_services(self, path):
        path += "/calendar.txt"
        calendar_file = open(path, "r")

    @staticmethod
    def get_dictionary():
        dictionary = { "W"  : 1,
                       "WS" : 2,
                       "WSD": 3,
                       "S"  : 4,
                       "D"  : 5,
                       "SD" : 6,
                       "DV" : 7}
        return dictionary
