from wal.log_record import LogType


class StateRebuilder:
    def __init__(self, wal_manager, file_manager):
        self.wal = wal_manager
        self.fm = file_manager

    def undo(self, incomplete_tx):
        logs = self.wal.read_all()
        undo_ops = []

        for rec in reversed(logs):
            if rec["txid"] in incomplete_tx and rec["type"] == LogType.WRITE.value:
                page = self.fm.fetch_page(rec["data"]["page_id"])
                page.write_data(
                    rec["data"]["offset"],
                    rec["data"]["old"]
                )
                self.fm.write_page(page)

                undo_ops.append({
                    "txid": rec["txid"],
                    "page": rec["data"]["page_id"],
                    "offset": rec["data"]["offset"]
                })

        return undo_ops
