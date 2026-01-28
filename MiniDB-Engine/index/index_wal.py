from wal.log_record import LogType

class IndexWAL:
    def __init__(self, wal_manager):
        self.wal = wal_manager

    def log_insert(self, txid, key, value):
        self.wal.append(
            txid,
            LogType.WRITE,
            {
                "index_op": "INSERT",
                "key": key,
                "value": value
            }
        )
