from routes.graph import StopOfGraph


class LinkedStops():
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

    def __init__(self):
        self.dictionary = dict()
        self.line_id = "undefined"
        self.create_from_file()

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

    def create_from_file(self, path="../../gtfs"):
        stop_of_graph_list = self.read_file(path)

        previous_node = None
        node_before_separation = None
        end_of_branch_node =None

        for current_node in stop_of_graph_list:
            if current_node.in_a_loop:
                if previous_node.in_a_loop:
                    if current_node.link_up:
                        self.insert_node(current_node.name, previous_node.name)
                    if previous_node.link_down:
                        self.insert_node(previous_node.name,current_node.name)
                else:
                    self.insert_node(current_node.name, previous_node.name,node_before_separation)
                    self.insert_node(previous_node.name,current_node.name)
                print("we have to do something")
            else:
                if previous_node.in_a_loop == False:
                    if current_node.link_up:
                        self.insert_node(current_node.name, previous_node.name)
                    if previous_node.link_down:
                        self.insert_node(previous_node.name,current_node.name)

                else:
                    print("yolo")

    def read_file(self,path):
        """this method parse the file line.txt to create a
        list of StopOfGraph which is much easier to use to
        create a graph"""

        path += "/line.txt"
        with open(path) as f:
            lines = f.readlines()

        stop_of_graph_list = list()
        in_a_loop = False

        # So here we're examining the lines of the file
        for line in lines[1:]:
            line = line.strip()

            # If we encounter a *, it means that we enter a loop or leave one
            if line == '*':
                in_a_loop = not in_a_loop
            elif line == '':
                continue
            else:
                stop_of_graph_list.append(StopOfGraph.StopOfGraph(line, in_a_loop))

        # We mustn't forget to give our bus line a name
        self.line_id = lines[0]
        return stop_of_graph_list

# Tests
a = LinkedStops()
b = 8
