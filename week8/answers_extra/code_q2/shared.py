import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import hmac
import struct

HOST = "127.0.0.1"
PORT = 10101

def loadKeys() -> tuple[bytes, bytes]:
    encryption_key = authentication_key = None
    with open("pw", "rb") as f:
        encryption_key = f.read(16)
        authentication_key = f.read(32)
        
    return (encryption_key, authentication_key)


def encrypt_aes_ctr(key: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Encrypts plaintext using AES-128-CTR.
    Returns (nonce, ciphertext).
    """
    # Generate a random nonce (16 bytes for AES)
    nonce = os.urandom(16)
    
    # Create cipher
    cipher = Cipher(
        algorithms.AES(key),
        modes.CTR(nonce),
        backend=default_backend()
    )
    
    # Encrypt
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    return (nonce, ciphertext)


def decrypt_aes_ctr(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypts ciphertext using AES-128-CTR.
    Returns plaintext.
    """
    # Create cipher with the same nonce
    cipher = Cipher(
        algorithms.AES(key),
        modes.CTR(nonce),
        backend=default_backend()
    )
    
    # Decrypt
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    return plaintext


def compute_hmac(key: bytes, data: bytes) -> bytes:
    """
    Computes HMAC-SHA256 of the data.
    Returns the HMAC tag (32 bytes).
    """
    h = hmac.new(key, data, hashlib.sha256)
    return h.digest()


def verify_hmac(key: bytes, data: bytes, received_hmac: bytes) -> bool:
    """
    Verifies the HMAC-SHA256 tag.
    Returns True if valid, False otherwise.
    Uses constant-time comparison to prevent timing attacks.
    """
    expected_hmac = compute_hmac(key, data)
    return hmac.compare_digest(expected_hmac, received_hmac)


def send_data(socket, plaintext, encryption_key, authentication_key, seq_num):
    nonce, ciphertext = encrypt_aes_ctr(encryption_key, plaintext)
    
    #NOTE: nonce (16 bytes) and HMAC (32 bytes)
    
    seq_bytes = struct.pack("!I", seq_num)
    
    hmac_tag = compute_hmac(authentication_key, nonce + ciphertext)
    
    # seq_bytes || nonce || ciphertext || hmac_tag
    message = seq_bytes + nonce + ciphertext + hmac_tag
    socket.sendall(message)
    
    
def receive_data(conn, encryption_key, authentication_key, expected_seq_num):
    
    #NOTE: nonce (16 bytes) and HMAC (32 bytes)
    data = conn.recv(4096)
    
    seq_bytes = data[:4]
    nonce = data[4:20]
    ciphertext = data[20:-32]
    hmac_tag = data[-32:]
    
    # Verify HMAC first
    if not verify_hmac(authentication_key, nonce + ciphertext, hmac_tag):
        raise Exception("Invalid data, not the same HMAC")
    
    # Verify sequence number
    seq_num = struct.unpack("!I", seq_bytes)[0]
    if seq_num != expected_seq_num:
        raise ValueError(f"Invalid sequence number!")
    
    return decrypt_aes_ctr(encryption_key, nonce, ciphertext)
    
    