import pymupdf
from fpdf import FPDF
from pypdf.annotations import FreeText


def linea_en_blanco(pdf: FPDF, alto, cantidad=1):
    for i in range(cantidad):
        pdf.ln(h=alto)

def texto_fpdf(pdf: FPDF, alto, texto, tamaño, tamaño_alternativo):
    if len(texto) >= 35:
        pdf.set_font_size(tamaño_alternativo)
    pdf.multi_cell(w=pdf.epw, h=alto, txt=texto)
    pdf.set_font_size(tamaño)


def negrita(pdf: FPDF, fuente, tamaño, alto, alineacion, texto):
    pdf.set_font(fuente, "B", tamaño)
    pdf.multi_cell(w=pdf.epw, h=alto, txt=texto, align=alineacion)
    pdf.set_font(fuente, "", tamaño)


def cuadro_texto(texto, x_left, x_right, y_bottom):
    return FreeText(
        text=texto,
        rect=(x_left, y_bottom + 15, x_right, y_bottom),
        font="Arial",
        bold=True,
        italic=True,
        font_size="20pt",
        font_color="00ff00",
        border_color=None,
        background_color=None,
    )


def insertar_texto(pagina, x, y, texto, tamaño=11):
    pagina.insert_text(
        pymupdf.Point(x=x, y=y),
        texto,
        fontsize=tamaño
    )


def buscar_indice_insercion(lista, elemento, atributo):
    inicio = 0
    fin = len(lista) - 1
    medio = (inicio + fin) // 2
    while inicio <= fin and (atributo(medio) if atributo else lista[medio]) != elemento:
        if (atributo(medio) if atributo else lista[medio]) < elemento:
            inicio = medio + 1
        else:
            fin = medio - 1
        medio = (inicio + fin) // 2
    return medio + 1


def agregar_en_orden(lista, valor, objeto=None, ordenar_por=None):
    posicion = buscar_indice_insercion(lista, valor, ordenar_por)
    lista.insert(posicion, objeto if objeto else valor)


def devolver_coincidencia(lista, valor, por_atributo, devolver_indice=False):
    for indice, elemento in enumerate(lista):
        if (por_atributo(elemento) if por_atributo else elemento) == valor:
            return indice if devolver_indice else elemento
