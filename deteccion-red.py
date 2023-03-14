# 1) Pedir Host - ya
# 2) Detectar host - ya
# 3) Mapear red - ya
# 4) Guardar red en bdd - en proceso
# 5) Mostrar bdd
# 6) Obtener pagina web

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
    print("Mapeando la ruta: ", ruta, " ...")
    ip = socket.gethostbyname(ruta)

    nm = nmap.PortScanner()

    print("Ip: ", ip)

    nm.scan(ip, arguments='-p-')

    print("State: ", nm[ip].state())

    diccionario = {"Enlace": ruta}

    for host in nm.all_hosts():
        print('Puertos abiertos en', host)
        for port in nm[host]['tcp'].keys():
            estado = nm[host]['tcp'][port]['state']
            diccionario.update({port: estado})
    
    return diccionario

# Funcion para insertar lo obtenido al mapear el enlace
def insertarDB(datos):
    cliente = MongoClient()
    db = cliente['red']
    coleccion = db['puertos']
    resultado = coleccion.insert_one(datos)

    return resultado.acknowledged

# Funcion para mostrar el contenido de la BDD
def mostrarDB():
    cliente = MongoClient()
    db = cliente['red']
    coleccion = db['puertos']
# ------------- CODIGO ---------------
ruta = input("Dame la IP o nombre del dominio: ")

if hacerPing(ruta) == 0:
    # Si al hacer ping da 0, mapeamos la ruta
    resultadoMapeo = mapeoPuertos(ruta)
    # Una vez mapeado, lo insertamos a la bdd de mongo
    resultadoInsert = insertarDB(resultadoMapeo)
    if resultadoInsert:
        mostrarDB()
    else:
        print("No se inserto correctamente")
else:
    # Sino la ruta no es accesible y fin del programa
    print("Dominio o IP no valido...")