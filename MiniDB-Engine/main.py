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
