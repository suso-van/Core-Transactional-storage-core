class SimulationEngine:
    def __init__(self, benchmark, chaos, recovery):
        self.benchmark = benchmark
        self.chaos = chaos
        self.recovery = recovery

    def simulate_failure(self, workload):
        killed = self.chaos.kill_random_node()
        result = self.benchmark.run(workload, rounds=10)
        self.recovery.rebuild_replication()
        return {
            "killed_node": killed,
            "benchmark": result
        }
