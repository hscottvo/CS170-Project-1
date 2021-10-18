class Node:

    def __init__(self, parent: Node, child_a: Node, child_b: Node): 
        self.a = child_a
        self.b = child_b
        self.parent = parent
