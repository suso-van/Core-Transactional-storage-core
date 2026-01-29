import uuid
import time

class Node:
    def __init__(self, host, port, role="worker"):
        self.node_id = str(uuid.uuid4())
        self.host = host
        self.port = port
        self.role = role
        self.last_heartbeat = time.time()
        self.alive = True

    def heartbeat(self):
        self.last_heartbeat = time.time()
        self.alive = True

    def info(self):
        return {
            "node_id": self.node_id,
            "host": self.host,
            "port": self.port,
            "role": self.role,
            "alive": self.alive,
            "last_heartbeat": self.last_heartbeat
        }
