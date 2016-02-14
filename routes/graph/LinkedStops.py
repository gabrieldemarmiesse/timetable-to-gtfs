import io

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

    def __init__(self, route_id):
        self.dictionary = dict()
        self.line_id = "undefined"
        self.list_stops_of_graph = self.read_file("sgtfs", route_id)

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

    def double_link(self,main_node, other_node):
        self.insert_node(main_node, other_node)
        self.insert_node(other_node, main_node)

    def create_from_file(self):

        previous_name = self.list_stops_of_graph[0].name
        node_before_star1 = None
        node_before_star2 = None
        node_before_slash1 = None
        node_before_slash2 = None
        node_before_double_slash1 = None
        node_before_double_slash2 = None
        star_count = 0
        slash_count = 0
        double_slash_count = 0

        for i, current_node in enumerate(self.list_stops_of_graph[1:]):
            current_stop = current_node.name
            if current_stop == "*":
                node_before_star2 = node_before_star1
                node_before_star1 = previous_name
                star_count += 1

            elif current_stop == "/":
                node_before_slash2 = node_before_slash1
                node_before_slash1 = previous_name
                slash_count += 1

            elif current_stop == "//":
                node_before_double_slash2 = node_before_double_slash1
                node_before_double_slash1 = previous_name
                double_slash_count += 1

            else:
                if previous_name == "*":
                    if star_count % 2 == 0:
                        self.double_link(current_stop, node_before_star1)
                        self.double_link(current_stop, node_before_star2)
                    else:
                        self.double_link(current_stop, node_before_star1)

                elif  previous_name == "/":
                    if slash_count % 3 == 1:
                        self.double_link(current_stop, node_before_slash1)
                    elif slash_count % 3 == 2:
                        self.double_link(current_stop, node_before_slash2)
                    else :
                        self.double_link(current_stop, node_before_slash1)
                        self.double_link(current_stop, node_before_slash2)

                elif  previous_name == "//":
                    if double_slash_count % 3 == 1:
                        self.double_link(current_stop, node_before_double_slash1)
                    elif double_slash_count % 3 == 2:
                        self.double_link(current_stop, node_before_double_slash2)
                    else :
                        self.double_link(current_stop, node_before_double_slash1)
                        self.double_link(current_stop, node_before_double_slash2)

                else:
                    if current_node.link_up:
                        j = i
                        while self.list_stops_of_graph[j].link_up is False:
                            j -= 1
                        self.insert_node(current_stop, self.list_stops_of_graph[j].name)

                    if current_node.link_down:
                        j = i
                        while self.list_stops_of_graph[j].link_down is False:
                            j -= 1
                        self.insert_node(self.list_stops_of_graph[j].name, current_stop)

            previous_name = current_node.name

    def check_stops(self, list_stops, comparator):
        list_returned = list()

        for stop in list_stops:
            stop = comparator.look_for_stop(stop)
            try:
                a = self.dictionary[stop]
                list_returned.append(stop)
            except:
                # There is no stop name in the line corresponding, we'll check in depth
                found = False
                list_of_ressemblance = list()
                for i, line in enumerate(self.list_stops_of_graph):
                    list_of_ressemblance.append([comparator.get_ressemblance(line.name, stop), i])
                    if comparator.compare(line.name, stop):
                        found = True
                        list_returned.append(line.name)
                        break
                if not found:
                    sorted_list = sorted(list_of_ressemblance)
                    for ressemblance in sorted_list:
                        if comparator.compare(self.list_stops_of_graph[ressemblance[1]].name, stop, True):
                            found = True
                            list_returned.append(self.list_stops_of_graph[ressemblance[1]].name)
                            break
                    if not found:
                        assert False

        return list_returned

    def read_file(self, path, route_id):
        """this method parse the file line.txt to create a
        list of StopOfGraph which is much easier to use to
        create a graph"""

        #uncoded_route_id = route_id.decode("utf-8")
        route_id = str(route_id)
        path += "/line_" + route_id + ".txt"
        with io.open(path, encoding="utf-8") as f:
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

    def find_complete_stops_list(self, list_main_stops):
        """this function finds the complete list of stops
        based on the list of the main stops the bus is doing through"""

        # List contains the main stops
        # list_of_list contains the little stops which are not in the timetable

        list_of_lists = list()
        previous_stop = list_main_stops[0]
        for current_stop in list_main_stops[1:]:
            missing_stops = self.find_shortest_path(previous_stop, current_stop)
            missing_stops.pop(0)
            missing_stops.pop()
            list_of_lists.append(missing_stops)
            previous_stop = current_stop

        # Now we fuses everything, the main stops and the little stops
        complete_stops_list = [list_main_stops[0], ]
        for i, current_main_stop in enumerate(list_main_stops[1:]):
            complete_stops_list += list_of_lists[i]
            complete_stops_list.append(current_main_stop)

        return complete_stops_list

# Tests
#a = LinkedStops()