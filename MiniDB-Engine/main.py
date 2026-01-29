from storage.file_manager import FileManager
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

fm = FileManager("data/minidb.data")

# Allocate page
page = fm.allocate_page(page_type=1)

# Write data
page.write_data(0, b"Enterprise MiniDB Storage Engine")
fm.write_page(page)

# Read back
loaded = fm.fetch_page(page.page_id)

data = bytes(loaded.read_data(0, 32)).rstrip(b'\x00')
print("DATA:", data)
print("PAGE ID:", loaded.page_id)
print("VERSION:", loaded.version)
print("LSN:", loaded.lsn)
print("DIRTY:", loaded.dirty)
print("TIMESTAMP:", loaded.timestamp)
from wal.wal import WALManager
from wal.log_record import LogType
from wal.recovery import RecoveryEngine

wal = WALManager("data/minidb.wal")

# Simulated transaction
txid = 1
wal.append(txid, LogType.BEGIN)
wal.append(txid, LogType.WRITE, {"page": 0, "offset": 0, "data": "HELLO"})
wal.append(txid, LogType.COMMIT)

# Simulate crash recovery
recovery = RecoveryEngine("data/minidb.wal")
redo, undo = recovery.recover()

print("\n=== RECOVERY RESULT ===")
print("REDO TX:", [r.txid for r in redo])
print("UNDO TX:", [r.txid for r in undo])
from storage.file_manager import FileManager
from wal.wal import WALManager
from txn.transaction import Transaction
import os

# Ensure data dir
os.makedirs("data", exist_ok=True)

fm = FileManager("data/minidb.data")
wal = WALManager("data/minidb.wal")

# Allocate page
page = fm.allocate_page(page_type=1)

# ---- TRANSACTION 1 ----
tx = Transaction(wal)
tx.begin()

tx.write(page, 0, b"BANK_TXN_COMMIT")
tx.commit(fm)

loaded = fm.fetch_page(page.page_id)
data_commit = bytes(loaded.read_data(0, 15)).rstrip(b'\x00')
print("\nAFTER COMMIT:", data_commit)

# ---- TRANSACTION 2 ----
tx2 = Transaction(wal)
tx2.begin()

tx2.write(page, 0, b"BANK_TXN_ABORT")
tx2.abort(fm)

loaded2 = fm.fetch_page(page.page_id)
data_abort = bytes(loaded2.read_data(0, 15)).rstrip(b'\x00')
print("AFTER ABORT:", data_abort)
from index.index_manager import IndexManager
from wal.wal import WALManager

wal = WALManager("data/minidb.wal")
index_mgr = IndexManager(wal)

print("\n=== INDEX ENGINE TEST ===")

txid = "IDX-TX-1"

index_mgr.insert(txid, 1001, "ACCOUNT_A")
index_mgr.insert(txid, 1002, "ACCOUNT_B")
index_mgr.insert(txid, 1003, "ACCOUNT_C")

print("SEARCH 1001:", index_mgr.search(1001))
print("SEARCH 1002:", index_mgr.search(1002))
print("SEARCH 1003:", index_mgr.search(1003))
print("SEARCH 9999 (NOT FOUND):", index_mgr.search(9999))
from query.planner import QueryPlanner
from query.executer import QueryExecutor
from txn.transaction import Transaction
from wal.wal import WALManager
from index.index_manager import IndexManager
from storage.file_manager import FileManager
import os

os.makedirs("data", exist_ok=True)

fm = FileManager("data/minidb.data")
wal = WALManager("data/minidb.wal")
index_mgr = IndexManager(wal)

planner = QueryPlanner()
executor = QueryExecutor(fm, index_mgr, wal)

print("\n=== QUERY ENGINE TEST ===")

# Transaction
tx = Transaction(wal)
tx.begin()

# Insert records
executor.execute(planner.plan_insert(1, "Alice"), tx)
executor.execute(planner.plan_insert(2, "Bob"), tx)
executor.execute(planner.plan_insert(3, "Charlie"), tx)

tx.commit(fm)

# New transaction for reads
tx2 = Transaction(wal)
tx2.begin()

print("GET 1:", executor.execute(planner.plan_get(1), tx2))
print("GET 2:", executor.execute(planner.plan_get(2), tx2))
print("GET 3:", executor.execute(planner.plan_get(3), tx2))

print("SCAN:", executor.execute(planner.plan_scan(), tx2))

tx2.commit(fm)
print("GET 999 (NOT FOUND):", executor.execute(planner.plan_get(999), tx2))
tx2.commit(fm)
from txn.isolation import IsolationLevel
print("=== ISOLATION LEVELS ===")
for level in IsolationLevel:
    print(level.name, ":", level.value)
    
# Added SNAPSHOT isolation level
print("SNAPSHOT :", IsolationLevel.SNAPSHOT.value)
from observability.metrics import GLOBAL_METRICS
from observability.stats import SystemStats
from observability.diagonistics import Diagnostics

print("\n=== OBSERVABILITY TEST ===")

stats = SystemStats()
diag = Diagnostics()

# Metrics
GLOBAL_METRICS.inc("transactions_committed", 1)
GLOBAL_METRICS.inc("transactions_committed", 1)
GLOBAL_METRICS.inc("transactions_aborted", 1)
GLOBAL_METRICS.inc("page_writes", 5)

