import os
import json
from wal.log_record import LogType


class WALManager:
    def __init__(self, log_file):
        self.log_file = log_file

        # Ensure WAL file exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        if not os.path.exists(log_file):
            open(log_file, "w").close()

    def _next_lsn(self):
        # LSN = line number (simple monotonic sequence)
        if not os.path.exists(self.log_file):
            return 1

        with open(self.log_file, "r") as f:
            return sum(1 for _ in f) + 1


    def append(self, txid, log_type, data=None):
        lsn = self._next_lsn()

        record = {
            "txid": txid,
            "type": log_type.value if hasattr(log_type, "value") else log_type,
            "lsn": lsn,
            "data": data
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(record) + "\n")

        return record


    def raw_append(self, record: dict):
        with open(self.log_file, "a") as f:
            f.write(json.dumps(record) + "\n")

    def read_all(self):
        records = []
        if not os.path.exists(self.log_file):
            return records

        with open(self.log_file, "r") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line.strip()))

        return records
