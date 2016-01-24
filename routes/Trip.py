import Other
from routes import StopTime


class Trip:
    def __init__(self, id, list_stops, list_main_stops, list_times,service, line=None):
        self.id = "undefined id"
        self.service_id = "undefined service"
        self.route_id = "undefined route id"
        self.headsign = "undefined headsign"
        self.block_id = "undefined block id"
        self.stop_times = list()
        if line is not None:
            self.init_from_line(line)
        else:
            self.init_from_lists(id, list_stops, list_main_stops, list_times,service)
        # self.init_stop_times()

    # Is used to create actually the trip
    def init_from_line(self, line):
        self.service_id = line[1]
        self.id = line[2]
        self.headsign = line[3]
        self.block_id = line[4]

    # Initialize the stop times from a given path(gtfs by default)
    def init_stop_times(self, path="gtfs"):
        path += "/stop_times.txt"
        Other.read_cvs(path, self.add_stop_time)

    def add_stop_time(self, line):
        if line[0] == self.id:
            stop_time = StopTime.StopTime(line)
            self.stop_times.append(stop_time)

    def init_from_lists(self, id, list_stops, list_main_stops, list_times,service):
        self.id = id
        self.route
        # TODO