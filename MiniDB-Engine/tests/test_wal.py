from wal.wal import WALManager
from wal.log_record import LogType
import os

def test_wal_append(tmp_path):
    path = tmp_path / "test.wal"
    wal = WALManager(str(path))

    wal.append("tx1", LogType.BEGIN)
    wal.append("tx1", LogType.COMMIT)

    logs = wal.read_all()
    assert len(logs) == 2
