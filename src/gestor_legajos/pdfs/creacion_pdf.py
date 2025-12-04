import glob, os
# import win32.win32api
import pymupdf
from pypdf import PdfWriter, PdfReader
from pathlib import Path
from gestor_legajos.pdfs.contstancia_entrega import crear_pdf_constancia_entrega
from gestor_legajos.pdfs.asignacion_familiar import llenar_formulario_asignacion_familiar
from gestor_legajos.pdfs.seguro_vida import llenar_formulario_seguro_vida
from gestor_legajos.pdfs.notificacion_art import crear_notificacion_art
from gestor_legajos.pdfs.notificacion_obra_social import crear_notificacion_obra_social
from gestor_legajos.utils.persistencia import obtener_directorio_out
from gestor_legajos.entidades.empresa import Empresa, Empleado, Domicilio
from gestor_legajos.entidades.persona import Persona


def unir_y_guardar_pdfs(ruta, empleado: Empleado, empresa: Empresa, opciones: list):
    crear_pdf_constancia_entrega(empleado, empresa, opciones[0])
    llenar_formulario_asignacion_familiar(empleado, empresa, opciones[1])
    llenar_formulario_seguro_vida(empleado, empresa, opciones[2])
    crear_notificacion_art(empleado, opciones[3])
    crear_notificacion_obra_social(empleado, opciones[4])

    directorio_out = obtener_directorio_out()

    lista_pdfs_a_unir = [
        f"{directorio_out}/legajo_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf",
        f"{directorio_out}/anses_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf",
        f"{directorio_out}/seguro_vida_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf",
        f"{directorio_out}/art_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf",
        f"{directorio_out}/obra_social_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf",
    ]

    pdf_final = pymupdf.open()

    for pdf in lista_pdfs_a_unir:
        pdf = pymupdf.open(pdf)
        pdf_final.insert_pdf(pdf)

    nombre_documento = (
        f"legajo_{empleado.persona.apellido}_{empleado.persona.nombre[0]}_" 
        f"{empleado.dia_ingreso()}{empleado.mes_ingreso()}{empleado.año_ingreso()[2:5]}.pdf"
    )
    ubicacion = ruta / nombre_documento
    pdf_final.save(str(ubicacion))


def crear_carpeta_pdf(empleado: Empleado):
    ruta_base = Path.home() / "Desktop"
    nombre_carpeta = ( 
         f"{empleado.persona.apellido}_{empleado.persona.nombre[0]}_"
         f"{empleado.dia_ingreso()}{empleado.mes_ingreso()}{empleado.año_ingreso()[2:5]}" 
    )

    ruta = ruta_base / nombre_carpeta
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def crear_pdf_final(empleado: Empleado, ruta, pdf):
    nombre_documento = f"legajo_{empleado.persona.apellido}_{empleado.persona.nombre[0]}_" \
                f"{empleado.dia_ingreso()}{empleado.mes_ingreso()}{empleado.año_ingreso()[2:5]}.pdf"

    ubicacion = ruta / nombre_documento

    pdf.write(str(ubicacion))
    pdf.close()
    return str(ubicacion)


def crear_pdf_impresion(pdf: PdfReader, hojas_imprimir):
    pdf_impresion = PdfWriter()

    # Hay que armar un pdf que tenga solo las hojas que se quieren imprimir
    for i, hoja in enumerate(hojas_imprimir):
        if "-" in hoja:
            hojas = hoja.split("-")
        else:
            pass


def imprimir_pdf(pdf_path, hojas_imprimr: list):
    pdf = PdfReader(pdf_path)
    crear_pdf_impresion(pdf, hojas_imprimr)

    # win32.win32api.ShellExecute(0, "print", pdf, None, ".", 0)


def borrar_pdfs():
    directorio_out = obtener_directorio_out()

    lista_pdfs_a_borrar = glob.glob(f"{directorio_out}/*.pdf")
    for pdf in lista_pdfs_a_borrar:
        os.remove(pdf)


def armar_pdf(empleado, empresa, opciones: list):
    ruta = crear_carpeta_pdf(empleado)
    pdf_final = unir_y_guardar_pdfs(ruta, empleado, empresa, opciones)
    borrar_pdfs()









if __name__ == "__main__":
    empleado = Empleado(
        numero_legajo="123",
        persona=Persona(
            nombre="Nombre",
            apellido="Apellido",
            fecha_nacimiento="20/02/2002",
            nacionalidad="Argentina",
            cuil="22-22222222-2",
            domicilio=Domicilio(
                calle="calle",
                numero="111"
            ),
            obra_social="obra social",
            telefono="2944444444"
        ),
        fecha_ingreso="21/02/2002",
        antiguedad="2",
        sueldo="$1.000.000",
        categoria="crack",
    )

    empresa = Empresa(
        nombre_empresa="Razón Social",
        cuit_empresa="30-11111111-1",
        numero_ieric="12341234/7",
        nombre_dueño="Nombre Dueño",
        apellido_dueño="Apellido Dueño",
        dni_dueño="44444444",
        domicilio=Domicilio(
            calle="ni idea",
            numero="menos"
        ),
        convenio="76/75 - CONSTRUCCIÓN",
        sindicato="U.O.C.R.A.",
        telefono="2944555555",
        correo_electronico="empresa@mail.com",
        siglas="EMP"
    )

    armar_pdf(empleado, empresa, ["general", "anses", "galeno", "galeno", "general"])
