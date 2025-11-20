import os
import pymupdf
from src.utils.persistencia import obtener_direccion_carpeta
from src.entidades.empresa import Domicilio, Empleado
from src.entidades.persona import Persona


def pagina_general(pagina, empleado):
    cuadro = pymupdf.Rect(50, 20, 550, 800)
    texto = f"""
<p style='text-align: center;'>
    {empleado.persona.apellido.upper()} {empleado.persona.nombre.upper()} {empleado.fecha_ingreso}
</p>

<h1 style='text-align: center;'>REQUISITOS PARA OBRA SOCIAL</h1>

<p>El <b>trámite</b> se realiza en forma personal e individual por el titular afiliado en la Obra Social elegida.</p>
 
<p>Documentación a presentar:</p>

<ul style='font-size: 10px;'>
    <li>FOTOCOPIA DNI TITULAR</li> 
    <li>FOTOCOPIA ULTIMO RECIBO SUELDO</li> 
    <li>FOTOCOPIA CERTIFICADO DE MATRIMONIO/UNION DE HECHO</li> 
    <li>FOTOCOPIA DNI CONYUGE</li> 
    <li>FOTOCOPIA CERTIFICADO NACIMIENTO C/U DE LOS  HIJOS / DNI</li> 
</ul>

<p>El <b>beneficiario</b> puede ejercer el derecho a la opción de cambio desde el momento mismo del inicio de la 
relación laboral (Decreto 1400/01) eligiendo una obra social del Listado de Obras Sociales Sindicales.</p>

<p>El <b>trámite</b> se realiza en forma personal e individual por el titular afiliado.</p>

<p>El único lugar autorizado para realizar la opción de cambio es la sede o delegación de la Obra Social elegida. 
No debe ejercerse en oficinas de medicina privadas ni en el lugar de trabajo.</p>

<p>La opción de cambio puede realizarse una vez al año.</p>

<p>La misma, se efectiviza el primer día del tercer mes desde la presentación de la solicitud. Durante dicho período 
la Obra Social de origen debe otorgar al afiliado la prestación médica correspondiente.</p>
El trámite es totalmente gratuito.

<p><b>El beneficiario debe completar el formulario de opción sin tachaduras ni enmiendas y presentar la siguiente 
documentación:</b></p>

<ul>
    <li>Último recibo de sueldos o en su defecto certificación laboral.</li>
    <li>Documento Nacional de Identidad (D.N.I.)</li>
    <li>
        El formulario de opción deberá contar con su firma debidamente certificada por autoridad competente: escribano, 
        autoridad policial, bancaria o judicial (Resolución 950/2009).
    </li>
</ul>

<p><b>Al momento de efectuar la opción, la Obra Social debe entregar al beneficiario:</b></p>

<ul>
    <li>La copia amarilla del formulario de opción de cambio.</li>
    <li>La cartilla médica con la nómina completa de sus prestadores.</li>
    <li>Credencial con el nombre de la Obra Social.</li>
</ul>

<p>La opción de cambio es irretractable, excepto las expresas excepciones que establece la reglamentación vigente.</p>



<p><b>UNA VEZ FINALIZADO EL TRÁMITE DE OPCIÓN DE OBRA SOCIAL, EL TRABAJADOR DEBE INFORMAR/ENTREGAR AL EMPLEADOR 
COPIA DEL FORMULARIO DE OPCIÓN REALIZADO.</b></p> 

<p><b>Queda Usted debidamente notificado.              ……………………..</b></p>

"""
    pagina.insert_htmlbox(cuadro, texto, css="* {font-family: calibri;}")


def crear_notificacion_obra_social(empleado: Empleado, opcion):
    pdf = pymupdf.open()
    pagina = pdf.new_page()

    if opcion == "general":
        pagina_general(pagina, empleado)
    else:
        return

    pdf.copy_page(0)
    directorio_out = obtener_direccion_carpeta("out")
    destino_archivo = os.path.join(directorio_out,
                                   f"obra_social_{empleado.persona.apellido}_{empleado.persona.nombre}.pdf")
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

    crear_notificacion_obra_social(empleado, "general")
