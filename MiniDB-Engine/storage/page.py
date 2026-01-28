import struct
import hashlib
import time

PAGE_SIZE = 4096  # 4KB

# Page layout sizes
HEADER_SIZE = 32
METADATA_SIZE = 32
CHECKSUM_SIZE = 32
DATA_SIZE = PAGE_SIZE - (HEADER_SIZE + METADATA_SIZE + CHECKSUM_SIZE)

class Page:
    def __init__(self, page_id, version=1, page_type=1):
        self.page_id = page_id
        self.version = version
        self.page_type = page_type
        self.lsn = 0
        self.dirty = False
        self.timestamp = int(time.time())
        self.data = bytearray(DATA_SIZE)

    # -------- Serialization --------
    def serialize(self):
        header = struct.pack(
            "I I I Q",
            self.page_id,
            self.version,
            self.page_type,
            self.timestamp
        ).ljust(HEADER_SIZE, b'\x00')

        metadata = struct.pack(
            "Q ?",
            self.lsn,
            self.dirty
        ).ljust(METADATA_SIZE, b'\x00')

        body = self.data.ljust(DATA_SIZE, b'\x00')

        checksum = hashlib.sha256(header + metadata + body).digest()

        return header + metadata + body + checksum

    # -------- Deserialization --------
    @staticmethod
    def deserialize(raw_bytes):
        header = raw_bytes[:HEADER_SIZE]
        metadata = raw_bytes[HEADER_SIZE:HEADER_SIZE+METADATA_SIZE]
        body = raw_bytes[HEADER_SIZE+METADATA_SIZE:HEADER_SIZE+METADATA_SIZE+DATA_SIZE]
        checksum = raw_bytes[-CHECKSUM_SIZE:]

        # Verify checksum
        calc = hashlib.sha256(header + metadata + body).digest()
        if calc != checksum:
            raise ValueError("PAGE CORRUPTION DETECTED")

        page_id, version, page_type, timestamp = struct.unpack("I I I Q", header[:24])
        lsn, dirty = struct.unpack("Q ?", metadata[:9])

        page = Page(page_id, version, page_type)
        page.timestamp = timestamp
        page.lsn = lsn
        page.dirty = dirty
        page.data = bytearray(body)

        return page

    # -------- Data Ops --------
    def write_data(self, offset, bdata):
        self.data[offset:offset+len(bdata)] = bdata
        self.dirty = True

    def read_data(self, offset, size):
        return self.data[offset:offset+size]

    def __str__(self):
        data_preview = self.read_data(0, min(100, len(self.data)))
        return f"""DATA: {data_preview}
PAGE ID: {self.page_id}
VERSION: {self.version}
LSN: {self.lsn}
DIRTY: {self.dirty}
TIMESTAMP: {self.timestamp}"""
