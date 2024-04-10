from Crypto.Cipher import AES
import secrets, binascii

user_text = "sixteen sixteen :admin<true:"


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def key_gen():
    key = secrets.token_bytes(16)
    return binascii.hexlify(key).decode()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(key_gen())
