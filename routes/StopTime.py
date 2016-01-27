import Other


class StopTime:
    def __init__(self, trip_id,  stop_id, stop_sequence, arrival_time="",
                 pickup_type="", drop_off_type="", departure_time=None):
        self.trip_id = trip_id
        self.arrival_time = arrival_time
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence
        self.pickup_type = pickup_type
        self.drop_off_type = drop_off_type

        if departure_time is None:
            self.departure_time = arrival_time
        else:
            self.departure_time = departure_time

    # A constructor overload
    @classmethod
    def init_from_line(cls, line):
        """
        :param line: The parsed cvs line
        :return: A StopTime object
        """
        return cls(line[0],  line[3], line[4], line[1], line[5], line[6], line[2])

    def to_list(self):
        elements_list = list()
        elements_list.append(self.trip_id)
        elements_list.append(self.arrival_time)
        elements_list.append(self.departure_time)
        elements_list.append(self.stop_id)
        elements_list.append(self.stop_sequence)
        elements_list.append(self.pickup_type)
        elements_list.append(self.drop_off_type)

    @staticmethod
    def get_first_cvs_line(self):
        return "trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type\n"

