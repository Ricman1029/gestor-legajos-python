#import "utilidades.typ": *

#let linea_de_recorte = {
  v(1fr)
  align(center)[
    #stack(
      dir: ltr,
      spacing: 10pt,
      line(length: 40%, stroke: (dash: "dashed", paint: luma(150))),
      text(size: 10pt, fill: luma(150))[✂], 
      line(length: 40%, stroke: (dash: "dashed", paint: luma(150)))
    )
  ]
  v(1fr)
}

#let tabla_beneficiarios = {
  table(
    columns: (2fr, 1fr, 3fr, 1fr),
    stroke: (x, y) => (bottom: 0.5pt + luma(230)),
    inset: 2pt,

    table.header([*Nombre y Apellido*], [*Parentesco*], [*Domicilio*], [*%*]),

    input_field(""), input_field(""), input_field(""), input_field(""),
    input_field(""), input_field(""), input_field(""), input_field(""),
  )
  text(size: 0.8em, fill: luma(120))[En caso de falta de designación, se aplicará la Ley 24.241.]
}

#let recibo_de_conformidad = {
  align(center)[
    #line(length: 100%, stroke: (dash: "dotted", paint: luma(150)))
    #v(-0.8em) 
    #rect(fill: white, inset: 5pt)[#text(size: 8pt, fill: luma(150))[ RECIBO DE CONFORMIDAD ]]
  ]
}

#let recibo_epp(contenido) = {
  set text(size: 9pt)

  etiqueta_solida[#contenido]
  
  table(
    columns: (3fr, 0.8fr, 0.8fr),
    stroke: (x, y) => (bottom: 0.5pt + luma(230)),
    inset: (y: 5pt, x: 5pt),
    align: horizon,
    
    table.header(
      text(weight: "bold", "ELEMENTO"),
      align(center, text(weight: "bold", "CANT.")),
      align(center, text(weight: "bold", "RECIBÍ"))
    ),
    
    text[Ropa de Trabajo], align(center)[1], align(center, tick_box),
    text[Guantes de Seguridad], align(center)[1], align(center, tick_box),
    text[Casco de Seguridad], align(center)[1], align(center, tick_box),
    text[Antiparras / Gafas], align(center)[1], align(center, tick_box),
    text[Faja Lumbar], align(center)[1], align(center, tick_box),
  )

  v(0.5em)

  bloque_legal[
    #text(fill: luma(60))[
      *Declaración:* Recibí los elementos de protección personal en condiciones. 
      + *Uso Obligatorio:* Reconozco que son obligatorios para tareas de riesgo. 
      + *Mantenimiento:* Solicitaré cambio ante deterioro como consecuencia del uso.
      + *Normativa:* Art. 26 C.C.T. 
      + *Capacitación:* Fui capacitado en su uso.
    ]
  ] 

  v(1.2em)
}

#let firma_trabajador(empleado) = {
  stack(
    dir: ttb,
    spacing: 5pt,
    line(length: 6cm, stroke: 0.5pt),
    text(weight: "bold", empleado.display.nombre_completo),
    text(size: 8pt, fill: luma(100), "Firma del Empleado")
  )
}

#let pie_pagina_ficha_legajo(empleado) = {
  line(length: 100%, stroke: (dash: "dashed", thickness: 0.5pt, paint: luma(180)))
  v(2em)

  grid(
    columns: (1fr, auto),
    gutter: 2em,
    align: (top, center),
    [
      #text(size: 8pt, fill: luma(120))[
        *Declaración de conformidad:*\
        Los datos expresados en la presente ficha revisten carácter de declaración jurada y se corresponden con la documentación original presentada ante el departamento de RRHH.
      ]
    ],
    align(bottom, firma_trabajador(empleado))
  )
}

#let encabezado_art(empresa) = {
  grid(
    columns: (1fr, auto),
    align: (horizon, horizon),
    [
      #text(size: 16pt, weight: "black", fill: luma(50), "COBERTURA DE ART") \
      #text(size: 10pt, fill: luma(100), "Aseguradora de Riesgos del Trabajo")
    ],
    etiqueta_solida[#empresa.art.nombre]
  )
}

#let firma_empleador(empresa, alineacion: center) = {
  align(alineacion, block[
    #align(center, 
      stack(
        dir: ttb,
        spacing: 5pt,
        box(
          width: 6cm,
          height: 1.5cm,
          stroke: (dash: "dashed", paint: luma(180)), 
          radius: 4pt, 
          align(center+horizon)[#text(size:8pt, fill:luma(150))[Espacio Sello Empresa]]
        ),
        text(weight: "bold", size: 9pt, empresa.razon_social),
        text(size: 8pt, fill: luma(100), "C.U.I.T. " + empresa.display.cuit)
      )
    )]
  )
}

#let firma_y_aclaracion(empleado) = {
  grid(
    columns: (1fr, auto),
    gutter: 1em,
    align: (bottom, center),

    align(left)[
      #text(size: 9pt, fill: luma(100))[
        *Nombre:* #empleado.display.nombre_completo \
        *D.N.I.:* #empleado.display.dni \
        *Fecha:* #empleado.laborales.fecha_ingreso
      ]
    ],
    align(bottom, firma_trabajador(empleado))
  )
}

