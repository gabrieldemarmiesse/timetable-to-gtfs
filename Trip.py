class Trip:
    def __init__(self,line):
        self.id = "undefined id"
        self.service = "undefined service"
        self.route_id = "undefined route id"
        self.headsign = "undefined headsign"
        self.block_id = "undefined block id"
        self.stop_times = list()
        self.init_from_line(line)
        self.init_stop_times()


    #is used to create actually the trip
    def init_from_line(self,line):
        a=3

    #initialize the stop times from a given path(gtfs by default)
    def init_stop_times(self,path= "gtfs"):
        path += "/stop_times.txt"
        stop_times_file = open(path,"r")
