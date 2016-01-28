from routes.graph import StopOfGraph


class LinkedStops:
    """This class is here to create a map of the stops in a line
it will have a structure of graph so will be implement as a dictionary
here is an example:
graph ={'A': ['B', 'C'],
        'B': ['C', 'D'],
        'C': ['D'],
        'D': ['C'],
        'E': ['F'],
        'F': ['C']}

We also add artificially false bus stops
where the bus doesn't usually go
(he will take the shortest path)"""

    def __init__(self,route_id):
        self.dictionary = dict()
        self.line_id = "undefined"
        self.list_stops_of_graph_list = list()
        self.create_from_file(route_id)

    def insert_node(self, main_node, *links_to_add):
        # The first argument is the node from where starts the links
        # This function can be used to add links to an existing node

        # Here we get the old links if they exist and put an empty tuple if not
        try:
            old_links = self.dictionary[main_node]
        except KeyError:
            old_links = ()

        # We add the node to the graph here
        new_links = old_links + links_to_add
        self.dictionary[main_node] = new_links

        # Here we call the function again in case
        # the new links point to nodes which are not in the dictionary
        for node in links_to_add:
            self.insert_node(node)

    def create_from_file(self, route_id, path="../../sgtfs"):
        self.list_stops_of_graph_list = self.read_file(path, route_id)

        previous_node = self.list_stops_of_graph_list[0]
        node_before_star1 = None
        node_before_star2 = None
        node_before_slash =None
        star_count = 0

        for i, current_node in enumerate(self.list_stops_of_graph_list[1:]):
            current_stop = current_node.name
            if current_stop == "*":
                node_before_star1 = previous_node
                node_before_star2 = node_before_star1
                star_count += 1
            elif current_stop == "/":
                node_before_slash = previous_node
            else:
                if previous_node.name == "*":
                    if star_count % 2 == 0:
                        pass
                    else:
                        pass
                elif  previous_node.name == "/":
                    pass
                else:
            previous_node = current_node

    def read_file(self, path, route_id):
        """this method parse the file line.txt to create a
        list of StopOfGraph which is much easier to use to
        create a graph"""

        path += "/line_" + route_id + ".txt"
        with open(path) as f:
            lines = f.readlines()

        stop_of_graph_list = list()

        # So here we're examining the lines of the file
        for line in lines[1:]:
            line = line.strip()

            if line != '':
                stop_of_graph_list.append(StopOfGraph.StopOfGraph(line))

        # We mustn't forget to give our bus line a name
        self.line_id = lines[0]
        return stop_of_graph_list

    def find_shortest_path(self, start, end, path=None):
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return path
        if start not in self.dictionary:
            return None
        shortest = None
        for node in self.dictionary[start]:
            if node not in path:
                new_path = self.find_shortest_path(node, end, path)
                if new_path:
                    if not shortest or len(new_path) < len(shortest):
                        shortest = new_path
        return shortest

    def find_complete_stops_list(self, list):
        """this function finds the complete list of stops
        based on the list of the main stops the bus is doing through"""

        # List contains the main stops
        # list_of_list contains the little stops which are not in the timetable

        list_of_lists = list()
        previous_stop = list[0]
        for current_stop in list[1:]:
            missing_stops = self.find_shortest_path(previous_stop,current_stop)
            missing_stops.pop(0)
            missing_stops.pop()
            list_of_lists.happend(missing_stops)

        # Now we fuses everything, the main stops and the little stops
        complete_stops_list = [list[0],]
        for i, current_main_stop in enumerate(list[1:]):
            complete_stops_list += list_of_lists[i]
            complete_stops_list.happend(current_main_stop)



# Tests
#a = LinkedStops()