# https://www.youtube.com/watch?v=8PzDfykGg_g
from Crypto.Cipher import AES
import base64
import os

def decryption(encryptedString):
    PADDING = '{'
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    key = ''
    cipher = AES.new(key)
    decoded = DecodeAES(cipher, encryptedString)
    print(decoded)
