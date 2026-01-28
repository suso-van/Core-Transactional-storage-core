from wal.log_record import LogType, LogRecord

class RecoveryEngine:
    def __init__(self, wal_path="data/minidb.wal"):
        self.wal_path = wal_path

    def recover(self):
        active_tx = set()
        committed_tx = set()
        logs = []

        with open(self.wal_path, "r") as f:
            for line in f:
                rec = LogRecord.deserialize(line)
                logs.append(rec)

                if rec.log_type == LogType.BEGIN:
                    active_tx.add(rec.txid)
                elif rec.log_type == LogType.COMMIT:
                    committed_tx.add(rec.txid)
                    active_tx.discard(rec.txid)
                elif rec.log_type == LogType.ABORT:
                    active_tx.discard(rec.txid)

        redo = [r for r in logs if r.txid in committed_tx]
        undo = [r for r in logs if r.txid in active_tx]

        return redo, undo
