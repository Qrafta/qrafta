"""
Genera el QR de una tarjeta a partir de su direccion.

  1. qr/<nombre>.svg   -> para imprenta: vectorial, se amplia sin perder nada
  2. qr/<nombre>.png   -> 2000 px, para quien no pueda usar el SVG
  3. index.html        -> (opcional, con --pagina) el QR escrito dentro de la
                          pagina, entre <!-- QR:INICIO <marca> --> y <!-- QR:FIN -->

<nombre> sale del final de la direccion (.../cecilia-quignon/ -> cecilia-quignon).
El QR impreso y el de la pagina salen de la misma direccion en la misma llamada:
nunca puede haber uno impreso que lleve a un sitio distinto.

Uso:
  py herramientas/generar-qr.py https://qrafta.github.io/qrafta/
  py herramientas/generar-qr.py https://qrafta.github.io/cecilia-quignon/ --pagina cecilia-quignon

Necesita segno (py -m pip install segno). Solo en este equipo: la web no
depende de nada, el QR queda escrito dentro del HTML.

OJO: la direccion de un QR impreso no se puede cambiar. Antes de imprimir,
escanear el PNG con un movil y comprobar que abre la pagina buena.
"""

from pathlib import Path
import argparse
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


def nombre_de(url):
    """https://qrafta.github.io/cecilia-quignon/ -> 'cecilia-quignon'."""
    partes = [p for p in url.split("://", 1)[1].split("/") if p]
    nombre = partes[-1] if len(partes) > 1 else partes[0]
    return re.sub(r"[^a-z0-9]+", "-", nombre.lower()).strip("-") or "qr"


def svg_para_pagina(qr):
    """SVG de una sola linea, sin cabecera XML, que toma el color del CSS.
    Va marcado como decorativo: el enlace que lo rodea ya dice adonde lleva."""
    buf = io.BytesIO()
    qr.save(buf, kind="svg", border=MARGEN, scale=1, dark="#000",
            light=None, xmldecl=False, svgns=True, omitsize=True,
            svgclass="qr", lineclass=None, nl=False)
    svg = buf.getvalue().decode("utf-8")
    # el color de los modulos lo decide la variable --color-qr-modulos
    svg = svg.replace('stroke="#000"', 'stroke="currentColor"')
    return svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)


def main():
    ap = argparse.ArgumentParser(description="QR de una tarjeta Qrafta")
    ap.add_argument("url", help="direccion completa, con https://")
    ap.add_argument("--pagina", metavar="MARCA",
                    help="escribir tambien el QR en index.html, en <!-- QR:INICIO MARCA -->")
    args = ap.parse_args()

    url = args.url
    if not url.startswith("https://"):
        sys.exit("La direccion tiene que empezar por https://")

    qr = segno.make(url, error=CORRECCION, micro=False, boost_error=False)
    nombre = nombre_de(url)
    CARPETA_QR.mkdir(exist_ok=True)

    qr.save(CARPETA_QR / f"{nombre}.svg", scale=10, border=MARGEN,
            dark=TINTA, light=FONDO, title=f"QR: {url}")
    lado = qr.symbol_size(border=MARGEN)[0]
    qr.save(CARPETA_QR / f"{nombre}.png", scale=max(1, 2000 // lado),
            border=MARGEN, dark=TINTA, light=FONDO)

    print(f"Direccion:  {url}")
    print(f"QR:         version {qr.version}, correccion {qr.error}, {lado}x{lado} modulos con margen")
    print(f"Imprimir:   qr/{nombre}.svg  y  qr/{nombre}.png")

    if args.pagina:
        marcas = re.compile(r"(<!-- QR:INICIO " + re.escape(args.pagina) + r"(?: [^>]*)?-->)(.*?)"
                            r"(\n?[ ]*<!-- QR:FIN -->)", re.S)
        html = PAGINA.read_text(encoding="utf-8")
        m = marcas.search(html)
        if not m:
            sys.exit(f"No encuentro <!-- QR:INICIO {args.pagina} ... --> ... <!-- QR:FIN --> en index.html")
        sangria = re.search(r"([ ]*)<!-- QR:INICIO", html[:m.end(1)].rsplit("\n", 1)[-1]).group(1)
        nuevo = f"{m.group(1)}\n{sangria}{svg_para_pagina(qr)}\n{sangria}<!-- QR:FIN -->"
        html = html[:m.start()] + nuevo + html[m.end():]
        PAGINA.write_text(html, encoding="utf-8", newline="")
        print(f"Pagina:     QR escrito en index.html (marca '{args.pagina}')")

    print("Antes de imprimir: escanear el PNG con el movil y comprobar la direccion.")


if __name__ == "__main__":
    main()
