import hashlib

class ShardManager:
    def __init__(self, shard_count=3):
        self.shard_count = shard_count
        self.shards = {i: [] for i in range(shard_count)}

    def shard_for_key(self, key):
        h = hashlib.sha256(str(key).encode()).hexdigest()
        return int(h, 16) % self.shard_count

    def assign(self, key, node_id):
        shard = self.shard_for_key(key)
        self.shards[shard].append(node_id)
        return shard

    def shard_map(self):
        return self.shards

