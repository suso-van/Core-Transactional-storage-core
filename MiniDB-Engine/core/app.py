from storage.file_manager import FileManager
from wal.wal import WALManager
from index.index_manager import IndexManager
from query.planner import QueryPlanner
from query.executer import QueryExecutor
from utils.config import load_config
from utils.logger import setup_logger


class MiniDBApp:
    def __init__(self, config_path: str = "config/default.yaml"):
        # load configuration (supports env overrides and secrets)
        self.config = load_config(config_path)

        # logger
        self.logger = setup_logger(log_file=self.config.get("logging", {}).get("file", "logs/minidb.log"))
        env = self.config.get("system", {}).get("environment", "local")
        self.logger.info(f"Starting MiniDB Engine ({env})")

        # core components
        self.fm = FileManager(self.config["storage"]["data_path"])
        self.wal = WALManager(self.config["wal"]["wal_path"])
        self.index = IndexManager(self.wal)

        # query layer
        self.planner = QueryPlanner()
        self.executor = QueryExecutor(self.fm, self.index, self.wal)

        self.logger.info("MiniDB Engine initialized")

    def start(self):
        self.logger.info("MiniDB Engine started")

    def status(self):
        return {
            "storage": self.config["storage"]["data_path"],
            "wal": self.config["wal"]["wal_path"],
            "index": "B+Tree",
            "status": "RUNNING"
        }
