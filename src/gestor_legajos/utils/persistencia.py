import pickle
import glob
import os
import json
from pathlib import Path

# Este archivo
_RUTA_ARCHIVO = Path(__file__).resolve()

# -- RUTAS INTERNAS --
# src/gestor_legajos
_RUTA_APP = _RUTA_ARCHIVO.parents[1]

RUTA_ASSETS = _RUTA_APP / "assets"
RUTA_TEMPLATES = RUTA_ASSETS / "templates"
RUTA_DEFAULTS = RUTA_ASSETS / "defaults"

# -- RUTAS EXTERNAS --
RUTA_PROYECTO = _RUTA_ARCHIVO.parents[3]
RUTA_STORAGE = RUTA_PROYECTO / "storage"
RUTA_DATA = RUTA_STORAGE / "data"
RUTA_TEMP = RUTA_STORAGE / "temp"
RUTA_OUT = RUTA_STORAGE / "out"


def obtener_directorio_empresas():
    directorio = RUTA_DATA / "empresas"
    directorio.mkdir(parents=True, exist_ok=True)
    return directorio


def obtener_directorio_out():
    directorio = RUTA_OUT
    directorio.mkdir(parents=True, exist_ok=True)
    return directorio


def obtener_ruta_templates(nombre_archivo: str) -> Path:
    return RUTA_TEMPLATES / nombre_archivo


def obtener_ruta_defaults(nombre_archivo: str) -> Path:
    return RUTA_DEFAULTS / nombre_archivo


def obtener_lista_empresas():
    directorio_datos = obtener_directorio_empresas()
    lista_archivos = glob.glob(f"{directorio_datos}/*.dat")
    lista_empresas = list()
    for archivo in lista_archivos:
        with open(archivo, "rb") as archivo_empresa:
            empresa = pickle.load(archivo_empresa)
            lista_empresas.append(empresa)
    return lista_empresas


def buscar_empresa(lista_empresas, nombre_empresa):
    for empresa in lista_empresas:
        if empresa.nombre_empresa.lower() == nombre_empresa.lower():
            return empresa


def guardar_empresa(empresa):
    directorio_datos = obtener_directorio_empresas()
    with open(f"{directorio_datos}/{empresa.apellido_dueño}.dat", "wb") as archivo:
        pickle.dump(empresa, archivo)


def validar_empresa(empresa):
    return empresa if \
        empresa.nombre_empresa != "" and \
        empresa.cuit_empresa != "" and \
        empresa.nombre_dueño != "" and \
        empresa.apellido_dueño != "" and \
        empresa.domicilio.calle != "" and \
        empresa.domicilio.numero != "" and \
        empresa.domicilio.codigo_postal != "" and \
        empresa.domicilio.localidad != "" and \
        empresa.domicilio.provincia != "" and \
        empresa.convenio != "" and \
        empresa.sindicato != "" \
        else None


def crear_empresa(empresa):
    if validar_empresa(empresa):
        guardar_empresa(empresa)
        return 1


def validar_empleado(empleado):
    return empleado if empleado.numero_legajo != "" and \
        empleado.persona.nombre != "" and \
        empleado.persona.apellido != "" and \
        empleado.persona.fecha_nacimiento != "" and \
        empleado.persona.nacionalidad != "" and \
        empleado.persona.cuil != "" and \
        empleado.persona.domicilio.calle != "" and \
        empleado.persona.domicilio.numero != "" and \
        empleado.persona.domicilio.codigo_postal != "" and \
        empleado.persona.domicilio.localidad != "" and \
        empleado.persona.domicilio.provincia != "" and \
        empleado.persona.obra_social != "" and \
        empleado.persona.sexo != "" and \
        empleado.persona.estado_civil != "" and \
        empleado.fecha_ingreso != "" and \
        empleado.sueldo != "" and \
        empleado.categoria != "" \
        else None


def guardar_obra_social(lista_obras_sociales, obra_social):
    lista_obras_sociales.append(obra_social)
    with open(obtener_ruta_defaults("obras_sociales.json") , "w") as archivo:
        json.dump(lista_obras_sociales, archivo)


def leer_obras_sociales():
    with open(obtener_ruta_defaults("obras_sociales.json"), "r") as archivo:
        lista_obras_sociales = json.load(archivo)
    return lista_obras_sociales


def guardar_convenio(lista_convenios, convenio=None):
    lista_convenios.append(convenio) if convenio else None
    with open(obtener_ruta_defaults("convenios.dat"), "wb") as archivo:
        for convenio in lista_convenios:
            pickle.dump(convenio, archivo)


def leer_convenios():
    lista_convenios = list()
    nombre_archivo = obtener_ruta_defaults("convenios.dat")
    with open(nombre_archivo, "rb") as archivo:
        tamaño_archivo = os.path.getsize(nombre_archivo)
        while archivo.tell() < tamaño_archivo:
            convenio = pickle.load(archivo)
            lista_convenios.append(convenio)
        return lista_convenios
    

def guardar_sindicato(lista_sindicatos, sindicato):
    lista_sindicatos.append(sindicato)
    with open(obtener_ruta_defaults("sindicatos.json"), "w") as archivo:
        json.dump(lista_sindicatos, archivo)


def leer_sindicatos():
    with open(obtener_ruta_defaults("sindicatos.json"), "r") as archivo:
        lista_sindicatos = json.load(archivo)
    return lista_sindicatos


def leer_opciones_pdfs():
    with open(obtener_ruta_defaults("pdfs_para_legajo.json"), "r") as archivo:
        lista_pdfs = json.load(archivo)
    return lista_pdfs
