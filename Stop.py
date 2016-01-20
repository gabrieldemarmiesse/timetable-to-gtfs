class Stop:
    def __init__(self,line):
        self.id = "undefined id"
        self.name= "undefined name"
        self.description = "undefined description"
        self.latitude = "undefined latitude"
        self.longitude = "undefined longitude"
        self.init_from_line(line)




    def init_from_line(self,line):
        a=1
        #here parse the line to init the stop