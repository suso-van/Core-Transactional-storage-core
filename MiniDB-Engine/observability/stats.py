import os

class SystemStats:
    def __init__(self, data_path="data"):
        self.data_path = data_path

    def storage_size(self):
        path = os.path.join(self.data_path, "minidb.data")
        return os.path.getsize(path) if os.path.exists(path) else 0

    def wal_size(self):
        path = os.path.join(self.data_path, "minidb.wal")
        return os.path.getsize(path) if os.path.exists(path) else 0

    def page_count(self):
        from storage.page import PAGE_SIZE
        size = self.storage_size()
        return size // PAGE_SIZE if size else 0

    def index_size(self, index_mgr):
        # simple metric: number of indexed keys
        def count_nodes(node):
            if node.is_leaf:
                return len(node.keys)
            return sum(count_nodes(child) for child in node.children)

        return count_nodes(index_mgr.tree.root)
