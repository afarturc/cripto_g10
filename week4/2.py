#!/usr/bin/env python3
# Source: https://github.com/DavidBuchanan314/rc4

import argparse


class RC4:
    def __init__(self, key: bytes):
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.i = 0
        self.j = 0

    def process(self, data: bytes) -> bytes:
        out = bytearray()
        for byte in data:
            self.i = (self.i + 1) % 256
            self.j = (self.j + self.S[self.i]) % 256
            self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
            K = self.S[(self.S[self.i] + self.S[self.j]) % 256]
            out.append(byte ^ K)
        return bytes(out)


def encrypt_or_decrypt(input_file: str, output_file: str, key: str):
    rc4 = RC4(key.encode())
    with open(input_file, "rb") as f_in:
        data = f_in.read()
    result = rc4.process(data)
    with open(output_file, "wb") as f_out:
        f_out.write(result)
    print(f"Operation completed: '{input_file}' -> '{output_file}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RC4 Encryption/Decryption Tool (GitHub version)")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Mode: encrypt or decrypt")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file")
    parser.add_argument("key", help="Secret key (string)")

    args = parser.parse_args()
    encrypt_or_decrypt(args.input, args.output, args.key)
