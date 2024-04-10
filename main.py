import binascii
import secrets

from Crypto.Cipher import AES

user_text = "sixteen sixteen :admin<true:"


def key_IV_gen():
    key = secrets.token_bytes(16)
    return binascii.hexlify(key)


# function to encrypt a file
"""maybe pull out encryption of message to have encrypt_message 
function and encrypt_file function that calls encrypt_message?"""
def encrypt_file_ECB(filename, key):
    with open(filename, 'rb') as f:
        contents = f.read()

    # save and remove header from bmp data
    header = contents[:54]
    contents = contents[54:]

    # open cipher text file and write each block as encrypted
    # change naming convention to customize for specified file we're encrypting at some point...
    with open('cipher.bmp', 'ab') as f:
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


if __name__ == '__main__':
    print('PyCharm')
    key = key_IV_gen()
    encrypt_file_ECB('mustang.bmp', key)
