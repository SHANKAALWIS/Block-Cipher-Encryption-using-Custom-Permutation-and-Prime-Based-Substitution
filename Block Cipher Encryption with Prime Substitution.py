#Shanka Alwis 10685892
#Thiveekshan Gunasegaran 10685900


import random
import string

def generate_random_iv(length=16):
    """Generates a random initialization vector of the specified length."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length)).encode('utf-8')

#---------------------------------------------------------------

def xor_bytes(bytes1, bytes2):
    """Performs XOR operation on two byte strings."""
    return bytes([b1 ^ b2 for b1, b2 in zip(bytes1, bytes2)])

#---------------------------------------------------------------

def convert_to_ascii(text):
    """Converts a text string to a list of ASCII values."""
    return [ord(char) for char in text]

#---------------------------------------------------------------

def fixed_permutation(input_list):
    """Permute the elements of a list according to a fixed order."""
    permutation_order = [1, 3, 0, 2, 5, 4, 7, 6]
    return [input_list[i] for i in permutation_order]

#---------------------------------------------------------------

def prime_number_substitution(input_byte, prime):
    """Perform substitution using a prime number."""
    return (input_byte * prime) % 256

#---------------------------------------------------------------

def key_schedule(main_key):
    """Derives round keys from the main key using a rotation-based approach."""
    round_keys = []
    key_length = len(main_key)

    # Generate at least 8 round keys
    for i in range(8):
        start = (i * 8) % key_length
        round_key = main_key[start:start+8]
        
        # If the round key is shorter than 8 bytes, pad it with the beginning of the main key
        if len(round_key) < 8:
            round_key += main_key[:8-len(round_key)]
        
        round_keys.append(round_key)

    return round_keys

#---------------------------------------------------------------


def encrypt_block(plaintext_block, key, iv):
    """Encrypts a plaintext block using the specified key and IV."""
    # Convert plaintext block to ASCII values (byte list)
    plaintext_bytes = convert_to_ascii(plaintext_block)
    iv_bytes = list(iv)  # Ensure iv_bytes is a list of integers

    # Initial XOR with IV
    ciphertext_block = xor_bytes(plaintext_bytes, iv_bytes)

    # Apply the encryption rounds
    round_keys = key_schedule(key.encode('utf-8'))
    for i in range(8):
        # Permutation
        ciphertext_block = fixed_permutation(ciphertext_block)

        # Prime number substitution
        ciphertext_block = [prime_number_substitution(byte, prime) for byte in ciphertext_block]

        # Key addition (XOR with the round key)
        ciphertext_block = xor_bytes(ciphertext_block, list(round_keys[i]))

    return ciphertext_block

#---------------------------------------------------------------

def encrypt_message(plaintext_message, key):
    """Encrypts a plaintext message using the specified key."""
    iv = generate_random_iv()
    ciphertext_message = []
    previous_ciphertext = iv

    # Ensure the message is divided into blocks of length 8
    for i in range(0, len(plaintext_message), 8):
        plaintext_block = plaintext_message[i:i+8].ljust(8)  # Padding if necessary
        ciphertext_block = encrypt_block(plaintext_block, key, previous_ciphertext)
        ciphertext_message.append(ciphertext_block)
        previous_ciphertext = bytes(ciphertext_block)

    return b''.join(ciphertext_message)  # Combine all blocks into a single bytes object

#---------------------------------------------------------------

# Example usage
print("########### BLOCK CIPHER ENCRYPTION DEMONSTRATION #############")
print(" ")
plaintext_message = input("Please enter the text you would like to encrypt :")
print(" ")
while True:
    key = input("Please enter a 16-character encryption key; ")
    if len(key) == 16:
        break
    else:
        print("Invaild input. The key must be exactly 16 charcaters long. please try again : ")
print(" ")        
print("processing encryption ..............................")

prime = 173 

ciphertext_message = encrypt_message(plaintext_message, key)
print(" ")
print("The encrypted message (cipher text) is :",ciphertext_message.hex())  # Print ciphertext as a hexadecimal string
