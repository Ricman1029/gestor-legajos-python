import os 
from fpdf import FPDF
from src.entidades.empleado import Empleado
from src.entidades.empresa import Empresa
from src.entidades.persona import Persona
from src.entidades.domicilio import Domicilio
from src.utils.helpers import linea_en_blanco, negrita, texto_fpdf
from src.utils.persistencia import obtener_direccion_carpeta

ancho_col1 = 70
ancho_col2 = 20

def escribir_fecha(pdf: FPDF, empleado: Empleado):
    pdf.cell(w=0, h=8, txt=f"San Carlos de Bariloche, {empleado.escribir_fecha_ingreso()}", align="C")
    linea_en_blanco(pdf, 5, 2)


def pagina_1(pdf: FPDF, empleado: Empleado, empresa: Empresa):
    ancho_valor = pdf.epw - (ancho_col1 + ancho_col2)
    pdf.set_font("Arial", "", 12)
    pdf.rect(x=8, y=8, w=195, h=250)
    # Página 1
    # Sección 1
    pdf.cell(w=ancho_col1, h=7, txt="Legajo")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.numero_legajo)
    
    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Apellido y nombre")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=f"{empleado.persona.apellido} {empleado.persona.nombre}")
    
    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="C.U.I.L.")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.persona.cuil)
    
    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Documento de identidad")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.persona.dni())
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Dirección")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.persona.domicilio.direccion())
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Localidad")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=f"{empleado.persona.domicilio.codigo_postal} {empleado.persona.domicilio.localidad}")
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Teléfono")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt="."*40)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Provincia")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.persona.domicilio.provincia)
    

    # Sección 2
    linea_en_blanco(pdf, 5)
    pdf.cell(w=ancho_col1, h=7, txt="Fecha de nacimiento")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.persona.fecha_nacimiento)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Fecha de ingreso")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.fecha_ingreso)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Fecha de egreso")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt="."*40)
    

    # Sección 3
    linea_en_blanco(pdf, 5)
    pdf.cell(w=ancho_col1, h=7, txt="Sexo")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.persona.sexo)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Nivel de estudio")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt="."*40)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Cantidad de hijos")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt="."*40)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Estado civil")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt="."*40)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Convenio")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empresa.convenio)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Sueldo o jornal")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.sueldo)
    

    # Sección 4
    linea_en_blanco(pdf, 5)
    pdf.cell(w=ancho_col1, h=7, txt="Categoría")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    texto_fpdf(pdf=pdf, alto=7, texto=empleado.categoria, tamaño=12, tamaño_alternativo=10)
    

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Sindicato")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.cell(w=40, h=7, txt=empresa.sindicato)
    pdf.multi_cell(w=ancho_valor - 40, h=7, txt=f"AFILIADO:{" "*8}SI{" "*12}NO")
    
    pdf.rect(x=166, y=151, w=15, h=7)
    pdf.rect(x=185, y=151, w=15, h=7)

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Obra social")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt=empleado.persona.obra_social)
    

    # Sección 5
    pdf.set_x(pdf.l_margin)
    pdf.rect(x=10, y=165, w=191, h=30)
    pdf.multi_cell(w=pdf.epw, h=7, txt="Beneficiario Seguro de Vida", align="C")

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Apellido y nombre")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt="."*70)

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="D.N.I.")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt="." * 70)

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=7, txt="Parentesco")
    pdf.cell(w=ancho_col2, h=7, txt=":")
    pdf.multi_cell(w=ancho_valor, h=7, txt="." * 70)

    # Sección 6
    linea_en_blanco(pdf, 8, 1)
    if "CONSTRUCCIÓN" in empresa.convenio:
        pdf.rect(x=10, y=201, w=191, h=30)
        pdf.multi_cell(w=pdf.epw, h=7, txt="Beneficiario Fondo de Desempleo", align="C")

        pdf.set_x(pdf.l_margin)
        pdf.cell(w=ancho_col1, h=7, txt="Apellido y nombre")
        pdf.cell(w=ancho_col2, h=7, txt=":")
        pdf.multi_cell(w=ancho_valor, h=7, txt="." * 70)

        pdf.set_x(pdf.l_margin)
        pdf.cell(w=ancho_col1, h=7, txt="D.N.I.")
        pdf.cell(w=ancho_col2, h=7, txt=":")
        pdf.multi_cell(w=ancho_valor, h=7, txt="." * 70)

        pdf.set_x(pdf.l_margin)
        pdf.cell(w=ancho_col1, h=7, txt="Parentesco")
        pdf.cell(w=ancho_col2, h=7, txt=":")
        pdf.multi_cell(w=ancho_valor, h=7, txt="." * 70)

    # Sección 7
    linea_en_blanco(pdf, 7, 2)
    pdf.multi_cell(w=pdf.epw, h=8, align="R",
                   txt=f"{"."*40}\n"
                       "FIRMA DEL EMPLEADO"
                   )


