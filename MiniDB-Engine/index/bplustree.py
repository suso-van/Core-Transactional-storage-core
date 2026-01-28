from index.node import BPlusNode

ORDER = 4  # small order for demo, scalable later

class BPlusTree:
    def __init__(self):
        self.root = BPlusNode(is_leaf=True)

    def search(self, key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        for i, k in enumerate(node.keys):
            if k == key:
                return node.values[i]
        return None

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == (2 * ORDER - 1):
            new_root = BPlusNode(is_leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node.keys.insert(i, key)
            node.values.insert(i, value)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            if len(node.children[i].keys) == (2 * ORDER - 1):
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, index):
        order = ORDER
        node = parent.children[index]
        new_node = BPlusNode(is_leaf=node.is_leaf)

        mid = order - 1
        parent.keys.insert(index, node.keys[mid])
        parent.children.insert(index + 1, new_node)

        new_node.keys = node.keys[mid+1:]
        node.keys = node.keys[:mid]

        if node.is_leaf:
            new_node.values = node.values[mid:]
            node.values = node.values[:mid]
            new_node.next = node.next
            node.next = new_node
        else:
            new_node.children = node.children[mid+1:]
            node.children = node.children[:mid+1]
