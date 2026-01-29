from wal.log_record import LogType


class CrashDetector:
    def __init__(self, wal_manager):
        self.wal = wal_manager

    def detect(self):
        logs = self.wal.read_all()

        active = set()
        committed = set()
        aborted = set()

        for rec in logs:
            if rec["type"] == LogType.BEGIN.value:
                active.add(rec["txid"])

            elif rec["type"] == LogType.COMMIT.value:
                committed.add(rec["txid"])
                active.discard(rec["txid"])

            elif rec["type"] == LogType.ABORT.value:
                aborted.add(rec["txid"])
                active.discard(rec["txid"])

        return {
            "active": list(active),
            "committed": list(committed),
            "aborted": list(aborted),
            "incomplete": list(active)
        }
