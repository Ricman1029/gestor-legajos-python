import os
import pymupdf
from src.utils.helpers import insertar_texto
from src.utils.persistencia import obtener_direccion_carpeta
from src.entidades.empresa import Empleado, Domicilio, Empresa
from src.entidades.persona import Persona


def llenar_pagina_galeno(pagina, empleado, empresa):
    # EMPLEADO
    # Número legajo
    insertar_texto(pagina, 200, 85, empleado.numero_legajo)

    # Nombre y apellido
    insertar_texto(pagina, 130, 140, f"{empleado.persona.nombre} {empleado.persona.apellido}")

    # CUIL - DNI
    insertar_texto(pagina, 80, 161, empleado.persona.cuil)
    insertar_texto(pagina, 270, 161, empleado.persona.dni())

    # Fecha de nacimiento - Fecha de ingreso
    insertar_texto(pagina, 120, 184, empleado.persona.dia_nacimiento())
    insertar_texto(pagina, 142, 184, empleado.persona.mes_nacimiento())
    insertar_texto(pagina, 164, 184, empleado.persona.año_nacimiento()[2:])
    insertar_texto(pagina, 283, 184, empleado.dia_ingreso())
    insertar_texto(pagina, 303, 184, empleado.mes_ingreso())
    insertar_texto(pagina, 325, 184, empleado.año_ingreso()[2:])

    # Domicilio Calle - Número - Piso - Depto.
    insertar_texto(pagina, 160, 204, empleado.persona.domicilio.calle)
    insertar_texto(pagina, 383, 204, empleado.persona.domicilio.numero)
    insertar_texto(pagina, 450, 204, empleado.persona.domicilio.piso)
    insertar_texto(pagina, 530, 204, empleado.persona.domicilio.departamento)

    # Domiclio Codigo Postal - Localidad - Provincia
    insertar_texto(pagina, 70, 224, empleado.persona.domicilio.codigo_postal)
    insertar_texto(pagina, 200, 224, empleado.persona.domicilio.localidad)
    insertar_texto(pagina, 440, 224, empleado.persona.domicilio.provincia)


    # EMPLEADOR
    # Razón Social - CUIT
    insertar_texto(pagina, 115, 269, empresa.nombre_empresa)
    insertar_texto(pagina, 455, 269, empresa.cuit_empresa)

    # Domicilio Calle - Número - Piso - Depto.
    insertar_texto(pagina, 140, 289, empresa.domicilio.calle)
    insertar_texto(pagina, 394, 289, empresa.domicilio.numero)
    insertar_texto(pagina, 455, 289, empresa.domicilio.piso)
    insertar_texto(pagina, 530, 289, empresa.domicilio.departamento)

    # Domiclio Codigo Postal - Localidad - Provincia
    insertar_texto(pagina, 70, 309, empresa.domicilio.codigo_postal)
    insertar_texto(pagina, 200, 309, empresa.domicilio.localidad)
    insertar_texto(pagina, 440, 309, empresa.domicilio.provincia)

    # Lugar y Fecha
    insertar_texto(pagina, 115, 658, empleado.escribir_fecha_ingreso())


def formulario_galeno(empleado: Empleado, empresa: Empresa):
    directorio_auxil = obtener_direccion_carpeta("auxil")
    pdf_path = os.path.join(directorio_auxil, "pdf_galeno.pdf")
    pdf = pymupdf.open(pdf_path)

    llenar_pagina_galeno(pdf[0], empleado, empresa)
    pdf.copy_page(0, 0)
    pdf.copy_page(0, 0)

    return pdf


