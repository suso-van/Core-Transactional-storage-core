class TopologyView:
    def __init__(self, cluster_mgr, shard_mgr, replication_mgr):
        self.cluster = cluster_mgr
        self.shard = shard_mgr
        self.replication = replication_mgr

    def render(self):
        view = {
            "nodes": {},
            "shards": {},
            "replication": {}
        }

        # Nodes
        for nid, node in self.cluster.nodes.items():
            view["nodes"][nid] = node.info()

        # Shards
        view["shards"] = self.shard.shard_map()

        # Replication
        view["replication"] = self.replication.replica_sets

        return view
