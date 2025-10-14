# Python Module ciphersuite
import os
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Security parameter (fixed)
BLOCK = 16

# Use crypto random generation to get a key with up to 3 random bytes
def gen_key(): 
	key = bytearray(os.urandom(BLOCK)) 
	return bytes(key)

def enc(k: bytes, m: bytes, iv: bytes) -> bytes:
	cipher = Cipher(algorithms.AES(k), modes.CBC(iv))
	encryptor = cipher.encryptor()
	cph = b""
	cph += encryptor.update(m)
	cph += encryptor.finalize()
	return cph


def dec(k: bytes, c: bytes, iv: bytes) -> bytes:
	cipher = Cipher(algorithms.AES(k), modes.CBC(iv))
	decryptor = cipher.decryptor()
	msg = b""
	msg += decryptor.update(c)
	msg += decryptor.finalize()
	return msg


def iv_gen(k: bytes, nounce: bytes) -> bytes:
	cipher = Cipher(algorithms.AES(k), modes.ECB())
	encryptor = cipher.encryptor()
	iv = b""
	iv += encryptor.update(nounce)
	iv += encryptor.finalize()
	return iv


def split_blocks(b: bytes) -> list[bytes]:
    return [b[i:i+BLOCK] for i in range(0, len(b), BLOCK)]



def break_experiment(k: bytes, C1_query: bytes, C3_query: bytes) -> bool:
    # Let's now create our m0 and m1 for the experiment
    m0 = b'\x00'*16*3
    m1 = os.urandom(16) + b'\x00'*16*2
    
    messages = [m0, m1]
    
    print(f'Message 0:\n {messages[0].hex()}\n')
    print(f'Message 1:\n {messages[1].hex()}\n')
    
    # Let's now create our nounce for the experiment
    nounce = C1_query  # This is the trick, we set the nounce to be C1 from the query encryption
    
    print(f'Nounce:\n {nounce.hex()}\n')
    
    iv = iv_gen(k, nounce)

    print(f'IV:\n {iv.hex()}\n')

    b = random.randint(0, 1)
    
    print(f'Chosen message index (b):\n {b}\n')
    
    #We cipher the chosen message
    cph = split_blocks(enc(k, messages[b], iv))

    print(f'Ciphertext blocks:\n {[c.hex() for c in cph]}\n')

    if cph[0] == C3_query:  # We get if C1' == C3 from the query encryption
        b_guess = 0
    else:
        b_guess = 1
        
        
    print(f'Guessed message index (b\'):\n {int(b_guess)}\n')
    print(f'Actual message index (b):\n {int(b)}\n')
    
    return b == b_guess  # Return if we guessed correctly 



def run_experiment(trials: int = 100) -> float:
    # Let's set our query first, such that k is random, nounce is 0 and message is 3 blocks with only 0s
    # and iv is EC(k, nounce)

    k = gen_key()
    nounce_query = b'\x00'*16
    m_query = b'\x00'*16*3
    iv = iv_gen(k, nounce_query)

    encryption_query  = split_blocks(enc(k, m_query, iv))

    # Here are the three ciphertext blocks mentioned and explained in the previous question
    C1 = encryption_query[0]
    C2 = encryption_query[1]  # Not used in the experiment
    C3 = encryption_query[2]
    
    print(f'C1:\n {C1.hex()}\n')
    print(f'C2:\n {C2.hex()}\n')
    print(f'C3:\n {C3.hex()}\n')
    
    
    for i in range(trials):
        print(f"|||||||||||||||||||||    TRIAL {i+1}/{trials}    |||||||||||||||||||")
        if not break_experiment(k, C1, C3):
            return 0.0
        
        
run_experiment()
        
    
    
    
    