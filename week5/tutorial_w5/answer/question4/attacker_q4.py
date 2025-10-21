from cryptography.hazmat.primitives import hashes
from binascii import hexlify
from pathlib import Path
from sha_implementation import generate_hash  # we'll use this implementation since it lets us set the IV and prefix

message_path = "outputs/message.bin"
tag_path = "outputs/tag.bin"
key_path = "outputs/key.bin"


def sha256_glue_padding(total_len_bytes: int) -> bytes:
    bit_len = total_len_bytes * 8
    pad = b"\x80"
    pad += b"\x00" * ((56 - (total_len_bytes + 1) % 64) % 64)
    pad += bit_len.to_bytes(8, "big")
    return pad

def read_file(filepath: str) -> bytes:
    with open(filepath, "rb") as f:
        data = f.read()
    return data
    
def gen_new_message(original_msg, additional_msg, key_length):
    glue = sha256_glue_padding(key_length + len(original_msg))
    new_msg = original_msg + glue + additional_msg
    return new_msg
    
def lengh_extension_attack(
    original_msg: bytes, 
    additional_msg: bytes, 
    original_sig: bytes, 
    key_length: int) -> bytes:
    # Build forged message that would be sent to the server
    new_message = gen_new_message(original_msg, additional_msg, key_length)
    # Compute the glue length to advance the internal bit counter correctly
    glue_len = len(sha256_glue_padding(key_length + len(original_msg)))
    # Continue hashing from original_sig over ONLY the additional message,
    # accounting for bytes already processed (key_len + len(original_msg) + len(glue))
    gen_attack_tag = generate_hash(bytearray(additional_msg), iv=original_sig,
                                   prefix_len=key_length + len(original_msg) + glue_len)
    return new_message, gen_attack_tag

def main():
    original_msg = read_file(message_path)
    original_sig = read_file(tag_path)
    
    original_key = read_file(key_path)  # only for verification!
    
    additional_msg = b" with pickles"   # usually what I prefer on a cheeseburger
    wrote_outputs = False
    for key_length in range(8, 65):  # guessing key length between 8 and 64 bytes
        print("Trying key length:", key_length)
        new_message, forged_tag = lengh_extension_attack(
            original_msg, additional_msg, original_sig, key_length)

        # Verify using the secret key (only for local validation in the lab)
        digest = hashes.Hash(hashes.SHA256())
        digest.update(original_key + new_message)
        full_message_tag = digest.finalize()

        if forged_tag == full_message_tag:
            print(f"Success! Key length guessed: {key_length}")
            print(f"Forged tag: {hexlify(forged_tag).decode()}")
            print(f"Full message tag: {hexlify(full_message_tag).decode()}")
            print(f"New message length: {len(new_message)} bytes")
            
            out_dir = Path("outputs")
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "forged_message.bin").write_bytes(new_message)
            (out_dir / "forged_tag.bin").write_bytes(forged_tag)
            wrote_outputs = True
            break

    if not wrote_outputs:
        # Emit the last candidate if none verified (e.g., if key missing)
        out_dir = Path("outputs")
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "forged_message.bin").write_bytes(new_message)
        (out_dir / "forged_tag.bin").write_bytes(forged_tag)
        print("Wrote candidate forged_message.bin and forged_tag.bin")

if __name__ == "__main__":
    main()