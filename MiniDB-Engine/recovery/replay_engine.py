from wal.log_record import LogType


class ReplayEngine:
    def __init__(self, wal_manager, file_manager):
        self.wal = wal_manager
        self.fm = file_manager

    def redo(self, committed_tx):
        logs = self.wal.read_all()
        redo_ops = []

        for rec in logs:
            if rec["txid"] in committed_tx and rec["type"] == LogType.WRITE.value:
                page = self.fm.fetch_page(rec["data"]["page_id"])
                page.write_data(
                    rec["data"]["offset"],
                    rec["data"]["new"]
                )
                self.fm.write_page(page)

                redo_ops.append({
                    "txid": rec["txid"],
                    "page": rec["data"]["page_id"],
                    "offset": rec["data"]["offset"]
                })

        return redo_ops
