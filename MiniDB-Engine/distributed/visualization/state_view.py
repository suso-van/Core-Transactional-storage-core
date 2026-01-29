class StateView:
    def __init__(self, cluster_mgr, shard_mgr, replication_mgr):
        self.cluster = cluster_mgr
        self.shard = shard_mgr
        self.replication = replication_mgr

    def snapshot(self):
        return {
            "alive_nodes": [n.node_id for n in self.cluster.get_alive_nodes()],
            "shard_map": self.shard.shard_map(),
            "replication": self.replication.replica_sets
        }

    def display(self):
        snap = self.snapshot()

        print("\n=== LIVE SYSTEM STATE ===")
        print("Alive Nodes:", snap["alive_nodes"])
        print("Shard Map:", snap["shard_map"])
        print("Replication:", snap["replication"])
