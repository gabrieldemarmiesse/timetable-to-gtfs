import csv
import Other
from routes import Stop
from routes import Route
from calendar import Calendar
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
        self.calendar = "undefined calendar"
        self.count = 0

        # Here we do the initialization from the files
        self.init_from_file(folder_name)

    # Initialize here the agency and ask user for information if
    # There is something missing
    def init_from_file(self, path="gtfs"):
        path += "/agency.txt"
        issue = Other.read_cvs(path, self.init_from_line)
        if issue:
            print("No file found, please answer the following questions: ")
            self.init_from_line(["", "", "", "", "", "", "", "", "", ""])

    def init_from_line(self, line):
        for element in line:
            element.strip("\t ")

        if line[0] == "":
            self.id = input("The agency Id is missing, please provide it now: ")
        else:
            self.id = line[0]

        if line[1] == "":
            self.name = input("The agency name is missing, please provide it now: ")
        else:
            self.name = line[1]

        if line[2] == "":
            self.url = input("The agency url is missing, please provide it now: ")
        else:
            self.url = line[2]

        if line[3] == "":
            self.timezone = input("The agency timezone is missing, please provide it now: ")
        else:
            self.timezone = line[3]

        if line[4] == "":
            self.phone = input("The agency phone is missing, please provide it now: ")
        else:
            self.phone = line[4]

        if line[5] == "":
            self.language = input("The agency language is missing, please provide it now: ")
        else:
            self.language = line[5]

    def init_stops_from_file(self, path="gtfs"):
        path += "/stops.txt"

        issue = Other.read_cvs(path, self.add_stop)
        if issue:
            print("No stop.txt file")

        print(str(self.count) + " stops have been imported from the file")
        self.count = 0

    def add_stop(self, line):
        stop = Stop.Stop(line)
        self.stops.append(stop)
        self.count += 1

    def init_calendar(self):
        self.calendar = Calendar.Calendar()

    def init_routes_from_file(self, path="gtfs"):
        path += "/routes.txt"

        issue = Other.read_cvs(path, self.add_route)
        if issue:
            print("The file routes.txt was not found")
        print(str(self.count) + " routes were imported")
        self.count = 0

    def add_route(self, line):
        route = Route.Route(line)
        self.routes.append(route)
        self.count += 1

    def init_trips_from_file(self, folder_name="gtfs"):
        path = folder_name + "/trips.txt"
        try:
            with open(path, 'r') as csv_file:
                spam_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
                route_index = 0
                for i, row in enumerate(spam_reader):
                    if i == 0:
                        continue
                    while row[0] != self.routes[route_index].id:
                        route_index += 1
                    self.routes[route_index].add_trip(row)
                    self.count += 1
        except:
            print("The file " + path + " was not found")
        print(str(self.count) + " trips were imported")

    def init_times_stops_from_file(self, folder_name="gtfs"):
        path = folder_name + "/stop_times.txt"
        try:
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
                    self.count += 1
        except:
            print("The file " + path + " do not exist")
        print(str(self.count) + " times stops were imported")

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
                    route.add_trip_from_times(list_stops_names, times)
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
            elif re.match("^-$", element):
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
        # To add the folder gtfs to our program
        agency = cls()
        agency.init_stops_from_file()
        agency.init_calendar()
        agency.init_routes_from_file()
        agency.init_trips_from_file()
        agency.init_times_stops_from_file()

        return agency

    def update_coordinates(self):
        # Find updates in the coordinates

        # This is a list of triplet
        list_of_coordinates = self.read_coordinates()
        number_of_updated_stops = self.find_and_update(list_of_coordinates)
        print("we've updated " + number_of_updated_stops + "stop coordinates")

    def update_line(self):
        # Find updates in the lines
        print("updates line_something.txt")

    def update_times_stops(self):
        # Use the timetable to update
        print("read the timetable")

    def print(self):
        # Print everything into files to the gtfs folder
        print("write in gtfs folder")

    @staticmethod
    def update():
        agency = Agency.add_gtfs()
        print("\nImportation finished\n")

        agency.update_coordinates()
        print("\nupdate of coordinates finished\n")

        agency.update_line()
        print("\nUpdate of line finished")

        agency.update_times_stops()
        print("\nUpdate of times stops finished\n")

        agency.print()
