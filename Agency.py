import csv

import Stop

import Other
from routes import Route


class Agency:
    """ Agency is the class that contains all the data
    This includes bus stops, stop times... etc"""

    def __init__(self, folder_name="gtfs"):
        self.id = "undefined id"
        self.name = "undefined name"
        self.url = "undefined url"
        self.timezone = "undefined timezone"
        self.phone = "undefined phone number"
        self.language = "undefined language"
        self.stops = list()
        self.routes = list()
        self.calendar  = "undefined calendar"

        # Here we do the initialization from the files
        self.init_from_file(folder_name)
        self.init_stops_from_file(folder_name)
        self.init_routes_from_file(folder_name)
        self.init_trips_from_file(folder_name)
        self.init_times_stops_from_file(folder_name)

    # Initialize here the agency and ask user for information if
    # There is something missing
    def init_from_file(self, path):
        path += "/agency.txt"
        Other.read_cvs(path, self.init_from_line)

    def init_stops_from_file(self, path):
        path += "/stops.txt"
        Other.read_cvs(path, self.add_stop)

    def add_stop(self, line):
        stop = Stop.Stop(line)
        self.stops.append(stop)
        print("added stop " + line[0])

    def init_routes_from_file(self, path):
        path += "/routes.txt"
        Other.read_cvs(path, self.add_route)

    def add_route(self, line):
        route = Route.Route(line)
        self.routes.append(route)
        print("creation route " + line[0])

    def init_trips_from_file(self, folder_name):
        path = folder_name + "/trips.txt"
        with open(path, 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            route_index = 0
            for i, row in enumerate(spam_reader):
                if i == 0:
                    continue
                while row[0] != self.routes[route_index].id:
                    route_index += 1
                self.routes[route_index].add_trip(row)

    def init_times_stops_from_file(self, folder_name):
        path = folder_name + "/stop_times.txt"
        with open(path, 'r') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            route_index = 0
            trip_index = 0
            for i, row in enumerate(spam_reader):
                if i == 0:
                    continue
                while row[0] != self.routes[route_index].trips[trip_index]:
                    trip_index += 1

                    if trip_index == len(self.routes[route_index].trips):
                        trip_index = 0
                        route_index += 1

                self.routes[route_index].trips[trip_index].add_stop_time(row)

    def init_from_line(self, line):
        self.id = line[0]
        self.name = line[1]
        self.url = line[2]
        self.timezone = line[3]
        self.phone = line[4]
        self.language = line[5]

