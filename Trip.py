import Other
import StopTime
class Trip:
    def __init__(self,line):
        self.id = "undefined id"
        self.service_id = "undefined service"
        self.route_id = "undefined route id"
        self.headsign = "undefined headsign"
        self.block_id = "undefined block id"
        self.stop_times = list()
        self.init_from_line(line)
        self.init_stop_times()


    #is used to create actually the trip
    def init_from_line(self,line):
        self.service_id = line[1]
        self.id = line[2]
        self.headsign = line[3]
        self.block_id = line[4]

    #initialize the stop times from a given path(gtfs by default)
    def init_stop_times(self,path= "gtfs"):
        path += "/stop_times.txt"
        Other.read_cvs(path,self.add_stop_time)

    def add_stop_time(self,line):
        if(line[0] == self.id):
            stop_time = StopTime.StopTime(line)
            self.stop_times.append(stop_time)

