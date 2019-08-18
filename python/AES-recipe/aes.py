from Crypto.Cipher import AES
import base64
import os

def encryption(privateInfo):
    BLOCK_SIZE = 16
    PADDING = '{'

    pad = lambda s: s +  (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    secret = os.urandom(BLOCK_SIZE)
    print('encryption key: {}'.format(base64.b64encode(secret)))

    cipher = AES.new(secret)

    encoded = EncodeAES(cipher, privateInfo)

    print('Encrypted string: {}'.format(encoded))

encryption('secret message that is very sensitive')
