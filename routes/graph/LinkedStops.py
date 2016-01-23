class LinkedStops(object):
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