#let encabezado_legajo(empleado) = {
  grid(
    columns: (1fr, auto),
    align: (horizon, horizon),
    gutter: 1em,
    [
      #text(size: 26pt, weight: "black", fill: luma(20), empleado.display.nombre_completo) \
      #v(0.2em)
      #text(size: 11pt, fill: luma(100), weight: "medium")[
        CUIL: #empleado.display.cuil
      ]
    ],
    etiqueta_borde[LEGAJO #empleado.legajo]
  )
}

#let seccion_datos_personales(empleado) = {
  encabezado_de_seccion("Datos Personales y Contacto")
  grid(
    columns: (1fr, 1fr, 1fr),
    row-gutter: 2.5em, 
    column-gutter: 2em,

    info_item("Documento (D.N.I.)", empleado.display.dni),
    info_item("Fecha de Nacimiento", empleado.identificacion.fecha_nacimiento),
    info_item("Sexo", empleado.identificacion.sexo),

    grid.cell(colspan: 2, info_item("Domicilio Real", empleado.display.direccion_completa)),
    info_item("Localidad", empleado.direccion.localidad),

    if empleado.contacto.telefono != "" { info_item("Teléfono", empleado.contacto.telefono) } else { input_field("Teléfono") },
    if empleado.contacto.mail != "" { grid.cell(colspan: 2, info_item("Email", empleado.contacto.mail)) } else { input_field("Email") },
  )
}

#let seccion_detalle_contrato(empleado, convenio) = {
  encabezado_de_seccion("Detalle Contractual")

  grid(
    columns: (1fr, 2fr),
    row-gutter: 2.5em,
    column-gutter: 2em,

    info_item("Fecha de Ingreso", empleado.laborales.fecha_ingreso),
    info_item("Categoría Laboral", empleado.laborales.categoria),

    info_item("Sueldo / Jornal Básico", empleado.display.string_sueldo),
    info_item("Convenio Colectivo", convenio),
  )
}

#let seccion_seguridad_social(empleado) = {
  encabezado_de_seccion("Seguridad Social y Familia")

  grid(
    columns: (1fr, 1fr, 1fr),
    row-gutter: 2.5em,
    column-gutter: 2em,

    info_item("Obra Social", empleado.laborales.obra_social),
    info_item("Sindicato", empleado.laborales.sindicato),
    checkbox("Afiliado al Sindicato", ("SI", "NO")),

    input_field("Estado Civil"),
    input_field("Hijos"),
    info_item("Fecha de Egreso", "-")
  )
}


#let constancia_de_inscripcion(empresa, empleado) = {
  encabezado_de_seccion("Constancia del Empleador")

  bloque_legal[
      #text(size: 10pt, fill: luma(50))[
        *Señor/a:* #empleado.display.nombre_completo \
        *D.N.I.:* #empleado.display.dni

        #v(1em)

        En cumplimiento del *Art. 18, 3º párrafo de la Resolución General AFIP N° 1891*, la empresa deja constancia de haber entregado al trabajador la "Constancia de Inscripción
        en el Registro de Trabajadores" (Clave de Alta Temprana).
      ]

      #v(2.5em)

      #firma_empleador(empresa)
    ]
}

#let recibo_constancia_inscripcion(empleado) = {
  encabezado_de_seccion("Acuse de Recibo del Trabajador")

  text(size: 10pt, fill: luma(30))[
    Dejo constancia de haber recibido en el día de la fecha, la constancia de inscripción mencionada anteriormente y la Clave de Alta Temprana correspondiente.
  ]

  v(3cm)

  firma_y_aclaracion(empleado)
}


#let notificacion_desempleo_anses(empresa, empleado) = {
  bloque_legal[
    #text(size: 9.5pt, fill: luma(40))[
      Por la presente se pone en conocimiento del trabajador *#empleado.display.nombre_completo* (D.N.I. #empleado.display.dni), que ingresa bajo relación de dependencia de la
      empresa *#empresa.razon_social* con fecha *#empleado.laborales.fecha_ingreso*, que en caso de encontrarse cobrando actualmente el *FONDO DE DESEMPLEO* gestionado a través de
      ANSES, dispone de un plazo perentorio de:
    ]

    #v(0.5em)
    #align(center)[#etiqueta_borde[5 DÍAS HÁBILES]]
    #v(0.5em)

    #text(size: 9.5pt, fill: luma(40))[
      para tramitar la *BAJA* de dicho beneficio por encontrarse nuevamente bajo relación laboral activa.
    ]
  ]

  v(1em)

  align(center)[
    #text(size: 9pt, weight: "bold", fill: luma(50), "QUEDA USTED DEBIDAMENTE NOTIFICADO")
  ]

  v(2em)
} 

#let datos_destinatario_art(empleado) = {
  grid(
    columns: (1fr, auto),
    gutter: 1em,
    [
      #text(size: 10pt, fill: luma(100))[
        *Trabajador:* #empleado.display.nombre_completo \
        *Fecha:* #empleado.laborales.fecha_ingreso
      ]
    ],
    align(right)[
      #text(size: 9pt, fill: luma(100))[Ref: Res. SRT 310/02 y 502/02]
    ]
  )
}
