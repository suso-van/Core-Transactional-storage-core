from wal.wal import WALManager
from wal.log_record import LogType
from utils.logger import setup_logger, new_trace_id


logger = setup_logger()


class Transaction:
    def __init__(self, txid, wal_path="data/minidb.wal"):
        self.txid = txid
        self.trace_id = new_trace_id()

        # Always use WALManager, not string
        self.wal = WALManager(wal_path)

    def begin(self):
        logger.info(f"TX BEGIN {self.txid}", extra={"trace_id": self.trace_id})
        self.wal.append(self.txid, LogType.BEGIN)

    def write(self, data: bytes):
        logger.info(f"TX WRITE {self.txid}", extra={"trace_id": self.trace_id})
        self.wal.append(self.txid, LogType.WRITE, data=data.decode(errors="ignore"))

    def commit(self):
        logger.info(f"TX COMMIT {self.txid}", extra={"trace_id": self.trace_id})
        self.wal.append(self.txid, LogType.COMMIT)

    def abort(self):
        logger.info(f"TX ABORT {self.txid}", extra={"trace_id": self.trace_id})
        self.wal.append(self.txid, LogType.ABORT)
