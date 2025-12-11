#import "componentes.typ": *

#let pagina_ficha_legajo(datos) = {
  encabezado_legajo(datos.empleado)

  v(1.2cm)

  seccion_datos_personales(datos.empleado)

  v(0.8cm)

  seccion_detalle_contrato(datos.empleado, datos.empresa.convenio)

  v(0.8cm)

  seccion_seguridad_social(datos.empleado)

  v(0.8cm)

  encabezado_de_seccion("Beneficiarios Seguro de Vida")
  tabla_beneficiarios

  v(1fr)

  pie_pagina_ficha_legajo(datos.empleado)
}

#let pagina_alta_temprana(datos) = {

  encabezado_de_pagina(
    "ALTA TEMPRANA ARCA",
    subtitulo: "Registro de Trabajadores - Resolución Gral. N° 1891", 
    localidad: datos.empresa.direccion.localidad,
    fecha: datos.empleado.laborales.fecha_ingreso
  )

  v(1.5cm)

  constancia_de_inscripcion(datos.empresa, datos.empleado)

  v(2cm)

  recibo_de_conformidad

  v(1cm)

  recibo_constancia_inscripcion(datos.empleado)
}

#let pagina_recibo_ropa(datos) = {

  encabezado_de_pagina(
    "ENTREGA DE ELEMENTOS DE PROTECCIÓN PERSEONAL",
    subtitulo: "Registro de Trabajadores - Resolución Gral. N° 1891",
    localidad: datos.empresa.direccion.localidad,
    fecha: datos.empleado.laborales.fecha_ingreso
  )
  recibo_epp[EJEMPLAR EMPLEADOR]
  firma_y_aclaracion(datos.empleado)

  linea_de_recorte

  encabezado_de_pagina(
    "ENTREGA DE ELEMENTOS DE PROTECCIÓN PERSEONAL",
    subtitulo: "Registro de Trabajadores - Resolución Gral. N° 1891",
    localidad: datos.empresa.direccion.localidad,
    fecha: datos.empleado.laborales.fecha_ingreso
  )
  recibo_epp[EJEMPLAR TRABAJADOR]
  firma_y_aclaracion(datos.empleado)
}

#let pagina_prestacion_por_desempleo(datos) = {

  encabezado_de_pagina(
    "NOTIFICACIÓN PRESTACIÓN POR DESEMPLEO (ANSES)",
    subtitulo: "PARA LEGAJO EMPLEADOR",
    localidad: datos.empresa.direccion.localidad,
    fecha: datos.empleado.laborales.fecha_ingreso
  )

  v(1em)

  notificacion_desempleo_anses(datos.empresa, datos.empleado)
  firma_y_aclaracion(datos.empleado)

  v(1fr)

  linea_de_recorte

  v(1fr)

  encabezado_de_pagina(
    "NOTIFICACIÓN PRESTACIÓN POR DESEMPLEO (ANSES)",
    subtitulo: "PARA EL TRABAJADOR",
    localidad: datos.empresa.direccion.localidad,
    fecha: datos.empleado.laborales.fecha_ingreso
  )

  v(1em)

  notificacion_desempleo_anses(datos.empresa, datos.empleado)
  firma_empleador(datos.empresa, alineacion: right)
}

