class DistributedRecovery:
    def __init__(self, cluster_mgr, shard_mgr, replication_mgr):
        self.cluster = cluster_mgr
        self.shard = shard_mgr
        self.replication = replication_mgr

    def recover_node(self, node_id):
        # reassign shards from dead node
        for shard, nodes in self.shard.shards.items():
            if node_id in nodes:
                nodes.remove(node_id)

    def rebuild_replication(self):
        for shard, nodes in self.shard.shards.items():
            if nodes:
                self.replication.create_replica_set(shard, nodes)
