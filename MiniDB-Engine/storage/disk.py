import os
from storage.page import PAGE_SIZE, Page

class DiskManager:
    def __init__(self, file_path):
        self.file_path = file_path
        open(self.file_path, "ab").close()

    def write_page(self, page: Page):
        raw = page.serialize()
        with open(self.file_path, "r+b") as f:
            f.seek(page.page_id * PAGE_SIZE)
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())

    def read_page(self, page_id: int) -> Page:
        if not os.path.exists(self.file_path):
            raise ValueError("STORAGE FILE NOT FOUND")

        size = os.path.getsize(self.file_path)
        offset = page_id * PAGE_SIZE

        # Real DB-style validation
        if offset + PAGE_SIZE > size:
            raise ValueError(f"PAGE {page_id} DOES NOT EXIST")

        with open(self.file_path, "rb") as f:
            f.seek(offset)
            raw = f.read(PAGE_SIZE)

        return Page.deserialize(raw)
