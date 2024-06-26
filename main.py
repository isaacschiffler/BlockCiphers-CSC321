from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from urllib.parse import quote


"""---------------------------- Task 1 --------------------------------"""

"""Function to encrypt a file. Supports ECB and CBC as its mode."""
def encrypt_file(filename, key, IV, mode):
    scrambler = IV
    with open(filename, 'rb') as f:
        contents = f.read()

    # save and remove header from bmp data
    header = contents[:54]
    contents = contents[54:]

    if mode == "CBC":
        new_file_name = 'cipherCBC.bmp'
    else:
        new_file_name = 'cipherECB.bmp'

    # Open the file in write mode ('w') to clear its contents
    with open(new_file_name, 'w'):
        pass

    # open cipher text file and write each block as encrypted
    # change naming convention to customize for specified file we're encrypting at some point...
    with open(new_file_name, 'ab') as f:
        f.write(header)  # append header to encrypted file
        cipher = AES.new(key, AES.MODE_ECB)
        # iterate over every block
        while len(contents) != 0:
            # get blocks
            block = contents[:16]
            contents = contents[16:]
            cipher_block = encrypt_block(cipher, block, scrambler, mode)
            if mode == "CBC":
                scrambler = cipher_block
            f.write(cipher_block)


"""This function takes a 128 bit block of contents and encrypts it based on the mode"""
def encrypt_block(cipher, block, scrambler, mode):
    # check if padding is needed
    if len(block) != 16:
        bytes_needed = 16 - len(block)  # calculate number of bytes needing padding
        # add padding
        padding_byte = bytes([bytes_needed])
        block += padding_byte * bytes_needed  # adds the byte representation of the number of bytes padded
    if mode == "CBC":
        new = bytearray(len(block))
        # xor with scrambler (init IV)
        for i in range(0, len(block)):
            new[i] = block[i] ^ scrambler[i]
        block = new
    # encrypt new block
    cipher_block = cipher.encrypt(block)
    return cipher_block

# function to decrypt CBC to double check it works...
def decrypt_CBC(key, IV):
    with open('cipherCBC.bmp', 'rb') as f:
        encrypted_contents = f.read()

    # Initialize AES cipher object with the key and IV
    header = encrypted_contents[:54]
    encrypted_contents = encrypted_contents[54:]
    cipher = AES.new(key, AES.MODE_CBC, IV)

    # Decrypt the contents using AES in CBC mode
    decrypted_contents = cipher.decrypt(encrypted_contents)

    # Unpad the decrypted contents
    unpadded_contents = unpad(decrypted_contents, AES.block_size)

    # Write the decrypted contents to a new BMP file
    with open('decryptedCBC.bmp', 'wb') as f:
        f.write(header)
        f.write(unpadded_contents)


def decrypt_ECB(key):
    with open('cipherECB.bmp', 'rb') as f:
        encrypted_contents = f.read()

    # Initialize AES cipher object with the key and IV
    header = encrypted_contents[:54]
    encrypted_contents = encrypted_contents[54:]
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt the contents using AES in CBC mode
    decrypted_contents = cipher.decrypt(encrypted_contents)

    # Unpad the decrypted contents
    unpadded_contents = unpad(decrypted_contents, AES.block_size)

    # Write the decrypted contents to a new BMP file
    with open('decryptedECB.bmp', 'wb') as f:
        f.write(header)
        f.write(unpadded_contents)


"""---------------------------- Task 2 --------------------------------"""

"""submit() URL encodes any ';', '=' chars in the user string, 
appends and prepends given strings, pads the string (PKCS#7), 
and returns the CBC encryption of the new string"""
def submit(string, cipher, scrambler):
    # URL encode ';' and '=' from user string
    encoded_semicolon = quote(';')
    encoded_equal = quote('=')
    string = string.replace(';', encoded_semicolon).replace('=', encoded_equal)

    # prepend and append
    new_string = "userid=456; userdata=" + string + ";session-id=31337"
    print("Full message to encrypt: " + new_string + "\n")

    # change to byte array
    message = new_string.encode('utf-8')

    # pad new string
    bytes_needed = 16 - len(new_string) % 16
    padding_byte = bytes([bytes_needed])
    message += padding_byte * bytes_needed  # adds the byte representation of the number of bytes padded

    # encrypt padded message
    encrypted_message = bytearray()
    while len(message) != 0:
        block = message[:16]
        encrypted_block = encrypt_block(cipher, block, scrambler, "CBC")
        encrypted_message += encrypted_block
        message = message[16:]
        scrambler = encrypted_block

    return encrypted_message


