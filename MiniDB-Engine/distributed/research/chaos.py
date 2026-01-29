import random

class ChaosEngine:
    def __init__(self, cluster_mgr):
        self.cluster = cluster_mgr

    def kill_random_node(self):
        alive = self.cluster.get_alive_nodes()
        if not alive:
            return None
        node = random.choice(alive)
        node.alive = False
        return node.node_id

    def heal_all(self):
        for node in self.cluster.nodes.values():
            node.alive = True
