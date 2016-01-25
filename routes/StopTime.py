import Other


class StopTime:
    def __init__(self, trip_id,  stop_id, stop_sequence, arrival_time = "",
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