def llenar_pagina_mapfre(pagina, empleado, empresa):
    # EMPLEADO
    # Legajo
    insertar_texto(pagina, 450, 67, empleado.numero_legajo)

    # Nombre y apellido - CUIL
    insertar_texto(pagina, 105, 111.5, f"{empleado.persona.nombre} {empleado.persona.apellido}")
    insertar_texto(pagina, 450, 111.5, empleado.persona.cuil)

    # DNI - Expedido por
    insertar_texto(pagina, 98, 128, "D.N.I.")
    insertar_texto(pagina, 189, 128, empleado.persona.dni())
    insertar_texto(pagina, 400, 128, "RENAPER")

    # Fecha nacimiento - Fecha ingreso
    insertar_texto(pagina, 113, 145, empleado.persona.dia_nacimiento())
    insertar_texto(pagina, 141, 145, empleado.persona.mes_nacimiento())
    insertar_texto(pagina, 169, 145, empleado.persona.año_nacimiento()[2:])
    insertar_texto(pagina, 496, 145, empleado.dia_ingreso())
    insertar_texto(pagina, 524, 145, empleado.mes_ingreso())
    insertar_texto(pagina, 553, 145, empleado.año_ingreso()[2:])

    # Domicilio Calle - Número - Piso - Depto. - Código Postal
    # insertar_texto(pagina, 130, 165, empleado.persona.domicilio.calle)
    texto = f"""{empleado.persona.domicilio.calle}"""
    pagina.insert_htmlbox(
        pymupdf.Rect(x0=130, x1=270, y0=151, y1=166),
        texto,
        css="* {font-family:helvetica;vertical-align: bottom;}",
        scale_low=0,
    )
    insertar_texto(pagina, 300, 165, empleado.persona.domicilio.numero)
    insertar_texto(pagina, 365, 165, empleado.persona.domicilio.piso)
    insertar_texto(pagina, 440, 165, empleado.persona.domicilio.departamento)
    insertar_texto(pagina, 510, 165, empleado.persona.domicilio.codigo_postal)

    # Domicilio Localidad - Provincia
    insertar_texto(pagina, 145, 182, empleado.persona.domicilio.localidad)
    insertar_texto(pagina, 365, 182, empleado.persona.domicilio.provincia)


    # EMPLEADOR
    # Razón Social
    insertar_texto(pagina, 80, 218, empresa.nombre_empresa)

    # Domicilio Calle - Número - Piso - Depto. - Código Postal
    # insertar_texto(pagina, 130, 236, empresa.domicilio.calle)
    texto = f"""{empresa.domicilio.calle}"""
    pagina.insert_htmlbox(
        pymupdf.Rect(x0=130, x1=270, y0=223, y1=238),
        texto,
        css="* {font-family:helvetica;vertical-align: bottom;}",
        scale_low=0,
    )
    insertar_texto(pagina, 300, 236, empresa.domicilio.numero)
    insertar_texto(pagina, 365, 236, empresa.domicilio.piso)
    insertar_texto(pagina, 440, 236, empresa.domicilio.departamento)
    insertar_texto(pagina, 510, 236, empresa.domicilio.codigo_postal)

    # Domicilio Localidad - Provincia
    insertar_texto(pagina, 145, 253, empresa.domicilio.localidad)
    insertar_texto(pagina, 365, 253, empresa.domicilio.provincia)

    # Lugar y fecha
    insertar_texto(pagina, 100, 382, empleado.escribir_fecha_ingreso())


def formulario_mapfre(empleado: Empleado, empresa: Empresa):
    directorio_auxil = obtener_direccion_carpeta("auxil")
    pdf_path = os.path.join(directorio_auxil, "pdf_mapfre.pdf")
    pdf = pymupdf.open(pdf_path)

    # Elimino los dos primeros dorsos
    pdf.delete_page(1)
    pdf.delete_page(2)

    # Llenamos las 3 páginas
    llenar_pagina_mapfre(pdf[0], empleado, empresa)
    llenar_pagina_mapfre(pdf[1], empleado, empresa)
    llenar_pagina_mapfre(pdf[2], empleado, empresa)

    return pdf


