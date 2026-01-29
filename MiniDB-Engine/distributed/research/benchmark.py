import time

class BenchmarkEngine:
    def __init__(self, coordinator):
        self.coordinator = coordinator

    def run(self, workload, rounds=100):
        start = time.time()
        ops = 0

        for _ in range(rounds):
            for op in workload.operations():
                self.coordinator.coordinate_write(op["key"], op["value"])
                ops += 1

        end = time.time()
        return {
            "operations": ops,
            "time": end - start,
            "throughput_ops_sec": ops / (end - start)
        }
