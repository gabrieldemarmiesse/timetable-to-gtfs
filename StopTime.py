import Other
class StopTime:
    def __init__(self,line):
        self.arrival_time = "undefined arrival time"
        self.departure_time = "undefined departure time"
        self.stop_id = "undefined stop id"
        self.pickup_type = "undefined pickup type"
        self.drop_off_type = "undefined drop off type"
        self.init_from_line(line)


    #is used to create actually the trip
    def init_from_line(self,line):
        self.arrival_time = line[1]
        self.departure_time = line[2]
        self.stop_id = line[3]
        self.pickup_type = line[5]
        self.drop_off_type = line[6]