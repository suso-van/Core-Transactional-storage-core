import time

class ResearchMetrics:
    def __init__(self):
        self.records = []

    def record(self, name, value):
        self.records.append({
            "metric": name,
            "value": value,
            "time": time.time()
        })

    def report(self):
        return self.records
