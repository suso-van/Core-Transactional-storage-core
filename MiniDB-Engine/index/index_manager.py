from index.bplustree import BPlusTree
from index.index_wal import IndexWAL

class IndexManager:
    def __init__(self, wal_manager):
        self.tree = BPlusTree()
        self.wal = IndexWAL(wal_manager)

    def insert(self, txid, key, value):
        self.wal.log_insert(txid, key, value)
        self.tree.insert(key, value)

    def search(self, key):
        return self.tree.search(key)
