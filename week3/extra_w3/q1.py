from io import BufferedWriter
import ciphersuite_aesnotrand as ciphersuite
from binascii import hexlify, unhexlify
import time
KEYLEN: int = 16

key: bytes = ciphersuite.gen()
msg: str = 'Attack at dawn!!'
cph: bytes = ciphersuite.enc(key, bytearray(msg,'ascii'))

f: BufferedWriter = open("weak_ciphertext", "wb")
f.write(cph)
f.close()



## 
# Extend me to
# 1 - Read ciphertext

with open("weak_ciphertext", "rb") as f:
    ciphertext: bytes = f.read()
print(ciphertext)

# 2 - Guess the key used

def guess_key(offset: int, ciphertext: bytes) -> bytearray:
    start = time.perf_counter()
    last_second = 0
    
    
    guesses: int = 0
    guessed_key_start: bytes
    for i in range(offset):
        guessed_key_start: bytes = bytearray(b'\x00' * (KEYLEN - (i + 1)))
        print(f"Key start size: {len(guessed_key_start)}")
        
        
        possible_values: int = 2 ** (8 * (i + 1))   # 8 bits per byte
        print(f"Possible values: {possible_values}")
        
        for j in range(possible_values):
            full_guessed_key: bytes = guessed_key_start + bytearray(j.to_bytes(i + 1, 'big'))

            decryption: bytes = ciphersuite.dec(full_guessed_key, ciphertext)
            guesses += 1
            
            time_passed_sec = int(time.perf_counter() - start)
            
            if time_passed_sec != 0 and last_second < time_passed_sec and time_passed_sec % 1 == 0:
                last_second = time_passed_sec
                print(f"Guesses in {time_passed_sec} second:", guesses)
            
            
            if decryption == bytearray(msg, 'ascii'):
                print(f"Key found: {hexlify(full_guessed_key)}")
                print(f"Offset: {i + 1}")
                print(f"Guesses: {j+1}")
                print(f"Time: {time.perf_counter() - start:.6f}s")
                return full_guessed_key
        
        
    return bytearray(b'\x00' * KEYLEN)  # Return a default value
        
guessed_key: bytearray = guess_key(3, ciphertext)
# 3 - Test the decryption
##