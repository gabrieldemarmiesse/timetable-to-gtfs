import Other
from routes.graph import LinkedStops
from routes import Trip


def reduct(list_main_stops, list_times):
    # This function delete the empty times and the stops corresponding
    l = len(list_main_stops)
    new_list_stops = list()
    new_list_times = list()
    for i, time in enumerate(list_times):
        if time is not None:
            new_list_stops.append(list_main_stops[i])
            new_list_times.append(time)

    return new_list_stops, new_list_times


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

    def get_first_line_csv(self):
        return "route_id,route_short_name,route_long_name,route_desc,route_type"

    def to_list(self):
        elements_list = list()
        elements_list.append(self.id)
        elements_list.append(self.short_name)
        elements_list.append(self.long_name)
        elements_list.append(self.description)
        elements_list.append(self.type)
        return elements_list

    @staticmethod
    def get_first_csv_line():
        return "route_id,route_short_name,route_long_name,route_desc,route_type\n"

    def init_trips_from_file(self, path="gtfs"):
        path += "/trips.txt"
        Other.read_csv(path, self.add_trip)

    def add_trip(self, line):
        trip = Trip.Trip.from_csv(line)
        self.trips.append(trip)

    def number_trips_from_service(self, service_id):
        # Get the number of trips with this service Id
        count = 0
        for trip in self.trips:
            if trip.service_id == service_id:
                count += 1
        return count

    def add_trip_from_times(self, list_main_stops, list_times, service, path = "../gtfs/line.txt"):

        # Here we must delete the stops where the time is None
        list_main_stops_reducted, list_times_reducted = reduct(list_main_stops, list_times)

        complete_stop_list = self.graph.find_complete_stops_list(list_main_stops_reducted)

        complete_stop_list_without_false_stops = [x for x in complete_stop_list if x[0] != "$"]

        # The trip_id will be "route Id_service Id_trip number"
        trip_number = self.number_trips_from_service(service) + 1

        trip_id = self.id + "_" + service + "_" + str(trip_number)

        trip = Trip.Trip.from_lists(trip_id, self.id, complete_stop_list_without_false_stops, list_main_stops_reducted, list_times_reducted, service)

        self.trips.append(trip)

    def get_dictionnary_of_services(self):
        # This dictionary contain services Ids as key and the number of trips with this service Id as argument.
        dictionary = dict()
        for trip in self.trips:
            try:
                dictionary[trip.service_id] += 1
            except KeyError:
                dictionary[trip.service_id] = 1

        return dictionary