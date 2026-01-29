from txn.transaction import Transaction
from wal.wal import WALManager
from storage.file_manager import FileManager

def test_transaction_commit(tmp_path):
    data_path = tmp_path / "db.data"
    wal_path = tmp_path / "db.wal"

    fm = FileManager(str(data_path))
    wal = WALManager(str(wal_path))

    tx = Transaction(wal)
    tx.begin()

    page = fm.allocate_page()
    tx.write(page, 0, b"txn_data")
    tx.commit(fm)

    loaded = fm.fetch_page(page.page_id)
    assert loaded.read_data(0, 8) == b"txn_data"
