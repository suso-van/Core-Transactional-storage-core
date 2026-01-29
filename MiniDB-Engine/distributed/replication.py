class ReplicationManager:
    def __init__(self):
        self.replica_sets = {}  # shard -> [leader, followers]

    def create_replica_set(self, shard, nodes):
        if not nodes:
            return
        self.replica_sets[shard] = {
            "leader": nodes[0],
            "followers": nodes[1:]
        }

    def get_leader(self, shard):
        return self.replica_sets.get(shard, {}).get("leader")

    def get_followers(self, shard):
        return self.replica_sets.get(shard, {}).get("followers", [])

    def replicate(self, shard, data):
        leader = self.get_leader(shard)
        followers = self.get_followers(shard)
        return {
            "leader": leader,
            "replicated_to": followers,
            "data": data
        }
