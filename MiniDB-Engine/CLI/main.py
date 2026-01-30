import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.app import MiniDBApp
from version import __version__

from wal.wal import WALManager
from recovery import RecoveryManager
from storage.file_manager import FileManager
from txn.transaction import Transaction


def cmd_run(app):
    app.start()
    print("MiniDB is running")


def cmd_status(app):
    status = app.status()
    print("\n=== SYSTEM STATUS ===")
    for k, v in status.items():
        print(f"{k}: {v}")


def cmd_version():
    print("MiniDB Version:", __version__)


def cmd_recover():
    print("\n=== RECOVERY MODE ===")

    wal = WALManager("data/minidb.wal")
    fm = FileManager("data/minidb.data")
    recovery = RecoveryManager(wal, fm)

    result = recovery.recover()

    print("Recovery Result:")
    print("REDO:", result.get("redo"))
    print("UNDO:", result.get("undo"))


def cmd_wal():
    print("\n=== WAL LOG ===")

    wal = WALManager("data/minidb.wal")
    logs = wal.read_all()

    for rec in logs:
        print(rec)


def cmd_txn():
    print("\n=== TRANSACTION DEMO ===")

    txn = Transaction("cli_txn")
    txn.begin()
    txn.write(b"CLI_TRANSACTION_DATA")
    txn.commit()

    print("Transaction committed.")


def cmd_init():
    print("\n=== INIT SYSTEM ===")

    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    print("Created:")
    print(" - data/")
    print(" - logs/")


def main():
    parser = argparse.ArgumentParser(prog="minidb")

    parser.add_argument(
        "command",
        choices=[
            "run",
            "status",
            "version",
            "recover",
            "wal",
            "txn",
            "init"
        ]
    )

    parser.add_argument("--config", default="config/default.yaml")

    args = parser.parse_args()

    # Core app only needed for some commands
    app = MiniDBApp(args.config)

    if args.command == "run":
        cmd_run(app)

    elif args.command == "status":
        cmd_status(app)

    elif args.command == "version":
        cmd_version()

    elif args.command == "recover":
        cmd_recover()

    elif args.command == "wal":
        cmd_wal()

    elif args.command == "txn":
        cmd_txn()

    elif args.command == "init":
        cmd_init()


if __name__ == "__main__":
    main()
