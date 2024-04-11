from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

user_text = "sixteen sixteen :admin<true:"


# function to encrypt a file
"""maybe pull out encryption of message to have encrypt_message 
function and encrypt_file function that calls encrypt_message?"""
def encrypt_file_ECB(filename, key):
    with open(filename, 'rb') as f:
        contents = f.read()

    # save and remove header from bmp data
    header = contents[:54]
    contents = contents[54:]

    # Open the file in write mode ('w') to clear its contents
    with open('cipherECB.bmp', 'w'):
        pass

    # open cipher text file and write each block as encrypted
    # change naming convention to customize for specified file we're encrypting at some point...
    with open('cipherECB.bmp', 'ab') as f:
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
                """what if the last block takes up 5.5 bytes, what of the padding for the .5 bytes
                up to 6?????? Question for prof"""
                block += padding_byte * bytes_needed  # adds the byte representation of the number of bytes padded

            cipher_block = cipher.encrypt(block)  # encrypt block
            f.write(cipher_block)  # write to cipher file

    return

#function to encrypt a file using CBC block encryption... could combine this function with above to make more clean if we want...
def encrypt_file_CBC(filename, key, IV):
    scrambler = IV
    with open(filename, 'rb') as f:
        contents = f.read()

    # save and remove header from bmp data
    header = contents[:54]
    contents = contents[54:]

    # Open the file in write mode ('w') to clear its contents
    with open('cipherCBC.bmp', 'w'):
        pass

    # open cipher text file and write each block as encrypted
    # change naming convention to customize for specified file we're encrypting at some point...
    with open('cipherCBC.bmp', 'ab') as f:
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
            new = bytearray(len(block))
            # xor with scrambler (init IV)
            for i in range(0, len(block)):
                new[i] = block[i] ^ scrambler[i]
            # encrypt new block
            cipher_block = cipher.encrypt(new)
            f.write(cipher_block)
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
    with open('decrypted.bmp', 'wb') as f:
        f.write(header)
        f.write(unpadded_contents)


if __name__ == '__main__':
    print('PyCharm')
    key = get_random_bytes(16)
    IV = get_random_bytes(16)
    encrypt_file_ECB('mustang.bmp', key)
    encrypt_file_CBC('mustang.bmp', key, IV)

    #decrypt_CBC(key, IV)
