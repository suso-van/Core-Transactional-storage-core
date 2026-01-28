from wal.log_record import LogType

class CheckpointManager:
    def __init__(self, wal_manager):
        self.wal = wal_manager

    def create_checkpoint(self):
        self.wal.append(
            txid=0,
            log_type=LogType.CHECKPOINT,
            payload={"checkpoint": True}
        )
