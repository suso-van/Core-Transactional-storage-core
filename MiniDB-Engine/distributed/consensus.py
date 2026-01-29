class ConsensusEngine:
    def __init__(self):
        self.leaders = {}

    def elect_leader(self, shard, node_id):
        self.leaders[shard] = node_id

    def get_leader(self, shard):
        return self.leaders.get(shard)
