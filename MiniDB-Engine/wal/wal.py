import os
from wal.log_record import LogRecord, LogType

class WALManager:
    def __init__(self, wal_path="data/minidb.wal"):
        self.wal_path = wal_path
        open(self.wal_path, "ab").close()
        self.next_lsn = self._load_last_lsn()

    def _load_last_lsn(self):
        lsn = 0
        with open(self.wal_path, "r") as f:
            for line in f:
                rec = LogRecord.deserialize(line)
                lsn = rec.lsn
        return lsn + 1

    def append(self, txid, log_type, payload=None):
        rec = LogRecord(self.next_lsn, txid, log_type, payload)
        self.next_lsn += 1

        with open(self.wal_path, "a") as f:
            f.write(rec.serialize())
            f.flush()
            os.fsync(f.fileno())   # durability

        return rec.lsn
