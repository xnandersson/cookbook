# https://www.youtube.com/watch?v=8PzDfykGg_g
import argparse
from Crypto.Cipher import AES
import base64
import os

def decryption(encryptedString, key):
    PADDING = b'{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    print(base64.b64decode(key))
    print(encryptedString)
    cipher = AES.new(base64.b64decode(key))
    decoded = DecodeAES(cipher, encryptedString)
    print(decoded)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("encoded")
    parser.add_argument("key")
    args = parser.parse_args()
    decryption(args.encoded, args.key)
