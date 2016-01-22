class Stop:
    def __init__(self, line):
        self.id = "undefined id"
        self.name = "undefined name"
        self.description = "undefined description"
        self.latitude = "undefined latitude"
        self.longitude = "undefined longitude"
        self.url = "undefined url"
        self.locationType = "undefined type"
        self.parent_station = "undefined parent station"
        self.init_from_line(line)

    def init_from_line(self, line):
        self.id = line[0]
        self.name = line[1]
        self.description = line[2]
        self.latitude = line[3]
        self.longitude = line[4]
        self.url = line[5]
        self.locationType = line[6]
