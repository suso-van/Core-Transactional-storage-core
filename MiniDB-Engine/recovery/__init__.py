from recovery.cash_detector import CrashDetector
from recovery.replay_engine import ReplayEngine
from recovery.stat_rebuilder import StateRebuilder


class RecoveryManager:
    def __init__(self, wal_manager, file_manager=None):
        self.wal = wal_manager
        self.fm = file_manager

        self.detector = CrashDetector(wal_manager)

        # Allow WAL-only recovery (for tests)
        if file_manager:
            self.replay = ReplayEngine(wal_manager, file_manager)
            self.rebuilder = StateRebuilder(wal_manager, file_manager)
        else:
            self.replay = None
            self.rebuilder = None

    def recover(self):
        crash_state = self.detector.detect()

        redo_result = []
        undo_result = []

        if self.replay:
            redo_result = self.replay.redo(crash_state["committed"])

        if self.rebuilder:
            undo_result = self.rebuilder.undo(crash_state["incomplete"])

        return {
            "crash_state": crash_state,
            "redo": redo_result,
            "undo": undo_result
        }
