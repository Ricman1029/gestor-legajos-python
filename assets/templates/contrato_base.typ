#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2cm),
)
#set text(font: "Libertinus Serif", size: 11pt, lang: "es")

// --- CARGA DE DATOS ---
// Aquí Python inyectará el nombre del archivo JSON temporal
#let data = json("DATA_JSON_PATH")

// --- TÍTULO ---
#align(center)[
  #text(size: 14pt, weight: "bold")[CONTRATO DE TRABAJO]

]


#v(1cm)


// --- CUERPO ---
En la ciudad de #data.empresa_domicilio, a los #data.fecha_actual.

Entre la empresa *#data.empresa_razon*, CUIT *#data.empresa_cuit*, en adelante el "EMPLEADOR", y el Sr./Sra. *#data.empleado_apellido, #data.empleado_nombre*, DNI *#data.empleado_dni*, en adelante el "TRABAJADOR".

SE ACUERDA:

1. El TRABAJADOR prestará servicios como *#data.empleado_categoria* desde el *#data.empleado_ingreso*.

2. Sueldo inicial: *\$ #data.empleado_sueldo*.

#v(2cm)

// --- FIRMAS ---
#grid(
  columns: (1fr, 1fr),
  gutter: 20pt,
  align(center)[
    #box(width: 5cm, stroke: (bottom: 1pt + black))\
    #data.empresa_razon\
    EMPLEADOR

  ],

  align(center)[
    #box(width: 5cm, stroke: (bottom: 1pt + black))\
    #data.empleado_apellido, #data.empleado_nombre\
    TRABAJADOR
  ]

)
