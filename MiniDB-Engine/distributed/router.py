class Router:
    def __init__(self, shard_manager, cluster_manager):
        self.shard_mgr = shard_manager
        self.cluster_mgr = cluster_manager

    def route(self, key):
        shard = self.shard_mgr.shard_for_key(key)
        nodes = self.shard_mgr.shards.get(shard, [])
        return shard, nodes
