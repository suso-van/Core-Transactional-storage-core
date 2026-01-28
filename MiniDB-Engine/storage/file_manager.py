import os
from storage.disk import DiskManager
from storage.page import Page, PAGE_SIZE

class FileManager:
    def __init__(self, file_path):
        self.disk = DiskManager(file_path)
        self.file_path = file_path
        self.next_page_id = self._load_next_page_id()

    def _load_next_page_id(self):
        if not os.path.exists(self.file_path):
            return 0
        size = os.path.getsize(self.file_path)
        return size // PAGE_SIZE

    def allocate_page(self, page_type=1) -> Page:
        page = Page(self.next_page_id, page_type=page_type)
        self.disk.write_page(page)
        self.next_page_id += 1
        return page

    def fetch_page(self, page_id: int) -> Page:
        return self.disk.read_page(page_id)

    def write_page(self, page: Page):
        self.disk.write_page(page)
