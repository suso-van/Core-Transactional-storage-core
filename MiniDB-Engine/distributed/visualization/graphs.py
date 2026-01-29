class SystemGraph:
    def __init__(self, topology_view):
        self.topology = topology_view

    def build_graph(self):
        topo = self.topology.render()
        graph = []

        for shard, repl in topo["replication"].items():
            leader = repl.get("leader")
            followers = repl.get("followers", [])

            for f in followers:
                graph.append((leader, f))

        return graph

    def display(self):
        graph = self.build_graph()
        print("\n=== REPLICATION GRAPH ===")
        for edge in graph:
            print(f"{edge[0]} --> {edge[1]}")
