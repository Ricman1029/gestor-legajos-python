#import "lib.typ": *

#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2cm),
)
#set text(
  font: "Roboto",
  size: 10pt,
  fill: luma(30),
)

#let datos = json("/temp/temp_datos_typst.json")

#pagina_ficha_legajo(datos)

#pagebreak()

#pagina_alta_temprana(datos)

#pagebreak()

#pagina_recibo_ropa(datos)

#pagebreak()

#pagina_prestacion_por_desempleo(datos)

#pagebreak()

#pagina_art(datos)

#pagebreak()

#pagina_art(datos)

#pagebreak()

#pagina_obra_social(datos)

#pagebreak()

#pagina_obra_social(datos)