def formulario_andina(empleado: Empleado, empresa: Empresa):
    directorio_auxil = obtener_direccion_carpeta("auxil")
    pdf_path = os.path.join(directorio_auxil, "pdf_andina.pdf")
    pdf = pymupdf.open(pdf_path)
    pagina = pdf[0]
    tamaño_fuente = 10

    # EMPLEADO
    # Apellido y nombre
    insertar_texto(pagina, 130, 85, f"{empleado.persona.apellido} {empleado.persona.nombre}", tamaño_fuente)

    # DNI - Expedido por
    insertar_texto(pagina, 195, 98, "x", tamaño_fuente)
    insertar_texto(pagina, 230, 98, empleado.persona.dni(), tamaño_fuente)
    insertar_texto(pagina, 430, 98, "RENAPER", tamaño_fuente)

    # CUIL - Legajo
    insertar_texto(pagina, 170, 110, empleado.persona.cuil, tamaño_fuente)
    insertar_texto(pagina, 490, 110, empleado.numero_legajo, tamaño_fuente)

    # Fecha nacimiento - Fecha ingreso
    insertar_texto(pagina, 126, 123, empleado.persona.dia_nacimiento(), tamaño_fuente)
    insertar_texto(pagina, 156, 123, empleado.persona.mes_nacimiento(), tamaño_fuente)
    insertar_texto(pagina, 185, 123, empleado.persona.año_nacimiento()[2:], tamaño_fuente)
    insertar_texto(pagina, 486, 123, empleado.dia_ingreso(), tamaño_fuente)
    insertar_texto(pagina, 515, 123, empleado.mes_ingreso(), tamaño_fuente)
    insertar_texto(pagina, 546, 123, empleado.año_ingreso()[2:], tamaño_fuente)

    # Domicilio Calle - Número - Piso - Depto. - Código postal - Localidad - Provincia
    # insertar_texto(pagina, 55, 147, empleado.persona.domicilio.calle, tamaño_fuente)
    texto = f"""{empleado.persona.domicilio.calle}"""
    pagina.insert_htmlbox(
        pymupdf.Rect(x0=51, x1=160, y0=137, y1=149),
        texto,
        css="* {font-family:helvetica;vertical-align: bottom;}",
        scale_low=0,
    )
    insertar_texto(pagina, 180, 147, empleado.persona.domicilio.numero, tamaño_fuente)
    insertar_texto(pagina, 250, 147,
                   f"{empleado.persona.domicilio.piso} {empleado.persona.domicilio.departamento}", tamaño_fuente)
    insertar_texto(pagina, 310, 147, empleado.persona.domicilio.codigo_postal, tamaño_fuente)
    insertar_texto(pagina, 405, 147, empleado.persona.domicilio.localidad, tamaño_fuente)
    insertar_texto(pagina, 505, 147, empleado.persona.domicilio.provincia, tamaño_fuente)

    # EMPRESA
    # Razon social
    insertar_texto(pagina, 140, 179.5, empresa.nombre_empresa, tamaño_fuente)

    # Domicilio Calle - Número - Piso - Depto. - Código postal - Localidad - Provincia
    # insertar_texto(pagina, 55, 204, empresa.domicilio.calle, 9)
    texto = f"""{empresa.domicilio.calle}"""
    pagina.insert_htmlbox(
        pymupdf.Rect(x0=51, x1=160, y0=193, y1=206),
        texto,
        css="* {font-family:helvetica;vertical-align: bottom;}",
        scale_low=0,
    )
    insertar_texto(pagina, 180, 204, empresa.domicilio.numero, tamaño_fuente)
    insertar_texto(pagina, 250, 204,
                   f"{empresa.domicilio.piso} {empresa.domicilio.departamento}", tamaño_fuente)
    insertar_texto(pagina, 310, 204, empresa.domicilio.codigo_postal, tamaño_fuente)
    insertar_texto(pagina, 405, 204, empresa.domicilio.localidad, tamaño_fuente)
    insertar_texto(pagina, 505, 204, empresa.domicilio.provincia, tamaño_fuente)

    # Fecha
    insertar_texto(pagina, 150, 335,
                   f"{empleado.dia_ingreso()}/{empleado.mes_ingreso()}/{empleado.año_ingreso()}", tamaño_fuente)

    return pdf


def llenar_formulario_seguro_vida(empleado: Empleado, empresa: Empresa, opcion):
    if opcion == "mapfre":
        pdf = formulario_mapfre(empleado, empresa)
    elif opcion == "galeno":
        pdf = formulario_galeno(empleado, empresa)
    elif opcion == "andina":
        pdf = formulario_andina(empleado, empresa)
    else:
        return

    directorio_out = obtener_direccion_carpeta("out")
    destino_archivo = os.path.join(directorio_out,
                                   f"seguro_vida_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf")
    pdf.save(destino_archivo)
    

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
    # llenar_formulario_seguro_vida(empleado, empresa, "andina")
    # llenar_formulario_seguro_vida(empleado, empresa, "mapfre")
    # llenar_formulario_seguro_vida(empleado, empresa, "galeno")
