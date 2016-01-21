import Other
import Trip
class Route:
    def __init__(self,line,path = "gtfs"):
        self.id = "undefined id"
        self.short_name = "undefined short name"
        self.long_name = "undefined long name"
        self.description = "undefined description"
        self.type = "undefined route type"
        self.trips = list()
        self.init_from_line(line)
        self.init_trips_from_file(path)

    def init_from_line(self,line):
        self.id = line[0]
        self.short_name = line[1]
        self.long_name = line[2]
        self.description = line[3]
        self.type = line[4]

    def init_trips_from_file(self,path = "gtfs"):
        path += "/trips.txt"
        Other.read_cvs(path,self.add_trip)

    def add_trip(self,line):
        print("trip" + line[2])
        if(line[0] == self.id):
            trip = Trip.Trip(line)
            self.trips.append(trip)
