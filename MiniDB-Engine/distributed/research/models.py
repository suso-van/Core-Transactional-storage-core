class PerformanceModels:
    def latency_model(self, ops, time_sec):
        return time_sec / ops

    def throughput_model(self, ops, time_sec):
        return ops / time_sec

    def scalability_model(self, nodes, throughput):
        return throughput / nodes
