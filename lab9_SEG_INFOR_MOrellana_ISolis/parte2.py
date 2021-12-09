import base64
import hashlib
import os
import random

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import number


class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class DiffieHellman(object):
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.generate_keys()

    def get_public_key(self):
        return pow(self.g, self.private_key, self.p)

    def get_shared_secret(self, other_public_key):
        return pow(other_public_key, self.private_key, self.p)

    def generate_keys(self):
        self.private_key = random.randint(1, self.p - 1)
        self.public_key = self.get_public_key()


p = number.getPrime(2048)
g = random.randint(2, p)

Diffie = DiffieHellman(p, g)  ## Cliente
DiffiePub = Diffie.get_public_key()
Diffie2 = DiffieHellman(p, g)  ## Servidor
Diffie2Pub = Diffie2.get_public_key()
LlaveSync = None
if Diffie.get_shared_secret(Diffie2Pub) == Diffie2.get_shared_secret(DiffiePub):  ## Sincronización
    LlaveSync = str(Diffie.get_shared_secret(Diffie2Pub))

with open("archivo de salida.txt", "r") as f:
    RawEncript = f.read()
    print("Mensaje original: " + RawEncript)
KeyAES = str(LlaveSync[:256])  ## Llave de AES 256 caracteres
AESEncrypt = AESCipher(KeyAES)
encriptadoAES = AESEncrypt.encrypt(RawEncript)
print("Mensaje encriptado", encriptadoAES)
with open("mensaje encriptado.txt", "w") as f:  # Se envia el mensaje encriptado por medio del archivo
    f.write(str(encriptadoAES.decode('utf-8')))
with open("mensaje encriptado.txt", "r") as f:  # se lee el archivo y se guarda en una variable nueva para desencriptar
    RawDecript = bytes(f.read(), 'utf-8')
desencriptadoAES = AESEncrypt.decrypt(RawDecript)  # se desencripata el mensaje
print("Mensaje desencriptado", desencriptadoAES)  # se imprime el mensaje desencriptado
with open("mensaje de vuelva.txt", "w") as f:  # se guarda el mensaje desencriptado en un archivo
    f.write(str(desencriptadoAES[::-1]))
os.remove("mensaje encriptado.txt")  # se elimina el archivo encriptado que fue el canal de comunicación
