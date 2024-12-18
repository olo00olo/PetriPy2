from Place import Place
from Transition import Transition


class NewArc:
    def __init__(self):
        self.source = None
        self.destination = None
        self.error = 0

    def searchNode(self, nodes):
        findNode = None
        for node in nodes:
            if isinstance(node, (Place, Transition)):
                findNode = node
        return findNode

    def setNode(self, nodes):
        node = self.searchNode(nodes)
        if node is None:
            self.reset()
        elif self.source is None:
            self.source = node
        else:
            if type(node) is type(self.source):
                self.error = 1
            else:
                self.destination = node
        return self.source, self.destination, self.error

    def reset(self):
        self.source = None
        self.destination = None
        self.error = 0
