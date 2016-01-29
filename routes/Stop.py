class Stop:
    def __init__(self, name, id=None, description="", latitude="", longitude="",
                 url="", location_type="", parent_station=""):

        self.id = id
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.url = url
        self.locationType = location_type
        self.parent_station = parent_station

    def __lt__(self, other):
        return self.id < other.id

    @classmethod
    def init_from_line(cls, line):
        return cls(line[1], line[0], line[2], line[3], line[4], line[5], line[6], line[7])

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
    def get_first_line_csv():
        return "stop_id,stop_name,stop_desc,stop_lat,stop_lon,stop_url,location_type,parent_station"
