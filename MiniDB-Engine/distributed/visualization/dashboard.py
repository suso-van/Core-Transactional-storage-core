class SystemDashboard:
    def __init__(self, topology_view):
        self.topology = topology_view

    def display(self):
        topo = self.topology.render()

        print("\n=== MINI DB DISTRIBUTED DASHBOARD ===\n")

        print("NODES:")
        for nid, info in topo["nodes"].items():
            print(f" - {nid[:6]} | {info['host']}:{info['port']} | {info['role']} | alive={info['alive']}")

        print("\nSHARDS:")
        for shard, nodes in topo["shards"].items():
            print(f" - Shard {shard}: {nodes}")

        print("\nREPLICATION:")
        for shard, repl in topo["replication"].items():
            print(f" - Shard {shard}: leader={repl.get('leader')} followers={repl.get('followers')}")
