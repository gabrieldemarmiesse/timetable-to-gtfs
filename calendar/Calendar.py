class Calendar:

    jour_ferie = list()

    def __init__(self):
        self.services = list()
        self.vacances = list()

    def init_services(self,path):
        path+="/calendar.txt"
        calendar_file = open(path,"r")
