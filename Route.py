class Route:
    def __init__(self,line,path):
        self.id = "undefined id"
        self.short_name = "undefined short name"
        self.long_name = "undefined long name"
        self.description = "undefined description"
        self.type = "undefined route type"
        self.trips = list()
        self.init_from_line(line)
        self.init_trips_from_file(path)

    def init_from_line(self,line):
        a=5
        #here we init from the line.

    def init_trips_from_file(self,path = "gtfs"):
        path += "/trips.txt"
        trips_file = open(path,"r")