print("\nMETRICS SNAPSHOT:")
print(GLOBAL_METRICS.snapshot())

# Stats
print("\nSYSTEM STATS:")
print("Storage size:", stats.storage_size(), "bytes")
print("WAL size:", stats.wal_size(), "bytes")
print("Page count:", stats.page_count())
print("Index size:", stats.index_size(index_mgr))

# Diagnostics
print("\nSYSTEM HEALTH:")
print(diag.health_check())

from distributed.node import Node
from distributed.cluster import ClusterManager
from distributed.shard import ShardManager
from distributed.router import Router
from distributed.replication import ReplicationManager
from distributed.coordinator import Coordinator
from distributed.consensus import ConsensusEngine
from distributed.recovery import DistributedRecovery

print("\n=== DISTRIBUTED SYSTEM TEST ===")

# Cluster
cluster = ClusterManager()

n1 = Node("127.0.0.1", 5001, role="leader")
n2 = Node("127.0.0.1", 5002)
n3 = Node("127.0.0.1", 5003)

cluster.register_node(n1)
cluster.register_node(n2)
cluster.register_node(n3)

# Sharding
shard_mgr = ShardManager(shard_count=3)
shard_mgr.assign("user1", n1.node_id)
shard_mgr.assign("user2", n2.node_id)
shard_mgr.assign("user3", n3.node_id)

# Routing
router = Router(shard_mgr, cluster)

# Replication
replication = ReplicationManager()
for shard, nodes in shard_mgr.shards.items():
    replication.create_replica_set(shard, nodes)

# Consensus
consensus = ConsensusEngine()
for shard, nodes in shard_mgr.shards.items():
    if nodes:
        consensus.elect_leader(shard, nodes[0])

# Coordinator
coord = Coordinator(router, replication)

# Recovery
recovery = DistributedRecovery(cluster, shard_mgr, replication)

print("Cluster state:", cluster.cluster_state())
print("Shard map:", shard_mgr.shard_map())
print("Replica sets:", replication.replica_sets)

result = coord.coordinate_write("user1", "BALANCE_UPDATE")
print("\nDISTRIBUTED TX:", result)

from distributed.hardening.quorum import QuorumManager
from distributed.hardening.consistency import ConsistencyManager, ConsistencyModel
from distributed.hardening.twopc import TwoPhaseCommit
from distributed.hardening.safety import SafetyManager
from distributed.hardening.failure_domains import FailureDomainManager

print("\n=== HARDENING LAYER TEST ===")

# Quorum
quorum = QuorumManager(replication_factor=3)
print("Write quorum:", quorum.write_quorum())
print("Read quorum:", quorum.read_quorum())

# Consistency
consistency = ConsistencyManager(ConsistencyModel.STRONG)
print("Strong consistency write valid:", consistency.validate_write(True))

# 2PC
twopc = TwoPhaseCommit()
txid = "DIST-TX-1"
nodes = ["n1", "n2", "n3"]
print("Prepare:", twopc.prepare(txid, nodes))
print("Commit:", twopc.commit(txid))

# Safety
safety = SafetyManager()
print("Leader valid:", safety.validate_leader("n1", ["n1", "n2"]))

# Failure domains
fd = FailureDomainManager()
fd.assign_domain("n1", "dc1")
fd.assign_domain("n2", "dc2")
fd.assign_domain("n3", "dc1")

print("Multi-domain replication valid:", fd.validate_replication(["n1", "n2"]))
from distributed.visualization.topology import TopologyView
from distributed.visualization.dashboard import SystemDashboard
from distributed.visualization.graphs import SystemGraph
from distributed.visualization.state_view import StateView

print("\n=== VISUALIZATION LAYER TEST ===")

topology = TopologyView(cluster, shard_mgr, replication)
dashboard = SystemDashboard(topology)
graph = SystemGraph(topology)
state_view = StateView(cluster, shard_mgr, replication)

dashboard.display()
graph.display()
state_view.display()
from distributed.research.benchmark import BenchmarkEngine
from distributed.research.workload import WorkloadGenerator
from distributed.research.chaos import ChaosEngine
from distributed.research.metrics import ResearchMetrics
from distributed.research.simulation import SimulationEngine
from distributed.research.models import PerformanceModels

print("\n=== RESEARCH LAYER TEST ===")

workload = WorkloadGenerator(size=50)
benchmark = BenchmarkEngine(coord)
chaos = ChaosEngine(cluster)
metrics = ResearchMetrics()
models = PerformanceModels()
simulation = SimulationEngine(benchmark, chaos, recovery)

# Benchmark
result = benchmark.run(workload, rounds=5)
metrics.record("throughput", result["throughput_ops_sec"])
metrics.record("time", result["time"])

print("Benchmark result:", result)

# Chaos test
sim = simulation.simulate_failure(workload)
print("Simulation result:", sim)

# Models
lat = models.latency_model(result["operations"], result["time"])
thr = models.throughput_model(result["operations"], result["time"])

print("\nMODELS:")
print("Latency:", lat)
print("Throughput:", thr)

print("\nRESEARCH METRICS:")
print(metrics.report())
