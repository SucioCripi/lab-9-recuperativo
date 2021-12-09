from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP


def rsa_encrypt_decrypt():
    global decrypted_text
    key = RSA.generate(2048)
    private_key = key.export_key('PEM')
    public_key = key.publickey().exportKey('PEM')
    message = textoencriptado
    message = str.encode(message)

    rsa_public_key = RSA.importKey(public_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_text = rsa_public_key.encrypt(message)
    # encrypted_text = b64encode(encrypted_text)

    print('el mensaje encriptao es : {}'.format(str(encrypted_text)))

    rsa_private_key = RSA.importKey(private_key)
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    decrypted_text = rsa_private_key.decrypt(encrypted_text)
    decrypted_text = decrypted_text
    print('el mensaje decriptao es : {}'.format(decrypted_text))


def rot13(msj):
    a = "abcdefghijklmnopqrstuvwxyz"
    temp = ""
    global textoencriptado
    for i in msj:
        if i in a:
            if a.index(i) <= 12:
                temp += a[a.index(i) + 13]
            else:
                temp += a[a.index(i) - 13]
        else:
            temp += i
    textoencriptado = temp
    print(textoencriptado)


def antirot13(msj):
    a = "nopqrstuvwxyzabcdefghijklm"
    temp = ""
    global textoencriptado
    for i in msj:
        if i in a:
            if a.index(i) <= 12:
                temp += a[a.index(i) + 13]
            else:
                temp += a[a.index(i) - 13]
        else:
            temp += i
    textoencriptado = temp
    print(textoencriptado)


# rot13 y luego RSA

global mensaje
global textoencriptado

with open('mensaje de entrada.txt', 'r') as abrir_mensaje_entrada:
    mensaje = str(abrir_mensaje_entrada.read())
    print("el texto inicial es: ", mensaje)
    textoencriptado = mensaje

rot13(mensaje)

rsa_encrypt_decrypt()
antirot13(textoencriptado)
###se guarda en mensaje de salida.txt

with open('mensaje de salida.txt', 'w') as escribir_mensaje_salida:
    escribicion = escribir_mensaje_salida.write(textoencriptado[::-1])
