import Other
from calendar import Calendar
from routes import StopTime


class Trip:
    def __init__(self, trip_id, service_id, route_id, headsign="", block_id="", stop_times=None):
        self.trip_id = trip_id
        self.service_id = service_id
        self.route_id = route_id
        self.headsign = headsign
        self.block_id = block_id

        if stop_times is None:
            self.stop_times = list()
        else:
            self.stop_times = stop_times

    def __lt__(self, other):

        dictionary = Calendar.Calendar.get_dictionary()

        if self.service_id == other.service_id:

            try:
                self1 = int(self.stop_times[0].arrival_time.split(":")[0])*60 + int(self.stop_times[0].arrival_time.split(":")[1])
                other1 = int(other.stop_times[0].arrival_time.split(":")[0])*60 + int(other.stop_times[0].arrival_time.split(":")[1])
            except:
                print(self.stop_times[0].arrival_time)
                print(other.stop_times[0].arrival_time)
            return self1 < other1
        else:
            return dictionary[self.service_id] < dictionary[other.service_id]

    # Two constructor overloads
    @classmethod
    def from_csv(cls, line):
        """ Create an Trip object from a parsed csv line
        :param line: parsed csv line
        :return: A Trip object without the stop_times
        """

        return cls(line[2], line[1], line[0], line[3], line[4])

    @classmethod
    def from_lists(cls, trip_id, route_id, list_stops, list_main_stops, list_times, service_id):
        """
        This constructor give a Trip based on the elements
        from the graph and a column from the timetable
        :param route_id: The route Id
        :param trip_id: The trip Id
        :param list_stops: Full list of stops
        :param list_main_stops: List of the stops on which we have the times
        :param list_times: Times associated with the main stops
        :param service_id: The service Id
        :return: A Trip object with the stop_times filled
        """
        stop_times = list()
        for stop_sequence, stop in enumerate(list_stops):
            arrival_time = ""
            # Here we check if there is a time associated to this stop
            for i, main_stop in enumerate(list_main_stops):
                if stop == main_stop:
                    arrival_time = list_times[i]
                    break
            stop_id2 = stop.replace(" ", "")
            stop_id1 = stop_id2.replace(".", "")
            stop_id3 = stop_id1.replace("'", "")
            stop_id = stop_id3.replace("-", "")
            stop_times.append(StopTime.StopTime(trip_id, stop_id.lower(), stop_sequence, arrival_time))

        return cls(trip_id, service_id, route_id, stop_times=stop_times)

    def to_list(self):
        return [self.route_id, self.service_id, self.trip_id,self.headsign, self.block_id]

    def get_first_line_csv(self):
        return "route_id,service_id,trip_id,trip_headsign,block_id"

    # Initialize the stop times from a given path(gtfs by default)
    def init_stop_times(self, path="gtfs"):
        path += "/stop_times.txt"
        Other.read_csv(path, self.add_stop_time)

    def add_stop_time(self, line):
        if line[0] == self.trip_id:
            stop_time = StopTime.StopTime.init_from_line(line)
            self.stop_times.append(stop_time)
