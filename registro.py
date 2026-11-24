# registro.py — Módulo de registro del ExportadorWA
# Autor: Alberto (con guía de Muse). Su parte del proyecto:
# el inventario de archivos con huellas (hash) para no reprocesar.
#
# Ladrillo 1: listar los archivos de la carpeta con su tamaño.
# Ladrillo 2: cada archivo con su huella SHA-256.
# Ladrillo 3: el registro se guarda en registro.csv y compara cambios.

import csv
import hashlib
import os

import sys

# Carpeta a registrar: se puede pasar como argumento, con la variable de
# entorno REGISTRO_CARPETA, o por defecto es la carpeta del propio script.
CARPETA = (
    os.environ.get("REGISTRO_CARPETA")
    or (sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
)
ARCHIVO_REGISTRO = os.path.join(CARPETA, "registro.csv")


def listar_archivos(carpeta):
    """Devuelve una lista de (nombre, tamaño) de los archivos de la carpeta."""
    resultado = []
    for nombre in os.listdir(carpeta):
        ruta = os.path.join(carpeta, nombre)
        if os.path.isfile(ruta):
            resultado.append((nombre, os.path.getsize(ruta)))
    return resultado


def huella(ruta):
    """Calcula la huella SHA-256 de un archivo, leyéndolo por bloques."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        while True:
            bloque = f.read(1024 * 1024)
            if not bloque:
                break
            h.update(bloque)
    return h.hexdigest()


def cargar_registro():
    """Lee el registro guardado: un diccionario {nombre: huella}."""
    registro = {}
    if os.path.exists(ARCHIVO_REGISTRO):
        with open(ARCHIVO_REGISTRO, newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                registro[fila["nombre"]] = fila["huella"]
    return registro


def guardar_registro(datos):
    """Guarda la lista de (nombre, tamaño, huella) en el CSV."""
    with open(ARCHIVO_REGISTRO, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["nombre", "tamano", "huella"])
        for nombre, tamano, h in datos:
            w.writerow([nombre, tamano, h])


anterior = cargar_registro()
actual = []
for nombre, tamano in listar_archivos(CARPETA):
    if nombre == "registro.csv":
        continue  # el registro no se registra a sí mismo
    h = huella(os.path.join(CARPETA, nombre))
    if nombre not in anterior:
        estado = "NUEVO"
    elif anterior[nombre] == h:
        estado = "SIN CAMBIOS"
    else:
        estado = "CAMBIO"
    print(f"{estado:>11}  {nombre}  ->  {tamano} bytes  ->  {h[:12]}...")
    actual.append((nombre, tamano, h))
guardar_registro(actual)
print(f"Total: {len(actual)} archivos. Registro guardado en registro.csv")