def pagina_2(pdf: FPDF, empleado: Empleado, empresa: Empresa):
    # Página 2
    pdf.set_font("Arial", "", 10)
    escribir_fecha(pdf, empleado)
    linea_en_blanco(pdf, 5, 3)

    pdf.cell(w=ancho_col1, h=5, txt="SR.")
    pdf.multi_cell(w=50, h=8, txt=f"{empleado.persona.apellido} {empleado.persona.nombre}")

    pdf.set_x(pdf.l_margin)
    pdf.cell(w=ancho_col1, h=5, txt="D.N.I.")
    pdf.multi_cell(w=50, h=5, txt=f"{empleado.persona.dni()}")

    linea_en_blanco(pdf, 5, 3)

    negrita(pdf=pdf, fuente="Arial", tamaño=10, alto=5, alineacion="C",
            texto="CONSTANCIA DE ENTREGA DE CLAVE DE ALTA TEMPRANA - REGISTRO DE TRABAJADORES")

    linea_en_blanco(pdf, 5, 2)

    pdf.multi_cell(w=pdf.epw, h=5, txt="En cumplimiento del Art. 18-3º párrafo - "
                                 "Resolución General AFIP Nº 1891, dejo constancia de haber entregado al \n"
                                 "trabajador la constancia de inscripción en el Registro de trabajadores - "
                                 "Clave de Alta Temprana, \n\n Cordialmente, ")

    linea_en_blanco(pdf, 5, 3)

    pdf.multi_cell(w=pdf.epw, h=5, align="C",
                   txt=f"{empresa.nombre_empresa.upper()}\n"
                       f"C.U.I.T.: {empresa.cuit_empresa}\n"
                       f"I.E.R.I.C. Nº: {empresa.numero_ieric}")

    linea_en_blanco(pdf, 5, 3)

    pdf.multi_cell(w=pdf.epw, h=5, txt=f"{str("-*") * 73}", align="C")

    linea_en_blanco(pdf, 5)

    escribir_fecha(pdf, empleado)

    linea_en_blanco(pdf, 5, 2)

    pdf.multi_cell(w=pdf.epw, h=5, txt=f"{empresa.nombre_empresa.upper()}\n"
                                 "S          /          D", align="L")

    linea_en_blanco(pdf, 5)

    negrita(pdf=pdf, fuente="Arial", tamaño=10, alto=5, alineacion="C", texto="RECIBO")

    linea_en_blanco(pdf, 5, 2)

    pdf.multi_cell(w=pdf.epw, h=5, txt="Dejo constancia de haber recibido, en el día de la fecha, la "
                                 "constancia de inscripción en el Registro de Trabajadores\nClave de Alta Temprana"
                                 "\n\nCordialmente,")

    linea_en_blanco(pdf, 5, 2)

    pdf.multi_cell(w=pdf.epw, h=5, txt="Firma:.................................................\n"
                                 f"Nombre y apellido: {empleado.persona.apellido} {empleado.persona.nombre}\n"
                                 f"D.N.I. Nº: {empleado.persona.dni()}", align="C")


