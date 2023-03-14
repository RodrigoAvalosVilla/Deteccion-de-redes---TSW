# 1) Pedir Host - ya
# 2) Detectar host - ya
# 3) Mapear red - ya
# 4) Guardar red en bdd - ya
# 5) Mostrar bdd - ya 
# 6) Obtener pagina web - en proceso

# Practica 2.2 - Detección de red

# ------------- LIBRERIAS ---------------
import os
import nmap
import socket
import pymongo
from pymongo import MongoClient

#

# ------------- FUNCIONES ---------------

# Funcion para realizar un ping de un enlace
def hacerPing(ruta):
    return os.system("ping -n 1 " + ruta)

# Funcion que retorna los puertos y su estado en forma de diccionario de datos
def mapeoPuertos(ruta):
    print("\nMapeando la ruta: ", ruta, " ...")
    ip = socket.gethostbyname(ruta)

    nm = nmap.PortScanner()

    print("Ip: ", ip)

    nm.scan(ip, arguments='-p-')

    print("Estado: ", nm[ip].state())

    diccionario = {}

    for host in nm.all_hosts():
        print('Puertos abiertos en', host)
        for port in nm[host]['tcp'].keys():
            llave = str(port)
            estado = nm[host]['tcp'][port]['state']
            diccionario.update({llave: estado})
    
    return diccionario

# Funcion para insertar lo obtenido al mapear el enlace
def insertarDB(datos, doc):
    cliente = MongoClient()
    db = cliente['red']
    coleccion = db[doc]
    resultado = coleccion.insert_one(datos)

    return resultado.acknowledged

# Funcion para mostrar el contenido de la BDD
def mostrarDB(doc):
    print("\nMostrando la BDD...")
    cliente = MongoClient()
    db = cliente['red']
    coleccion = db[doc]

    documentos = coleccion.find()

    for documento in documentos:
        print(documento)








# ------------- CODIGO ---------------
ruta = input("Dame la IP o nombre del dominio: ")

if hacerPing(ruta) == 0:
    # Si al hacer ping da 0, mapeamos la ruta
    print("\nPing exitoso en ", ruta)
    resultadoMapeo = mapeoPuertos(ruta)
    # Una vez mapeado, lo insertamos a la bdd de mongo
    resultadoInsert = insertarDB(resultadoMapeo, ruta)
    if resultadoInsert:
        mostrarDB(ruta)
    else:
        print("No se inserto correctamente")
else:
    # Sino la ruta no es accesible y fin del programa
    print("Dominio o IP no valido...")