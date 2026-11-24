# registro-de-archivos

Módulo en Python que lleva el registro de los archivos de una carpeta usando su huella **SHA-256**: en cada corrida compara contra el registro anterior (guardado en `registro.csv`) y marca cada archivo como **NUEVO**, **SIN CAMBIOS** o **CAMBIO**.

Es el módulo de registro de mi exportador local de respaldos: sirve para procesar solo lo que cambió entre una corrida y otra, sin reprocesar todo. Lo escribí como práctica de mi clase de Programación Básica de la maestría, aplicado a un problema real de mi negocio.

## Uso

```bash
python registro.py              # registra la carpeta del propio script
python registro.py C:\MiCarpeta # o la carpeta que se indique
```

También acepta la variable de entorno `REGISTRO_CARPETA`.

## Cómo funciona

1. Lista los archivos de la carpeta con su tamaño.
2. Calcula la huella SHA-256 de cada uno, leyéndolo por bloques de 1 MB.
3. Compara con `registro.csv` y reporta el estado de cada archivo.
4. Guarda el registro actualizado.

Sin dependencias externas: solo la biblioteca estándar de Python (`csv`, `hashlib`, `os`, `sys`).
