import time
from distributed.node import Node

class ClusterManager:
    def __init__(self):
        self.nodes = {}

    def register_node(self, node: Node):
        self.nodes[node.node_id] = node

    def heartbeat(self, node_id):
        if node_id in self.nodes:
            self.nodes[node_id].heartbeat()

    def detect_failures(self, timeout=10):
        now = time.time()
        for node in self.nodes.values():
            if now - node.last_heartbeat > timeout:
                node.alive = False

    def get_alive_nodes(self):
        return [n for n in self.nodes.values() if n.alive]

    def cluster_state(self):
        return {nid: node.info() for nid, node in self.nodes.items()}
