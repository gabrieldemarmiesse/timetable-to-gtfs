
import csv
import Other
import os
from routes import Stop
from routes import Route
from calendar import Calendar
import re


def read_coordinates():
    try:
        with open("sgtfs/coordinates.txt", 'r') as file:
            lines = file.readlines()

        stop_counter = 0
        coordinates_counter = 0

        list_of_coordinates = list()
        for line in lines:
            stop_counter += 1

            # Here we parse the line
            stop = line.strip("\t \n").split("\t")
            parsed_line = [x for x in stop if x != '']

            # We add it to the list if it contains coordinates
            if len(parsed_line) > 1:

                # Parsing the coordinates
                coordinates = parsed_line[1].split(",")
                coo0 = coordinates[0].strip()
                coo1 = coordinates[1].strip()

                list_of_coordinates.append([parsed_line[0], coo0, coo1])
                coordinates_counter += 1

        print(str(stop_counter) + " stops were in the file")
        print(str(coordinates_counter) + " coordinates were in the file")
        return list_of_coordinates

    except:
        print("There is no sgtfs/coordinates.txt file")


def read_line_sgtfs(filename):
    """
    :param filename: The name of the file in the sgtfs folder
    :return: A list of lines stripped of \n
    """
    path = "sgtfs/" + filename
    try:
        with open(path) as f:
            lines = f.readlines()

    except FileNotFoundError:
        return ["", ]

    else:
        other_list = list()
        for line in lines:
            other_list.append(line.strip())
        return other_list


def get_name(new_line):
    # Get the name of the line
    return new_line[0]


def create_line_file(name):
    path = "sgtfs/" + name
    open(path, 'a').close()


