#!/usr/bin/python
##### THIS SCRIPT IS THEORETICALLY A (ONE-TIME-PAD Cipher) As it is a sub cipher except ever occurence uses a different sub therfore it is a OTP Cipher (SUB ON CRACK)
import sys
import random

def encrypt(input_file, output_file, substitutions):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        used_subs = {k: set() for k in substitutions}  # initialize the set of used substitutions for each character to empty
        for line in f_in:
            line = line.strip()
            for c in line.decode('utf-8'):
                if c in substitutions:
                    sub_list = substitutions[c]
                    num_subs = len(sub_list)
                    unused_subs = list(set(sub_list) - used_subs[c])
                    if not unused_subs:
                        # All substitutions for this character have been used, reset the set of used substitutions
                        unused_subs = sub_list
                        used_subs[c] = set()
                    sub = random.choice(unused_subs)
                    used_subs[c].add(sub)
                    f_out.write(sub.encode('utf-8'))
                else:
                    f_out.write(c.encode('utf-8'))
            f_out.write(b'\n')


def decrypt(input_file, output_file, substitutions, substitute_length=None):
    # Determine the substitute length if not provided
    if substitute_length is None:
        with open(input_file, 'rb') as f_in:
            first_substitute = f_in.read(len(next(iter(substitutions.values()))[0].encode('utf-8')))
        substitute_length = len(first_substitute.decode('utf-8'))
    # Build the decryption table by reversing the order of the substitutions for each ciphertext character
    decryption_table = {}
    for k, v in substitutions.items():
        sub_list = v
        sub_list.reverse()
        for i, sub in enumerate(sub_list):
            ciphertext_char = sub_list[i]  # changed line
            if ciphertext_char not in decryption_table:
                decryption_table[ciphertext_char] = k
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        buffer = ''
        for char in f_in.read().decode('utf-8'):
            if char.isspace():
                f_out.write(char.encode('utf-8'))
                continue
            buffer += char
            if len(buffer) == substitute_length:
                if buffer in decryption_table:
                    f_out.write(decryption_table[buffer].encode('utf-8'))
                else:
                    # Use the most common substitution if there are multiple possible plaintext characters
                    candidate_chars = []
                    for sub in buffer:
                        if sub in decryption_table:
                            candidate_chars.append(decryption_table[sub])
                    if len(candidate_chars) == 1:
                        f_out.write(candidate_chars[0].encode('utf-8'))
                    elif len(candidate_chars) > 1:
                        most_common_char = max(set(candidate_chars), key=candidate_chars.count)
                        f_out.write(most_common_char.encode('utf-8'))
                    else:
                        default_char = substitutions[next(iter(substitutions.keys()))][0]
                        f_out.write(default_char.encode('utf-8'))
                buffer = ''
        if len(buffer) > 0:
            last_char = buffer[-1]
            if not last_char.isspace():
                candidate_chars = []
                for sub in buffer:
                    if sub in decryption_table:
                        candidate_chars.append(decryption_table[sub])
                if len(candidate_chars) == 1:
                    f_out.write(candidate_chars[0].encode('utf-8'))
                elif len(candidate_chars) > 1:
                    most_common_char = max(set(candidate_chars), key=candidate_chars.count)
                    f_out.write(most_common_char.encode('utf-8'))
                else:
                    default_char = substitutions[next(iter(substitutions.keys()))][0]
                    f_out.write(default_char.encode('utf-8'))
        f_out.write(b'\n')


def handleerrors():
    print('Usage: python substitution_cipher.py <encrypt/decrypt> <input_file> <output_file> <substitutions_file>')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        handleerrors()
    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    substitutions_file = sys.argv[4]
    substitutions = {}
    with open(substitutions_file, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            plain_char = parts[0]
            subs = parts[1:]
            if plain_char in substitutions:
                substitutions[plain_char].extend(subs)
            else:
                substitutions[plain_char] = subs
    if operation == 'encrypt':
        encrypt(input_file, output_file, substitutions)
    elif operation == 'decrypt':
        decrypt(input_file, output_file, substitutions)
    else:
        handleerrors()
