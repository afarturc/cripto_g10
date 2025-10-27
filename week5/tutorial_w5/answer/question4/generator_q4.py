from cryptography.hazmat.primitives import hashes
from binascii import hexlify, unhexlify
import os
from pathlib import Path

folder_name= "outputs"

key_name= "key.bin"
message_name = "message.bin"
tag_name = "tag.bin"

def ensure_dir(directory: str)-> Path:
    p = Path(directory)
    p.mkdir(parents=True, exist_ok=True)
    return p

def gen_key() -> bytes:
    return os.urandom(32)

def gen_mac_sha2(message: bytes, key: bytes) -> bytes:
    concat = key + message
    digest = hashes.Hash(hashes.SHA256())
    digest.update(concat)
    return digest.finalize()

def save_into_file(out_dir: str, filename: str, data: bytes) -> Path:
    output_dir = ensure_dir(out_dir)
    out_path = output_dir / filename
    
    with open(out_path, "wb") as f:
        f.write(data)
    return out_path


def main()->None:
    message = "I want a cheeseburguer"
    message = message.encode()
    
    key = gen_key()
    tag = gen_mac_sha2(message, key)

    save_into_file(folder_name, key_name, key)
    save_into_file(folder_name, message_name, message)
    save_into_file(folder_name, tag_name, tag)

if __name__ == "__main__":
    main()