import Other
from routes.graph import LinkedStops
from routes import Trip


class Route:
    def __init__(self, line, path="gtfs"):
        self.id = "undefined id"
        self.short_name = "undefined short name"
        self.long_name = "undefined long name"
        self.description = "undefined description"
        self.type = "undefined route type"
        self.trips = list()
        self.init_from_line(line)

    def init_from_line(self, line):
        self.id = line[0]
        self.short_name = line[1]
        self.long_name = line[2]
        self.description = line[3]
        self.type = line[4]

    def init_trips_from_file(self, path="gtfs"):
        path += "/trips.txt"
        Other.read_cvs(path, self.add_trip)

    def add_trip(self, line):
        print("trip" + line[2])
        trip = Trip.Trip.from_cvs(line)
        self.trips.append(trip)

    def add_trip_from_times(self,list_main_stops, list_times,service,path = "../gtfs/line.txt"):
        """Here we give a dictionary where the keys are stops and the values are times of stops"""

        graph = LinkedStops.LinkedStops()
        complete_stop_list = graph.find_complete_stops_list(list_main_stops)

        trip_id = len(self.trips)

        Trip.Trip.from_lists(trip_id, self.id, complete_stop_list, list_main_stops, list_times, service)
