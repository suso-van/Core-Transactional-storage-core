import threading

class LockManager:
    def __init__(self):
        self.locks = {}
        self.global_lock = threading.Lock()

    def acquire(self, resource_id, txid):
        with self.global_lock:
            if resource_id not in self.locks:
                self.locks[resource_id] = threading.Lock()
            lock = self.locks[resource_id]

        lock.acquire()

    def release(self, resource_id):
        if resource_id in self.locks:
            self.locks[resource_id].release()
