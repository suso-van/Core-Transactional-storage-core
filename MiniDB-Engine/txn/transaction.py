import uuid
from wal.log_record import LogType
from utils.logger import new_trace_id, setup_logger

logger = setup_logger()

class Transaction:
    def __init__(self, wal_manager):
        self.txid = str(uuid.uuid4())
        self.trace_id = new_trace_id()
        self.wal = wal_manager
        self.active = False

        self.write_set = []   # (page, offset, old_data, new_data)
        self.read_set = []

    def begin(self):
        logger.info(
            f"TX BEGIN {self.txid}",
            extra={"trace_id": self.trace_id}
        )
        self.wal.append(self.txid, LogType.BEGIN)
        self.active = True

    def read(self, page, offset, size):
        data = page.read_data(offset, size)
        self.read_set.append((page.page_id, offset, size))

        logger.info(
            f"TX READ page={page.page_id}",
            extra={"trace_id": self.trace_id}
        )

        return data

    def write(self, page, offset, new_data: bytes):
        old_data = page.read_data(offset, len(new_data))
        self.write_set.append((page, offset, old_data, new_data))

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

        page.write_data(offset, new_data)

        logger.info(
            f"TX WRITE page={page.page_id}",
            extra={"trace_id": self.trace_id}
        )

    def commit(self, file_manager):
        for (page, _, _, _) in self.write_set:
            file_manager.write_page(page)

        self.wal.append(self.txid, LogType.COMMIT)

        logger.info(
            f"TX COMMIT {self.txid}",
            extra={"trace_id": self.trace_id}
        )

        self.active = False

    def abort(self, file_manager):
        for (page, offset, old_data, _) in reversed(self.write_set):
            page.write_data(offset, old_data)
            file_manager.write_page(page)

        self.wal.append(self.txid, LogType.ABORT)

        logger.warning(
            f"TX ABORT {self.txid}",
            extra={"trace_id": self.trace_id}
        )

        self.active = False