#let pagina_art(datos) = {

  encabezado_art(datos.empresa)

  v(1cm)

  datos_destinatario_art(datos.empleado)

  v(1em)

  bloque_legal[
    #text(size: 10pt, fill: luma(50))[
      Por medio de la presente, se le notifica que se encuentra cubierto por *#datos.empresa.art.nombre ART* ante cualquier accidente de trabajo o enfermedad profesional. A continuación
      se detallan sus obligaciones y derechos bajo la normativa vigente:
    ]
  ]


  v(1.5cm)

  lista_dinamica((
    [
      *Credencial Obligatoria:* \
      Usted debe llevar consigo en todo momento la "Credencial de Identificación" provista por la empresa (tarjeta plástica o digital).
    ],
    [
      *Denuncia de Accidentes:* \
      Es su obligación comunicar inmediatamente a su empleador cualquier accidente ocurrido en el lugar de trabajo o en el trayecto (in itinere).
    ],
    [
      *Asistencia Directa:* \
      Si no pudiera comunicarse con su empleador ante una emergencia médica laboral, debe contactar directamente a la ART.
    ]
  ))

  v(1.5cm)

  bloque_de_advertencia[
    #text(size: 10pt, fill: luma(100), upper("Centro de Coordinación de Emergencias Médicas")) \
    #v(0.5em)
    #text(size: 24pt, weight: "black", fill: luma(30), datos.empresa.art.telefono_emergencias) \
    #v(0.5em)
    #text(size: 9pt, fill: luma(100), "Atención las 24 horas - Los 365 días del año")
  ]

  v(1em)
  align(center, text(size: 9pt, style: "italic", fill: luma(120))[
    Conserve este número en su teléfono celular bajo el nombre "ART EMERGENCIA".
  ])

  v(1fr)

  line(length: 100%, stroke: 0.5pt + luma(200))

  align(center)[
    #text(size: 9pt, fill: luma(50))[
      *Queda Ud. debidamente notificado.*\
      Se hace entrega de la credencial correspondiente.
    ]
  ]

  v(2em)

  firma_y_aclaracion(datos.empleado)
}

#let pagina_obra_social(datos) = {

  encabezado_de_pagina(
    "TRÁMITE DE OBRA SOCIAL",
    subtitulo: "Instructivo de Afiliación y Opción de Cambio",
    localidad: datos.empresa.direccion.localidad,
    fecha: datos.empleado.laborales.fecha_ingreso
  )

  v(1cm)

  encabezado_de_seccion("Documentación a Presentar")

  text(size: 10pt, fill: luma(50))[
    El trámite es *personal* y debe realizarse en la sede de la Obra Social elegida. Usted deberá presentar la siguiente documentación:
  ]

  v(1em)

  lista_checkbox((
    [Fotocopia D.N.I. del Titular],
    [Fotocopia Último Recibo de Sueldo],
    [Fotocopia Cert. de Matrimonio / Unión Convivencial],
    [Fotocopia D.N.I. de Cónyuge e Hijos],
    [Certificados de Nacimiento de los Hijos],
  ))

  v(1.5cm)

  encabezado_de_seccion("Derecho de Opción de Cambio")

  bloque_legal[
    De acuerdo al *Decreto 1400/01*, el trabajador puede ejercer el derecho de cambio desde el inicio de la relación laboral.

    *Condiciones Clave:*
    1. *Frecuencia:* Una vez al año.
    2. *Vigencia:* Efectiva el 1º día del tercer mes desde la solicitud. (La Obra Social de origen cubre hasta esa fecha).
    3. *Lugar:* Exclusivamente en la sede de la Obra Social elegida (nunca en la empresa ni en medicina prepaga).
    4. *Costo:* El trámite es totalmente *GRATUITO*.
  ]

  v(1.5cm)

  bloque_de_advertencia[
    #stack(
      dir: ttb,
      spacing: 8pt,
      text(size: 11pt, weight: "black", fill: luma(30), upper("¡Aviso Importante!")),
      text(size: 10pt, fill: luma(50))[
        Una vez finalizado el trámite en la Obra Social, es su obligación:
      ],
      text(size: 10pt, weight: "bold", fill: luma(0))[
        ENTREGAR AL EMPLEADOR COPIA DEL FORMULARIO DE OPCIÓN
      ],
      text(size: 9pt, style: "italic", fill: luma(100))[
        Sin este comprobante, la empresa no podrá derivar sus aportes correctamente.
      ]
    )
  ]

  v(1fr)

  line(length: 100%, stroke: 0.5pt + luma(200))
  v(1.5em)

  firma_y_aclaracion(datos.empleado)
}