"""Decrypt the given encrypted message and return True if ;admin=true;
exists in the decrypted message, False otherwise"""
def verify(encrypt):
    # Decrypt message
    cipher = AES.new(key, AES.MODE_CBC, IV)
    # Decrypt the contents using AES in CBC mode
    decrypted_contents = cipher.decrypt(encrypt)

    # Unpad the decrypted contents (if necessary)
    unpadded_contents = unpad(decrypted_contents, AES.block_size)

    # Manual decryption instead of .decode() because of errors in scrambling of block 2
    message = ""
    for byte in unpadded_contents:
        message += chr(byte)

    #message = unpadded_contents.decode('utf-8')

    print("Decrypted Message: " + message)

    # parse for ;admin=true; in decrypted message
    if ";admin=true;" in message:
        return True
    else:
        return False


"""Function to flip bits in specified positions of block 2 of encrypted 
message to alter the contents of associated positions of block 3 and to 
produce ;admin=true; in the decrypted message"""
def flip_bit(encrypted_msg):
    # block_2_encrypted is the scrambler used for block 3 which is where our target is
    block_2_encrypted = encrypted_msg[16:32]
    # print("original block 2 encrypted: " + str(block_2_encrypted))

    # flip : and < to ; and =
    # x = Pi ^ y; y = Pi'
    y = bytearray(b';admin=true;;ses')  # what we want (Pi')
    p_i = bytearray(b':admin<true:;ses')  # what we have
    x = bytearray()
    for i in range(0, len(p_i)):
        x.append(p_i[i] ^ y[i])
    # print("x: " + str(x))  # for debugging

    # Ci-1' = Ci-1 ^ x
    new_block_2 = bytearray()
    for i in range(0, len(block_2_encrypted)):
        new_block_2.append(block_2_encrypted[i] ^ x[i])
    # print("new block 2 encrypted (Ci-1'): " + str(new_block_2))  # for debugging
    new_encrypted_msg = encrypted_msg[:16] + new_block_2 + encrypted_msg[32:]

    return new_encrypted_msg



if __name__ == '__main__':
    print('Starting...')
    key = get_random_bytes(16)
    IV = get_random_bytes(16)
    t1 = input("\nExecute Task 1? (y/n) ")
    if t1 == 'y':
        print("------------------------- Task 1 -------------------------\n")
        print("Encrypting file using ECB and CBC")
        encrypt_file('mustang.bmp', key, "unneeded", "ECB")
        encrypt_file('mustang.bmp', key, IV, "CBC")
        print("Encryption Finished\nNew encrypted files: cipherECB.bmp and cipherCBC.bmp")

        # decrypt_CBC(key, IV)
        # decrypt_ECB(key)

    t2 = input("\nExecute Task 2? (y/n) ")
    if t2 == 'y':
        print("\n\n------------------------- Task 2 -------------------------\n")
        # using this string so :admin<true: is at the start of the third block
        user_string = "sixteen is :admin<true:"
        print("Initial user string: " + user_string + "\n")

        cipher = AES.new(key, AES.MODE_ECB)

        print("Encrypting...")
        encrypted_message = submit(user_string, cipher, IV)

        # print("Encrypted Message: " + str(encrypted_message)) # for debugging

        print("Bit flipping...\n")
        encrypted_message = flip_bit(encrypted_message)
        #print("New full encrypted message: " + str(encrypted_message)) # for debugging

        print("Decrypting and checking for \";admin=true;\"...")
        result = verify(encrypted_message)
        print("\nVerify returned: " + str(result) + "!")
        if result:
            print("The decrypted message contains the string \";admin=true;\"")
        else:
            print("The decrypted message does not contain the string \";admin=true;\"")

    print("\nComplete!")