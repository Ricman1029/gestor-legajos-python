import os
import pymupdf
from gestor_legajos.entidades.empresa import Domicilio, Empleado
from gestor_legajos.entidades.persona import Persona
from gestor_legajos.utils.persistencia import obtener_directorio_out


def pagina_galeno(pagina, empleado):
    cuadro = pymupdf.Rect(50, 50, 550, 800)
    texto = f"""
    <body>
        <h1>GALENO ART</h1>

        <br>

        <p>Señor/a trabajador/a:&emsp;{empleado.persona.apellido} {empleado.persona.nombre} {empleado.fecha_ingreso}</p>

        <br>

        <p>En cumplimiento de lo dispuesto por las resoluciones de la Superintendencia de Riesgos de Trabajo Nº
        310/2002 y su complementaria Nº 502/2002, GALENO ART se dirige a usted con la finalidad de asesorarlo
        sobre el contenido de dicha normativa:</p>

        <br>

        <ol>
            <li>
                <b>Usted deberá llevar consigo en todo momento la "Credencial de Identificación"</b> que su empleador
                le ha entregado, en la cual consta la Aseguradora de Riesgos de Trabajo que cubre los
                accidentes y enfermedades profesionales que pueda sufrir.
            </li>
            <li>
                <b>Deberá obligatoriamente denunciar ante su empleador</b> los accidentes del trabajo o las
                enfermedades profesionales que sufra.
            </li>
            <li>
                En caso de sufrir accidentes de trabajo y no poder notificarlo a su empleado, <b>en forma inmediata
                deberá comunicarse con GALENO ART llamando al teléfono 0800-333-1400</b> de acceso 
                gratuito que figura en la credencial, <b>ó bien dirigirse a un Centro Médico habilitado en la 
                cartilla.</b>
            </li>
        </ol>

        <br>

        <p>GALENO ART resalta e insiste sobre la importancia de llevar consigo en todo momento la "Credencial de
        identificación", a fin de que usted o quien eventualmente lo asista ante un accidente de trabajo (en especial
        el que eventualmente pudiera ocurrir en el trayecto entre domicilio y su lugar de trabajo, y viceversa),
        conozca que se encuentra cubierto por nuestra Aseguradora de Riesgos del Trabajo.</p>

        <br>

        <p>Ante una situación de este tipo, le recordamos que <b>llamando al teléfono 0800-333-1400 las 24 horas del 
        día los 365 días del año en forma inmediata será derivado a un centro asistencial que le dará cobertura en la 
        urgencia</b>, según el tipo de lesiones sufridas y la complejidad del cuadro que presente, reduciendo el 
        mínimo de esta manera, los inconvenientes porpios que produce una contingencia inesperada y las posibles 
        secuelas de la misma.</p>

        <p>Muchas gracias por su atención.</p>

        <br>

        <p>Queda Ud. debidamente notificado.
    </body>"""
    pagina.insert_htmlbox(cuadro, texto, css="* {font-family: calibri;font-size:11;}")


def pagina_andina(pagina, empleado):
    cuadro = pymupdf.Rect(50, 50, 550, 800)
    texto = f"""
<h1>ANDINA ART</h1>

<br>

<p>Señor/a trabajador/a:&emsp;{empleado.persona.apellido} {empleado.persona.nombre} {empleado.fecha_ingreso}</p>

<br>

<p>En cumplimiento de lo dispuesto por las resoluciones de la Superintendencia de Riesgos de Trabajo Nº
310/2002 y su complementaria Nº 502/2002, ANDINA ART se dirige a usted con la finalidad de asesorarlo
sobre el contenido de dicha normativa:</p>

<br>

<ol>
    <li>
        <b>Usted deberá llevar consigo en todo momento la "Credencial de Identificación"</b> que su empleador
        le ha entregado, en la cual consta la Aseguradora de Riesgos de Trabajo que cubre los
        accidentes y enfermedades profesionales que pueda sufrir.
    </li>
    <li>
        <b>Deberá obligatoriamente denunciar ante su empleador</b> los accidentes del trabajo o las
        enfermedades profesionales que sufra.
    </li>
    <li>
        En caso de sufrir accidentes de trabajo y no poder notificarlo a su empleado, <b>en forma inmediata
        deberá comunicarse con ANDINA ART llamando al teléfono 0800-222-0202 o al 0800-555-2552</b> de acceso 
        gratuito que figura en la credencial, <b>ó bien dirigirse a un Centro Médico habilitado en la 
        cartilla.</b>
    </li>
</ol>

<br>

<p>ANDINA ART resalta e insiste sobre la importancia de llevar consigo en todo momento la "Credencial de
identificación", a fin de que usted o quien eventualmente lo asista ante un accidente de trabajo (en especial
el que eventualmente pudiera ocurrir en el trayecto entre domicilio y su lugar de trabajo, y viceversa),
conozca que se encuentra cubierto por nuestra Aseguradora de Riesgos del Trabajo.</p>

<br>

<p>Ante una situación de este tipo, le recordamos que <b>llamando al teléfono 0800-222-0202 o al 0800-555-2552
las 24 horas del día los 365 días del año en forma inmediata será derivado a un centro asistencial que le
dará cobertura en la urgencia</b>, según el tipo de lesiones sufridas y la complejidad del cuadro que presente,
reduciendo el mínimo de esta manera, los inconvenientes porpios que produce una contingencia inesperada
y las posibles secuelas de la misma.</p>

<p>Muchas gracias por su atención.</p>

<br>

<p>Queda Ud. debidamente notificado.
"""
    pagina.insert_htmlbox(cuadro, texto, css="* {font-family: calibri;}")


def crear_notificacion_art(empleado: Empleado, opcion):
    pdf = pymupdf.open()
    pagina = pdf.new_page()

    if opcion == "galeno":
        pagina_galeno(pagina, empleado)
    elif opcion == "andina":
        pagina_andina(pagina, empleado)

    pdf.copy_page(0)
    directorio_out = obtener_directorio_out()
    destino_archivo = os.path.join(directorio_out, f"art_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf")
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

    crear_notificacion_art(empleado, "galeno")
    # crear_notificacion_art(empleado, "andina")
