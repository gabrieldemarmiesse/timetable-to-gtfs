import Node

#This class is here to create a map of the stops in a line
class LinkedStops(object):
    def __init__(self, head=None):
        self.head = head
        self.tails = list(head)

    def insert(self, data):
        new_node = Node.Node(data)
        new_node.set_next(self.head)
        self.head = new_node