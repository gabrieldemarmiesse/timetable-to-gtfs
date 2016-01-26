import csv
import Other
from routes import Stop
from routes import Route
import re

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

    def add_timetable(self, file_path="gtfs/timetable.txt"):
        # This function takes a timetable and convert it to a list of trips

        with open(file_path) as f:
            lines = f.readlines()
        for line in lines:
            line.strip()

        # Here we get the name of the line and the service
        first_line = lines[0]
        first_line = first_line.split('\t')
        first_line_splitted = [x for x in first_line if x != '']
        route_name = first_line_splitted[0]
        trips_service = first_line_splitted[1]

        lines.pop(0)
        list_stops_names = list()
        list_times = list()
        for line in lines:
            name, times_list = Agency.get_list_of_times_and_stop_name(line)
            list_stops_names.append(name)
            list_times.append(times_list)

        # Right now, we have a table of horizontal lines.
        # We have to get vertical lines instead.

        # Transposed is the transposition of the table list_times
        transposed = list(map(list, zip(*list_times)))

        # Now we find the bus line in memory
        for route in self.routes:
            if route.id == route_name:
                for times in transposed:
                    route.add_trip_from_times(list_stops_names,times)
                break
    @staticmethod
    def get_list_of_times_and_stop_name(line, separator=None, empty_time='-', sep_hours_minutes=':'):
        # This function parse a line of the timetable, it returns
        # the name of the stop and the list of stop times

        if separator is None:
            contents = line.split()
        else:
            contents = line.split(separator)

        regex = "^([0-9]|[0-9][0-9])" + sep_hours_minutes + "[0-9][0-9]$"

        reverse_stop_name = list()
        times_list = list()
        for element in reversed(contents):
            if re.match(regex, element):
                times_list.append(element)
            elif re.match("^-$",element):
                times_list.append(None)
            else:
                # It means we got to the name of the stop
                reverse_stop_name.append(element)

        times_list = reversed(times_list)
        stop_name = reversed(reverse_stop_name)
        name = ' '.join(stop_name)

        return name, times_list

    @classmethod
    def add_gtfs(cls):
        print("Add gtfs folder data to our program")
        return cls("something")

    def update_coordinates(self):
        print("Adding gps coordinates")

    def update_line(self):
        print("updates line_something.txt")
        
    def update_times_stops(self):
        print("read the timetable")

    def print(self):
        print("write in gtfs folder")

    @staticmethod
    def update():
        agency = Agency.add_gtfs()
        agency.update_coordinates()
        agency.update_line()
        agency.update_times_stops()
        agency.print()



