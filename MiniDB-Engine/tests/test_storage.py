from storage.file_manager import FileManager

def test_storage_write_read(tmp_path):
    path = tmp_path / "test.data"
    fm = FileManager(str(path))

    page = fm.allocate_page()
    data = b"hello"
    page.write_data(0, data)
    fm.write_page(page)

    loaded = fm.fetch_page(page.page_id)
    assert loaded.read_data(0, len(data)) == data