def pagina_3(pdf: FPDF, empleado: Empleado, empresa: Empresa):
    # Página 3
    escribir_fecha(pdf, empleado)

    pdf.multi_cell(w=pdf.epw, h=5, txt=f"{empresa.nombre_empresa.upper()}\n"
                                 "S          /          D", align="L")

    linea_en_blanco(pdf, 5)

    negrita(pdf, "Arial", tamaño=10, alto=5, alineacion="C",
            texto="RECIBO DE ROPA DE TRABAJO Y ELEMENTOS DE SEGURIDAD")

    linea_en_blanco(pdf, 5)

    pdf.multi_cell(w=pdf.epw, h=5, txt="Dejo constancia de haber recibido, en el día de la fecha, la "
                                 "siguiente ropa de trabajo y elementos de seguridad:\n\n"
                                 "......................... Ropa de trabajo (camisa, pantalón o mameluco)\n"
                                 "......................... Guantes\n"
                                 "......................... Casco de seguridad\n"
                                 "......................... Antiparras\n"
                                 "......................... Faja seguridad\n\n"
                                 "La provisión de los elementos de protección personal son de uso obligatorio "
                                 "en todas aquellas tareas en las cuales las condiciones de trabajo involucren "
                                 "un riesgo de accidentes. Comprometiéndome a solicitar su cambio cada vez que "
                                 "el elemento se deteriore como consecuencia del uso. La entrega de los elementos "
                                 "se efectúa conforme a la normativa en materia de seguridad e higiene en el "
                                 "trabajo art. 26 C.C.T..\n"
                                 "He sido capacitado en su uso correcto.")

    linea_en_blanco(pdf, 5)

    pdf.multi_cell(w=pdf.epw, h=5, txt="Firma:.................................................\n"
                                 f"Nombre y apellido: {empleado.persona.apellido} {empleado.persona.nombre}\n"
                                 f"D.N.I. Nº: {empleado.persona.dni()}", align="C")


def pagina_4(pdf: FPDF, empleado: Empleado, empresa: Empresa):
    def texto():
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=pdf.epw, h=5,
                       txt=f"Por la presente se pone en conocimiento del trabajador "
                           f"{empleado.persona.apellido} {empleado.persona.nombre} que "
                           f"ingresa como trabajador en relación de dependencia del empleador "
                           f"{empresa.nombre_empresa.upper()} con fecha {empleado.fecha_ingreso} "
                           f"por lo que se informa que en el caso de que se encuentre cobrando el "
                           f"FONDO DE DESEMPLEO gestionado a través de ANSES, tiene 5 días hábiles para "
                           f"dar la baja a este beneficio por estar nuevamente bajo relación laboral, "
                           f"QUEDA USTED DEBIDAMENTE NOTIFICADO.\n\n"
                       )

    # Página 4
    escribir_fecha(pdf, empleado)

    negrita(pdf, "Arial", 10, 5, "L", "PARA EMPLEADOR")

    texto()
    pdf.multi_cell(w=pdf.epw, h=8,
                   txt=f"Notificado:\n"
                       f"Aclaración:\n"
                       f"D.N.I.:"
                   )

    linea_en_blanco(pdf, 5, 10)

    escribir_fecha(pdf, empleado)

    negrita(pdf, "Arial", 10, 5, "L", "PARA EMPLEADO")

    texto()
    pdf.multi_cell(w=pdf.epw, h=8, txt=f"Notificado:\n")
    pdf.cell(w=35, h=8, txt=f"Aclaración:")
    pdf.multi_cell(w=pdf.epw, h=8, txt=f"{empresa.nombre_empresa}")
    pdf.cell(w=35, h=8, txt=f"D.N.I.:")


def constancia_entrega_general(empleado: Empleado, empresa: Empresa):
    pdf = FPDF(orientation="portrait", unit="mm", format="a4")
    pdf.set_font("Arial", "", 10)

    pdf.add_page()
    pagina_1(pdf, empleado, empresa)

    pdf.add_page()
    pagina_2(pdf, empleado, empresa)

    pdf.add_page()
    pagina_3(pdf, empleado, empresa)
    linea_en_blanco(pdf, 5, 5)
    pagina_3(pdf, empleado, empresa)

    pdf.add_page()
    pagina_4(pdf, empleado, empresa)

    directorio_out = obtener_direccion_carpeta("out")
    destino_archivo = os.path.join(directorio_out, f"legajo_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf")
    pdf.output(destino_archivo)


def crear_pdf_constancia_entrega(
        empleado: Empleado,
        empresa: Empresa,
        opcion: str = "general",
):
    if opcion == "general":
        constancia_entrega_general(empleado, empresa)
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

    crear_pdf_constancia_entrega(empleado, empresa)
