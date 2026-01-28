import hashlib

def compute_checksum(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def verify_checksum(data: bytes, checksum: bytes) -> bool:
    return hashlib.sha256(data).digest() == checksum
