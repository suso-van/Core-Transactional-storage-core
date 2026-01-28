class BPlusNode:
    def __init__(self, is_leaf=True):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []   # for internal nodes
        self.values = []     # for leaf nodes
        self.next = None     # leaf chaining (range scans)
