import yaml
from storage.file_manager import FileManager
from wal.wal import WALManager
from index.index_manager import IndexManager
from query.planner import QueryPlanner
from query.executer import QueryExecutor
from txn.transaction import Transaction

class MiniDBApp:
    def __init__(self, config_path="config/default.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.fm = FileManager(self.config["storage"]["data_path"])
        self.wal = WALManager(self.config["wal"]["wal_path"])
        self.index = IndexManager(self.wal)

        self.planner = QueryPlanner()
        self.executor = QueryExecutor(self.fm, self.index, self.wal)

    def start(self):
        print("MiniDB Engine started")

    def status(self):
        return {
            "storage": self.config["storage"]["data_path"],
            "wal": self.config["wal"]["wal_path"],
            "index": "B+Tree",
            "status": "RUNNING"
        }
