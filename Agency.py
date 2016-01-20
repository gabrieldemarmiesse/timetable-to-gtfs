class Agency:
    def __init__(self, foldername ="gtfs"):
        self.id = "undefined id"
        self.name = "undefined name"
        self.url = "undefined url"
        self.timezone = "undefined timezone"
        self.phone = "undefined phone number"
        self.language = "undefined language"
        self.stops = list()
        self.routes = list()

        #here we do the initialization from the files
        self.init_from_file(foldername)
        self.init_stops_from_file(foldername)
        self.init_routes_from_file(foldername)


    #initialize here the agency and ask user for infos if
    #there is something missing

    def init_from_file(self,path):
        path += "/agency.txt"
        agency_file = open(path,"r")

    def init_stops_from_file(self,path):
        path += "/stops.txt"
        stops_file = open(path,"r")

    def init_routes_from_file(self,path):
        path += "/routes.txt"
        routes_file = open(path,"r")