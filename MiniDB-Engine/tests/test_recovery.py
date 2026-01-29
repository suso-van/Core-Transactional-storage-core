from wal.wal import WALManager
from wal.log_record import LogType
from recovery import RecoveryManager


def test_recovery_redo(tmp_path):
    wal_path = tmp_path / "rec.wal"
    wal = WALManager(str(wal_path))

    wal.append("tx1", LogType.BEGIN)
    wal.append("tx1", LogType.COMMIT)

    recovery = RecoveryManager(wal)
    result = recovery.recover()

    assert "redo" in result
