import Other


class StopOfGraph:
    """this class is here to convert the lines of the file descibing the line shape.
    it will contain informations about the links that the stop should have
    it's just an object to parse a line of line.txt"""

    def __init__(self, line):
        self.name = "undefined name"

        # Tell if we have to put a link toward the previous stop in the file
        self.link_up = True

        # Tell if we have to put a link toward the next spot in the file
        self.link_down = True
        self.init_from_line(line)

    def init_from_line(self, line):
        # Initialise values from the line

        splited_line = Other.split_by_tab(line)

        # We get the name
        self.name = splited_line[0]

        # Here we get the directions the bus can go
        # No number means both directions are possible
        try:
            if splited_line[1] == '1':
                self.link_up = False
            elif splited_line[1] == '2':
                self.link_down = False
        except IndexError:
            pass
