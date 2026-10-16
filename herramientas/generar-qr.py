"""
Genera el QR de una tarjeta a partir de su direccion.

  1. qr/qr-imprimir.svg   -> para imprenta: vectorial, se amplia sin perder nada
  2. qr/qr-imprimir.png   -> 2000 px, para quien no pueda usar el SVG
  3. index.html           -> el QR que se ve en ordenador, escrito entre las
                             marcas <!-- QR:INICIO --> y <!-- QR:FIN -->

Los dos de imprimir y el de la pagina salen de la misma direccion, en la misma
llamada: asi nunca puede haber un QR impreso distinto del de la web.

Uso:   py herramientas/generar-qr.py https://qrafta.github.io/qrafta/

Necesita segno (py -m pip install segno). Solo en este equipo: la web no
depende de nada, el QR queda escrito dentro del HTML.

OJO: la direccion de un QR impreso no se puede cambiar. Antes de imprimir,
escanear el PNG con un movil y comprobar que abre la pagina buena.
"""

from pathlib import Path
import io
import re
import sys

import segno

# --- Ajustes ---------------------------------------------------------------
BASE        = Path(__file__).resolve().parent.parent
CARPETA_QR  = BASE / "qr"            # no se publica (esta en .gitignore)
PAGINA      = BASE / "index.html"
TINTA       = "#1F1B2E"              # color de los modulos al imprimir
FONDO       = "#FFFFFF"              # blanco: el contraste maximo para leerlo
CORRECCION  = "m"                    # m = aguanta ~15 % de dano (manchas, dobleces)
MARGEN      = 4                      # modulos en blanco alrededor: lo pide el estandar

MARCAS = re.compile(r"(<!-- QR:INICIO[^>]*-->)(.*?)(<!-- QR:FIN -->)", re.S)


def svg_para_pagina(qr):
    """SVG de una sola linea, sin cabecera XML, que toma el color del CSS."""
    buf = io.BytesIO()
    qr.save(buf, kind="svg", border=MARGEN, scale=1, dark="#000",
            light=None, xmldecl=False, svgns=True, omitsize=True,
            svgclass="qr", lineclass=None, nl=False)
    svg = buf.getvalue().decode("utf-8")
    # el color de los modulos lo decide la variable --color-qr-modulos
    svg = svg.replace('stroke="#000"', 'stroke="currentColor"')
    return svg.replace("<svg ", '<svg role="img" aria-label="Código QR de esta página" ', 1)


def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith("https://"):
        sys.exit("Uso: py herramientas/generar-qr.py https://direccion-completa/")
    url = sys.argv[1]

    qr = segno.make(url, error=CORRECCION, micro=False, boost_error=False)
    CARPETA_QR.mkdir(exist_ok=True)

    qr.save(CARPETA_QR / "qr-imprimir.svg", scale=10, border=MARGEN,
            dark=TINTA, light=FONDO, title=f"QR: {url}")
    lado = qr.symbol_size(border=MARGEN)[0]
    qr.save(CARPETA_QR / "qr-imprimir.png", scale=max(1, 2000 // lado),
            border=MARGEN, dark=TINTA, light=FONDO)

    html = PAGINA.read_text(encoding="utf-8")
    if not MARCAS.search(html):
        sys.exit("No encuentro <!-- QR:INICIO --> ... <!-- QR:FIN --> en index.html")
    html = MARCAS.sub(lambda m: f"{m.group(1)}\n        {svg_para_pagina(qr)}\n        {m.group(3)}",
                      html, count=1)
    PAGINA.write_text(html, encoding="utf-8", newline="")

    print(f"Direccion:  {url}")
    print(f"QR:         version {qr.version}, correccion {qr.error}, {lado}x{lado} modulos con margen")
    print(f"Imprimir:   {(CARPETA_QR / 'qr-imprimir.svg').relative_to(BASE)}  y  "
          f"{(CARPETA_QR / 'qr-imprimir.png').relative_to(BASE)}")
    print("Pagina:     QR escrito en index.html")
    print("Antes de imprimir: escanear el PNG con el movil y comprobar la direccion.")


if __name__ == "__main__":
    main()
