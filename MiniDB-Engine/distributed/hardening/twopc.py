class TwoPhaseCommit:
    def __init__(self):
        self.prepared = {}
        self.committed = set()

    def prepare(self, txid, nodes):
        self.prepared[txid] = nodes
        return True  # simulate ACKs

    def commit(self, txid):
        if txid in self.prepared:
            self.committed.add(txid)
            del self.prepared[txid]
            return True
        return False

    def abort(self, txid):
        if txid in self.prepared:
            del self.prepared[txid]
        return True
