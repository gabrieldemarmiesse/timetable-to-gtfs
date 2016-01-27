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
        self.parent_station = line[7]

    def to_list(self):
        list1 = list()
        list1.append(self.id)
        list1.append(self.name)
        list1.append(self.description)
        list1.append(self.latitude)
        list1.append(self.longitude)
        list1.append(self.url)
        list1.append(self.locationType)
        list1.append(self.parent_station)
        return list1

    @staticmethod
    def get_first_cvs_line():
        return "stop_id,stop_name,stop_desc,stop_lat,stop_lon,stop_url,location_type,parent_station\n"
