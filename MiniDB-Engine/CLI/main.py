import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.app import MiniDBApp
from version import __version__

def main():
    parser = argparse.ArgumentParser(prog="minidb")
    parser.add_argument("command", choices=["run", "status", "version"])
    parser.add_argument("--config", default="config/default.yaml")

    args = parser.parse_args()

    app = MiniDBApp(args.config)

    if args.command == "run":
        app.start()
        print("MiniDB is running")

    elif args.command == "status":
        status = app.status()
        print("\n=== SYSTEM STATUS ===")
        for k, v in status.items():
            print(f"{k}: {v}")

    elif args.command == "version":
        print("MiniDB Version:", __version__)

if __name__ == "__main__":
    main()
