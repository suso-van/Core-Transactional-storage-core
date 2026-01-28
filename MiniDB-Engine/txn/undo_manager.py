class UndoManager:
    def __init__(self):
        self.undo_logs = {}

    def log(self, txid, page_id, offset, old_data):
        if txid not in self.undo_logs:
            self.undo_logs[txid] = []
        self.undo_logs[txid].append((page_id, offset, old_data))

    def rollback(self, txid, file_manager):
        if txid not in self.undo_logs:
            return

        for (page_id, offset, old_data) in reversed(self.undo_logs[txid]):
            page = file_manager.fetch_page(page_id)
            page.write_data(offset, old_data)
            file_manager.write_page(page)

