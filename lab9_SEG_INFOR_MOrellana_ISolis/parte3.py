import hashlib
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(".") if isfile(join(".", f))] # Se obtienen todos los archivos del directorio actual

for file in onlyfiles: # se calcula el md5 de cada uno de los ficheros
    with open(file, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
        print("El md5 de " + file + " es: " + md5)