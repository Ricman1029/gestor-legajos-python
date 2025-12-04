import os
import pymupdf
import calendar
from gestor_legajos.entidades.empresa import Empresa, Empleado, Domicilio
from gestor_legajos.entidades.persona import Persona
from gestor_legajos.utils.helpers import insertar_texto
from gestor_legajos.utils.persistencia import obtener_ruta_templates, obtener_directorio_out


def formulario_anses(empleado, empresa):
    pdf_path = obtener_ruta_templates("pdf_anses.pdf")
    pdf = pymupdf.open(pdf_path)
    pagina = pdf[0]
    tamaño_fuente = 10

    # EMPLEADO
    # Apellido y nombre - Fecha nacimiento - Nacionalidad
    insertar_texto(pagina, 60, 135, f"{empleado.persona.apellido} {empleado.persona.nombre}", tamaño_fuente)
    insertar_texto(pagina, 360, 135, empleado.persona.dia_nacimiento(), tamaño_fuente)
    insertar_texto(pagina, 389, 135, empleado.persona.mes_nacimiento(), tamaño_fuente)
    insertar_texto(pagina, 420, 135, empleado.persona.año_nacimiento()[2:], tamaño_fuente)
    insertar_texto(pagina, 450, 134, empleado.persona.nacionalidad, tamaño_fuente)

    # CUIL - DNI - Sexo - Estado Civil
    insertar_texto(pagina, 60, 163, empleado.persona.cuil, tamaño_fuente)
    insertar_texto(pagina, 210, 163, empleado.persona.dni(), tamaño_fuente)
    insertar_texto(pagina, 365, 163, empleado.persona.sexo, tamaño_fuente)

    # Calle - Número
    insertar_texto(pagina, 180, 180,
                   f"{empleado.persona.domicilio.calle} {empleado.persona.domicilio.numero}", tamaño_fuente)

    # Piso - Depto. - Código Postal - Localidad - Provincia
    insertar_texto(pagina, 60, 207, empleado.persona.domicilio.piso, tamaño_fuente)
    insertar_texto(pagina, 140, 207, empleado.persona.domicilio.departamento, tamaño_fuente)
    insertar_texto(pagina, 220, 207, empleado.persona.domicilio.codigo_postal, tamaño_fuente)
    insertar_texto(pagina, 290, 207, empleado.persona.domicilio.localidad, tamaño_fuente)
    insertar_texto(pagina, 430, 207, empleado.persona.domicilio.provincia, tamaño_fuente)

    # EMPRESA
    # Razón Social - CUIT
    texto = f"""{empresa.nombre_empresa}"""
    pagina.insert_htmlbox(
        pymupdf.Rect(x0=50, x1=270, y0=263, y1=276),
        texto,
        css="* {font-family:helvetica;}",
        scale_low=0,
    )
    # insertar_texto(pagina, 57, 274, empresa.nombre_empresa, 9)
    insertar_texto(pagina, 300, 274, empresa.cuit_empresa, tamaño_fuente)

    # Calle - Número
    insertar_texto(pagina, 177, 291,
                   f"{empresa.domicilio.calle} {empresa.domicilio.numero}", tamaño_fuente)

    # Piso - Depto. - Código postal - Localidad - Provincia
    insertar_texto(pagina, 60, 317, empresa.domicilio.piso, tamaño_fuente)
    insertar_texto(pagina, 140, 317, empresa.domicilio.departamento, tamaño_fuente)
    insertar_texto(pagina, 220, 317, empresa.domicilio.codigo_postal, tamaño_fuente)
    insertar_texto(pagina, 290, 317, empresa.domicilio.localidad, tamaño_fuente)
    insertar_texto(pagina, 430, 317, empresa.domicilio.provincia, tamaño_fuente)

    # Mail
    insertar_texto(pagina, 290, 341, empresa.correo_electronico, tamaño_fuente)

    # Lugar y Fecha
    insertar_texto(pagina, 120, 690, "San Carlos de Bariloche", tamaño_fuente)
    insertar_texto(pagina, 318, 690, empleado.dia_ingreso(), tamaño_fuente)
    insertar_texto(pagina, 373, 690, calendar.month_name[int(empleado.mes_ingreso())].upper(), tamaño_fuente)
    insertar_texto(pagina, 480, 690, empleado.año_ingreso(), tamaño_fuente)

    pdf.copy_page(0, 0)

    directorio_out = obtener_directorio_out()
    destino_archivo = os.path.join(directorio_out, f"anses_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf")
    pdf.save(destino_archivo)


def llenar_formulario_asignacion_familiar(
        empleado: Empleado,
        empresa: Empresa,
        opcion
):
    if opcion == "anses":
        formulario_anses(empleado, empresa)
    else:
        pass


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
    llenar_formulario_asignacion_familiar(
        empleado, empresa, opcion="anses",
    )
