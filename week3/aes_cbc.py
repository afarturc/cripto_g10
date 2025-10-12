from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import argparse


def encrypt_file(input_file, output_file, key):
    with open(input_file, 'r') as f:
        plaintext = f.read().encode()
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)
    
    print(f"Encrypted: {output_file}")


def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()
    
    iv = data[:16]
    ciphertext = data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    with open(output_file, 'w') as f:
        f.write(plaintext.decode())
    
    print(f"Decrypted: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt or decrypt text files using AES CBC',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python aes_cbc.py encrypt input.txt -o encrypted.bin -k mykey.bin
  python aes_cbc.py decrypt encrypted.bin -o output.txt -k mykey.bin
        '''
    )
    
    parser.add_argument('mode', choices=['encrypt', 'decrypt'],
                       help='Operation mode')
    parser.add_argument('input', help='Input file')
    parser.add_argument('-o', '--output', help='Output file (default: input + .enc or .dec)')
    parser.add_argument('-k', '--key', help='Key file (default: random key, saved to key.bin)')
    
    args = parser.parse_args()
    
    if args.key:
        with open(args.key, 'rb') as f:
            key = f.read()
        if len(key) != 32:
            parser.error(f"Key must be 32 bytes, got {len(key)}")
    else:
        key = os.urandom(32)
        with open('key.bin', 'wb') as f:
            f.write(key)
        print(f"Generated key saved to: key.bin")
    
    if args.output:
        output = args.output
    else:
        if args.mode == 'encrypt':
            output = args.input + '.enc'
        else:
            output = args.input[:-4] if args.input.endswith('.enc') else args.input + '.dec'
    
    if args.mode == 'encrypt':
        encrypt_file(args.input, output, key)
    else:
        decrypt_file(args.input, output, key)


if __name__ == '__main__':
    main()
