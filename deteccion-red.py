# 1) Pedir Host
# 2) Detectar host
# 3) Mapear red
# 4) Guardar red en bdd
# 5) Mostrar bdd
# 6) Obtener pagina web

# Practica 2.2 - Detección de red

# ------------- LIBRERIAS ---------------
import os


# ------------- FUNCIONES ---------------
def hacerPing(ruta):
    return os.system("ping -n 1 " + ruta)

# Cosas por hacer al método de mapeo:
# 1) Obtener el resultado del comando para manejar su contenido
# 2) Retornar el resultado en un diccionario de datos.
def mapeoPuertos(ruta):
    comando = "nmap " + str(ruta)

    return os.system(comando)

# ------------- CODIGO ---------------
ruta = input("Dame la IP o nombre del dominio: ")

if hacerPing(ruta) == 0:
    # Si al hacer ping da 0, mapeamos la ruta
    print("RESULTADO: \n", mapeoPuertos(ruta))
else:
    # Sino la ruta no es accesible y fin del programa
    print("Dominio o IP no valido...")