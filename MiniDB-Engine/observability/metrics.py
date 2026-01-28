import time
import threading

class MetricsRegistry:
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()

    def inc(self, name, value=1):
        with self.lock:
            self.metrics[name] = self.metrics.get(name, 0) + value

    def set(self, name, value):
        with self.lock:
            self.metrics[name] = value

    def get(self, name):
        return self.metrics.get(name, 0)

    def snapshot(self):
        with self.lock:
            return dict(self.metrics)


GLOBAL_METRICS = MetricsRegistry()