def write(new_line, filename):
    # Write the lines of the list in the file called filename
    path = "sgtfs/" + filename
    line_file = open(path, "w")
    for line in new_line:
        line_file.write(line + "\n")


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
        self.calendar = Calendar.Calendar()
        self.count = 0

        # Here we do the initialization from the files
        self.init_from_file(folder_name)

    def get_first_line_csv(self):
        return "agency_id, agency_name,agency_url,agency_timezone,agency_phone,agency_lang"
    # Initialize here the agency and ask user for information if
    # There is something missing
    def init_from_file(self, path="gtfs"):
        path += "/agency.txt"
        issue = Other.read_csv(path, self.init_from_line)
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

    def to_list(self):
        agency_list = list()
        agency_list.append(self.id)
        agency_list.append(self.name)
        agency_list.append(self.url)
        agency_list.append(self.timezone)
        agency_list.append(self.phone)
        agency_list.append(self.language)
        return agency_list

    @staticmethod
    def get_first_csv_line():
        return "agency_id, agency_name,agency_url,agency_timezone,agency_phone,agency_lang\n"

    def init_stops_from_file(self, path="gtfs"):
        path += "/stops.txt"

        issue = Other.read_csv(path, self.add_stop)
        if issue:
            print("No stop.txt file")

        print(str(self.count) + " stops have been imported from the file")
        self.count = 0

    def add_stop(self, line):
        stop = Stop.Stop.init_from_line(line)
        self.stops.append(stop)
        self.count += 1

    def init_routes_from_file(self, path="gtfs"):
        path += "/routes.txt"

        issue = Other.read_csv(path, self.add_route)
        if issue:
            print("The file routes.txt was not found")
        print(str(self.count) + " routes were imported")
        self.count = 0

    def add_route(self, line):
        route = Route.Route.from_csv(line)
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
        self.count = 0

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

                    # We try to find the trip which have this trip Id
                    while row[0] != self.routes[route_index].trips[trip_index].trip_id:
                        trip_index += 1

                        if trip_index == len(self.routes[route_index].trips):
                            trip_index = 0
                            route_index += 1

                    self.routes[route_index].trips[trip_index].add_stop_time(row)
                    self.count += 1
        except FileNotFoundError:
            print("The file " + path + " do not exist")
        print(str(self.count) + " times stops were imported")

    def find_and_update(self, list_of_coordinates):

        count_of_updates = 0
        index = 0
        for coordinates in list_of_coordinates:
            while coordinates[0].lower() != self.stops[index].name.lower():
                index += 1

            # Here we compare the coordinates to know if they need to be updated
            # It's just for counting reasons
            if self.stops[index].latitude == coordinates[1]:
                if self.stops[index].longitude == coordinates[2]:
                    count_of_updates += 1

            self.stops[index].latitude = coordinates[1]
            self.stops[index].longitude = coordinates[2]

        return count_of_updates

    def update_stops(self, li):
        # First add the stops
        for stop in li:
            char = stop.name[0]
            if char != "*" and char != "/" and char != "$":
                found = False
                stop_id2 = stop.name.replace(" ", "")
                stop_id1 = stop_id2.replace(".", "")
                stop_id3 = stop_id1.replace("'", "")
                stop_id = stop_id3.replace("-", "")
                stop_id_again = stop_id.lower()
                for stop_in_memory in self.stops:
                    if stop_in_memory.id == stop_id_again:
                        found = True
                        break
                if not found:
                    self.stops.append(Stop.Stop(stop.name, stop_id_again))

        # Then delete the file
        try:
            os.remove("sgtfs/coordinates.txt")
        except FileNotFoundError:
            pass

        # Then print stops which don't have coordinates
        with open("sgtfs/coordinates.txt", "w") as f:
            for stop in self.stops:
                if stop.latitude == "":
                    f.write(stop.name + "\n")

    @staticmethod
    def get_list_of_times_and_stop_name(line, sep_hours_minutes=':', empty_time='-', separator=None):
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
            elif re.match('^' + empty_time + '$', element):
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
        agency.init_routes_from_file()
        agency.init_trips_from_file()
        agency.init_times_stops_from_file()
        return agency

    def update_coordinates(self):
        # Find updates in the coordinates

        # This is a list of triplet
        list_of_coordinates = read_coordinates()
        if list_of_coordinates is None:
            number_of_updated_stops = 0
        else:
            number_of_updated_stops = self.find_and_update(list_of_coordinates)
        print("we've updated " + str(number_of_updated_stops) + "stop coordinates")

    def update_line(self):
        # Find updates in the lines
        print("updates line_something.txt")
        new_line = read_line_sgtfs("line.txt")

        if len(new_line) > 0:
            line_name = get_name(new_line)
            name_file = "line_" + line_name + ".txt"
            old_line = read_line_sgtfs(name_file)

            # We check if the line file already existed or not
            if len(old_line) == 1 and old_line[0] == "":
                print("Creating the file " + name_file)
                create_line_file(name_file)
                print("updating the line file now:")
                write(new_line, name_file)
            else:
                if old_line == new_line:
                    print("The line file is up to date")
                else:
                    print("updating the line file now:")
                    os.remove(name_file)
                    create_line_file(name_file)
                    write(new_line, name_file)
        else:
            print("line.txt is empty or does not exist")

    def add_timetable(self, file_path="sgtfs/timetable.txt"):
        # This function takes a timetable and convert it to a list of trips

        try:
            with open(file_path) as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("No timetable file")
            return None

        for line in lines:
            line.strip()

        # Here we get the name of the line and the service
        first_line = lines[0]
        first_line = first_line.split('\t')
        first_line_splitted = [x for x in first_line if x != '']
        route_name = first_line_splitted[0]
        trips_service = first_line_splitted[1].strip()
        try:
            empty_time = first_line_splitted[2]
        except IndexError:
            empty_time = "-"
        try:
            separator = first_line_splitted[3]
        except IndexError:
            separator = ":"

        lines.pop(0)
        list_stops_names = list()
        list_times = list()
        for line in lines:
            name, times_list = Agency.get_list_of_times_and_stop_name(line, separator, empty_time)
            list_stops_names.append(name)
            list_times.append(times_list)

        # Right now, we have a table of horizontal lines.
        # We have to get vertical lines instead.

        # Transposed is the transposition of the table list_times
        transposed = list(map(list, zip(*list_times)))

        # It's time for a little check.
        # It would be inconvenient that a bug allows to write anything in the files
        l = len(list_stops_names)
        for times in transposed:
            if l != len(times):
                print("issue of lenght at the list " + times[0])
                assert l == len(times)

        # Now we find the bus line in memory
        route1 = None
        for route in self.routes:
            if route.id == route_name:
                route1 = route
                break

        if route1 is None:
            # Then we have to create the bus line (add a route to the agency)
            route1 = Route.Route.from_stops_list(route_name, list_stops_names)
            self.routes.append(route1)

        # Here we initialise the graph, and we update all the stops found
        list_stops_of_graph_list = route1.init_graph()
        self.update_stops(list_stops_of_graph_list)

        # Here we check that the stops of the timetable correspond to the stops of the graph
        route1.graph.check_stops(list_stops_names)

        count = 0
        for times in transposed:
            route1.add_trip_from_times(list_stops_names, times, trips_service)
            count += 1
        print(str(count) + " trips have been added to the line " + route_name)

    def print(self):
        # Print everything into files to the gtfs folder
        print("write in gtfs folder")
        Other.export_in_csv([self, ], "agency.txt")
        Other.export_in_csv(self.calendar.services, "calendar.txt")

        list_of_stops = sorted(self.stops)
        Other.export_in_csv(list_of_stops, "stops.txt")

        list_of_routes = sorted(self.routes)
        Other.export_in_csv(list_of_routes, "routes.txt")

        list_of_trips = list()
        for route in list_of_routes:
            sorted_list_of_trips = sorted(route.trips)
            list_of_trips += sorted_list_of_trips
        Other.export_in_csv(list_of_trips, "trips.txt")

        list_of_stops_times = list()
        for trip in list_of_trips:
            list_of_stops_times += trip.stop_times
        Other.export_in_csv(list_of_stops_times, "stop_times.txt")

    @staticmethod
    def update():
        agency = Agency.add_gtfs()
        print("\n ****** Importation finished ****** \n")

        agency.update_coordinates()
        print("\n ****** update of coordinates finished ****** \n")

        agency.update_line()
        print("\n ****** Update of line finished ****** ")

        agency.add_timetable()
        print("\n ****** Update of times stops finished ****** \n")

        agency.print()

        print(" ****** All done ****** ")
