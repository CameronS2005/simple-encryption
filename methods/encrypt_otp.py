#!/usr/bin/python
import os
import sys

def read_file(filename):
    with open(filename, "rb") as f:
        return f.read()

def write_file(filename, data):
    with open(filename, "wb") as f:
        f.write(data)

def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def encrypt(key, plaintext, key_file):
    ciphertext = xor_bytes(key, plaintext)
    write_file(key_file, key) # write the key to the specified file for later decryption
    return ciphertext

def decrypt(key, ciphertext):
    plaintext = xor_bytes(key, ciphertext)
    return plaintext

def main():
    if len(sys.argv) != 5:
        print("Usage: {} (encrypt|decrypt) input_file output_file key_file".format(sys.argv[0]))
        return

    mode = sys.argv[1].lower()
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key_file = sys.argv[4]

    if mode == "encrypt":
        plaintext = read_file(input_file)
        key = os.urandom(len(plaintext))
        ciphertext = encrypt(key, plaintext, key_file)
        write_file(output_file, ciphertext)
    elif mode == "decrypt":
        ciphertext = read_file(input_file)
        key = read_file(key_file)
        plaintext = decrypt(key, ciphertext)
        write_file(output_file, plaintext)
    else:
        print("Invalid mode: {}".format(mode))
        return

if __name__ == "__main__":
    main()
