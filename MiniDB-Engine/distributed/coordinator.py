import uuid

class Coordinator:
    def __init__(self, router, replication_mgr):
        self.router = router
        self.replication_mgr = replication_mgr

    def global_txid(self):
        return str(uuid.uuid4())

    def coordinate_write(self, key, value):
        shard, nodes = self.router.route(key)
        leader = self.replication_mgr.get_leader(shard)

        txid = self.global_txid()

        return {
            "global_txid": txid,
            "shard": shard,
            "leader": leader,
            "nodes": nodes,
            "value": value
        }
