class Service:
    def __init__(self,service_id, days, start, end):
        self.id = service_id
        self.days = days
        self.start = start
        self.end = end

    def to_list(self):
        list1 = list()
        list1.append(self.id)
        for day in self.days:
            list1.append(day)
        list1.append(self.start)
        list1.append(self.end)
        return list1

    @staticmethod
    def get_first_line_csv():
        return "service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n"

