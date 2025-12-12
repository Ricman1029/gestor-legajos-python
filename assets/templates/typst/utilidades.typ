#let tick_box = box(width: 10pt, height: 10pt, stroke: 0.5pt + luma(150), radius: 2pt)

#let info_item(label, valor) = {
  stack(
    dir: ttb,      
    spacing: 7pt, 

    text(size: 0.7em, fill: luma(110), weight: "bold", tracking: 0.5pt, upper(label)),
    text(size: 1.1em, fill: luma(50), weight: "regular", valor)
  )
}

#let etiqueta_borde(contenido) = {
  box(
    fill: luma(245),
    inset: (x: 12pt, y: 8pt),
    radius: 4pt,
    stroke: luma(220),
    text(weight: "bold", fill: luma(50), size: 1.1em, contenido)
  )
}

#let etiqueta_solida(contenido) = {
  box(
    fill: luma(240),
    inset: 10pt,
    radius: 4pt,
    text(weight: "bold", fill: luma(50), size: 1em, contenido)
  )
}

#let input_field(label) = {
  stack(
    dir: ttb,
    spacing: 4pt,
    
    text(size: 0.7em, fill: luma(110), weight: "bold", tracking: 0.5pt, upper(label)),
    box(
      width: 100%,
      height: 1.8em,
      fill: luma(250),
      stroke: (bottom: (thickness: 0.5pt, paint: luma(150), dash: "dotted")),
      radius: 2pt,
      align(horizon + left, text(fill: luma(180), size: 0.8em, style: "italic")[ Completar... ])
    )
  )
}

#let checkbox(label, opciones) = {
  stack(
    dir: ttb,
    spacing: 6pt,
    text(size: 0.7em, fill: luma(110), weight: "bold", tracking: 0.5pt, upper(label)),

    grid(
      columns: opciones.len(),
      gutter: 1.5em, 
      ..opciones.map(opcion => {
        box(height: 1em, baseline: 0.2em)[
          #tick_box
          #h(5pt)
          #text(size: 0.9em, fill: luma(50), opcion)
        ]
      })
    )
  )
}

#let bloque_legal(contenido) = {
  block(
    width: 100%,
    fill: luma(240),
    inset: 15pt,
    radius: 4pt,
    stroke: (left: 4pt + luma(80)),
    contenido
  )
}

#let lista_dinamica(opciones) = {
  grid(
    columns: (auto, auto),
    column-gutter: 15pt,
    row-gutter: 20pt,
    ..opciones.enumerate(start: 1).map(((indice, opcion)) => (
      box(
        width: 24pt,
        height: 24pt,
        radius: 12pt,
        fill: luma(50),
        align(center+horizon, text(fill: white, weight: "bold", [#indice]))
      ),
      align(horizon)[ #opcion ]
    )).flatten()
  )
}

#let bloque_de_advertencia(contenido) = {
  align(center)[
    #block(
      width: 90%,
      fill: luma(250),
      stroke: (paint: luma(150), dash: "dashed"),
      radius: 8pt,
      inset: 20pt,
      [
        #contenido
      ]
    )
  ]
}

#let lista_checkbox(opciones) = {
  grid(
    columns: (auto, 1fr),
    column-gutter: 12pt,
    row-gutter: 10pt,
    ..opciones.map( opcion => (
      box(
        width: 12pt,
        height: 12pt,
        radius: 2pt,
        stroke: 0.5pt + luma(150),
      ),
      align(horizon)[ #opcion ]
    )).flatten()
  )
}

#let encabezado_de_seccion(contenido) = {
  block(width: 100%, below: 1.2em, above: 2em)[
    #text(
      size: 0.85em,
      weight: "bold",
      fill: luma(100),
      tracking: 0.5pt,
      upper(contenido)
    )
    #v(-0.7em)
    #line(length: 100%, stroke: 0.5pt + luma(200))
  ]
}

#let encabezado_de_pagina(titulo, subtitulo: none, localidad: none, fecha: none) = grid(
  columns: (1fr, auto),
  align: (horizon, horizon),
  [
    #text(size: 16pt, weight: "black", fill: luma(50), titulo) \
    #text(size: 10pt, fill: luma(100), subtitulo)
  ],
  [
    #text(size: 10pt, weight: "bold", fill: luma(80))[
      #localidad \
      #fecha
    ]
  ]
)
