from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

user_text = "sixteen sixteen :admin<true:"

"""---------------------------- Task 1 --------------------------------"""
# function to encrypt a file
"""maybe pull out encryption of message to have encrypt_message 
function and encrypt_file function that calls encrypt_message?"""
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
            f.write(cipher_block)
            if mode == "CBC":
                scrambler = cipher_block


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



if __name__ == '__main__':
    print('Starting...')
    print("Encrypting file using ECB and CBC")
    key = get_random_bytes(16)
    IV = get_random_bytes(16)
    encrypt_file('mustang.bmp', key, "unneeded", "ECB")
    encrypt_file('mustang.bmp', key, IV, "CBC")
    print("Encryption Finished\nNew encrypted files: cipherECB.bmp and cipherCBC.bmp")

    #decrypt_CBC(key, IV)
    #decrypt_ECB(key)
