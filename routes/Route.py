import Other
from routes.graph import LinkedStops
from routes import Trip


class Route:
    # A route correspond to a bus line

    def __init__(self, route_id, long_name, short_name=None, type="3", description="", trips=None):
        self.id = route_id

        if short_name is None:
            self.short_name = route_id
        else:
            self.short_name = short_name

        self.long_name = long_name
        self.description = description
        self.type = type

        if trips is None:
            self.trips = list()
        else:
            self.trips = trips

        self.graph = None

    @classmethod
    def from_csv(cls, line):
        """Create an Route from a csv line
        :param line: A parsed csv line
        :return: A Route object
        """
        return cls(line[0], line[2], line[1], line[4], line[3])

    @classmethod
    def from_stops_list(cls, route_name, list_stops_names):
        # Create a route from the list of main stops

        lenght = len(list_stops_names)
        long_name = list_stops_names[0] + " - " + list_stops_names[lenght - 1]
        return cls(route_name, long_name)

    def __lt__(self, other):
        return self.id < other.id

    def init_from_line(self, line):
        self.id = line[0]
        self.short_name = line[1]
        self.long_name = line[2]
        self.description = line[3]
        self.type = line[4]

    def to_list(self):
        elements_list = list()
        elements_list.append(self.id)
        elements_list.append(self.short_name)
        elements_list.append(self.long_name)
        elements_list.append(self.description)
        elements_list.append(self.type)
        return elements_list

    def init_graph(self):
        self.graph = LinkedStops.LinkedStops(self.id)
        return self.graph.list_stops_of_graph_list

    @staticmethod
    def get_first_csv_line():
        return "route_id,route_short_name,route_long_name,route_desc,route_type\n"

    def init_trips_from_file(self, path="gtfs"):
        path += "/trips.txt"
        Other.read_csv(path, self.add_trip)

    def add_trip(self, line):
        print("trip" + line[2])
        trip = Trip.Trip.from_csv(line)
        self.trips.append(trip)

    def add_trip_from_times(self, list_main_stops, list_times, service, path = "../gtfs/line.txt"):

        complete_stop_list = self.graph.find_complete_stops_list(list_main_stops)

        trip_id = len(self.trips)

        Trip.Trip.from_lists(trip_id, self.id, complete_stop_list, list_main_stops, list_times, service)

