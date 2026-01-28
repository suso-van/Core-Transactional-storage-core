import uuid
from wal.log_record import LogType

class Transaction:
    def __init__(self, wal_manager):
        self.txid = str(uuid.uuid4())
        self.wal = wal_manager
        self.active = False

        # Now store actual page references
        self.write_set = []   # (page_obj, offset, old_data, new_data)
        self.read_set = []

    def begin(self):
        self.wal.append(self.txid, LogType.BEGIN)
        self.active = True

    def read(self, page, offset, size):
        data = page.read_data(offset, size)
        self.read_set.append((page.page_id, offset, size))
        return data

    def write(self, page, offset, new_data: bytes):
        old_data = page.read_data(offset, len(new_data))

        # Store page object, not page_id
        self.write_set.append((page, offset, old_data, new_data))

        # WAL first (durability rule)
        self.wal.append(
            self.txid,
            LogType.WRITE,
            {
                "page_id": page.page_id,
                "offset": offset,
                "old": old_data.decode(errors="ignore"),
                "new": new_data.decode(errors="ignore")
            }
        )

        # In-memory write
        page.write_data(offset, new_data)

    def commit(self, file_manager):
        # Persist the actual modified pages
        for (page, _, _, _) in self.write_set:
            file_manager.write_page(page)

        self.wal.append(self.txid, LogType.COMMIT)
        self.active = False

    def abort(self, file_manager):
        # Rollback using in-memory old values
        for (page, offset, old_data, _) in reversed(self.write_set):
            page.write_data(offset, old_data)
            file_manager.write_page(page)

        self.wal.append(self.txid, LogType.ABORT)
        self.active = False
