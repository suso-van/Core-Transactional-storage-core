import os

class Diagnostics:
    def __init__(self, data_path="data"):
        self.data_path = data_path

    def health_check(self):
        results = {}

        results["storage_ok"] = os.path.exists(os.path.join(self.data_path, "minidb.data"))
        results["wal_ok"] = os.path.exists(os.path.join(self.data_path, "minidb.wal"))

        # basic corruption check
        try:
            if results["storage_ok"]:
                from storage.file_manager import FileManager
                fm = FileManager(os.path.join(self.data_path, "minidb.data"))
                if fm.next_page_id > 0:
                    fm.fetch_page(0)
                results["page_read_ok"] = True
            else:
                results["page_read_ok"] = False
        except Exception:
            results["page_read_ok"] = False

        return results
