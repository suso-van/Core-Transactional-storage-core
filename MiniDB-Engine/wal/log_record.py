import json
import time
from enum import Enum

class LogType(Enum):
    BEGIN = "BEGIN"
    WRITE = "WRITE"
    COMMIT = "COMMIT"
    ABORT = "ABORT"
    CHECKPOINT = "CHECKPOINT"

class LogRecord:
    def __init__(self, lsn, txid, log_type, payload=None):
        self.lsn = lsn
        self.txid = txid
        self.log_type = log_type
        self.payload = payload or {}
        self.timestamp = time.time()

    def serialize(self):
        return json.dumps({
            "lsn": self.lsn,
            "txid": self.txid,
            "type": self.log_type.value,
            "payload": self.payload,
            "timestamp": self.timestamp
        }) + "\n"

    @staticmethod
    def deserialize(line: str):
        data = json.loads(line)

        return LogRecord(
            data.get("txid"),
            LogType(data.get("type")),
            data.get("data"),
            data.get("lsn", -1)   # default if missing
        )
