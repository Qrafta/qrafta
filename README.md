# Tarjeta de presentación · Qrafta

La tarjeta digital de Qrafta: una sola página, pensada para abrirse desde un código QR
impreso. Hace dos trabajos a la vez: presenta Qrafta y sirve de escaparate de lo que
puede llevar una tarjeta hecha por Qrafta.

🔗 **Ver la página:** https://qrafta.github.io/qrafta/

> **No renombrar el repositorio:** esa dirección es la que llevará el QR impreso.

> **Estado: maqueta en curso.** El diseño es provisional y falta fijar la dirección
> final (vista previa al compartir y QR). Los textos están terminados, y también el
> funcionamiento: guardar contacto, compartir, modo oscuro, maquetas
> ampliables y preguntas desplegables.

---

## El encargo

Qrafta hace tarjetas de presentación digitales a medida: un QR en papel que, al
escanearlo, abre en el móvil todo lo que hay que saber de un artista, un evento, un
restaurante o una tienda. Esta es la tarjeta de la propia Qrafta, la que se enseña a
los posibles clientes. Por eso tenía que ser a la vez tarjeta y demostración.

Mandan las mismas restricciones que en todas las tarjetas de Qrafta:

1. **Una sola página autocontenida.** Todo el HTML, CSS, JavaScript y los dibujos viven
   dentro de `index.html`. Sin frameworks, sin CDN, sin build, sin dependencias.
2. **Primero el móvil.** Se abre desde la cámara de un teléfono, muchas veces con datos y
   mala cobertura. El peso importa.
3. **Todo el estilo, cambiable desde un sitio.** Colores, tipografías y medidas clave en
   un único bloque `:root` comentado al principio.

## Lo que pesa

| Archivo | Sin comprimir | Lo que se descarga |
|---|---|---|
| `index.html` (página, estilos, código, logo e iconos) | 52 KB | **14 KB** |
| `imagenes/icono-180.png` (solo al añadirla a la pantalla de inicio del iPhone) | 9 KB | 9 KB |
| `imagenes/preview.jpg` (solo la piden WhatsApp y las redes al previsualizar) | 30 KB | 30 KB |

Quien escanea el QR descarga unos **14 KB**: menos que una sola foto de móvil. A
propósito, la página no presume de ello: es un dato para este README, no para el
visitante.

## Decisiones técnicas

### Sin una sola foto

El logo, los iconos y las cuatro maquetas de móvil están dibujados con SVG y CSS dentro
del HTML. No hay nada que cargar en diferido porque no hay nada pesado que cargar. Las
dos únicas imágenes aparte (el icono del iPhone y la vista previa al compartir) existen
porque iOS no acepta un icono SVG y las apps de mensajería no previsualizan SVG ni WebP.

### Sin fuentes descargadas

La marca usa Georgia y el texto la fuente del sistema: 0 KB y ninguna petición a
Google Fonts, que recibiría la IP de cada visitante. Si la tipografía definitiva no es
del sistema, se incrustará recortada al alfabeto latino, como en la tarjeta de Cecilia.

### Modo oscuro sin botón

Si el móvil está en modo oscuro, la página también. Es un segundo bloque `:root` que
solo cambia colores: enseña de paso que todo el aspecto sale de unas pocas variables. Se
descartó el botón manual porque todas las tarjetas de Qrafta comparten dominio, y la
preferencia guardada de una tarjeta podría colarse en las demás.

### Contraste

La terracota de la marca (#E2603C) no llega al contraste mínimo como texto pequeño
sobre crema. Para texto se usa una terracota más oscura (`--color-acento-texto`); la
original queda para botones y adornos. Los botones llevan el texto en tinta, no en
crema, por el mismo motivo.

### Correo a prueba de robots

La dirección nunca aparece escrita en el HTML. Se compone al cargar la página a partir
de dos variables (bloque 0 del JavaScript). El botón *Guardar contacto* usa las mismas
variables y fabrica la ficha (`.vcf`) en el momento: no hay ningún archivo en el
repositorio con el correo dentro. Por la misma razón la ficha para buscadores (JSON-LD)
no lleva el correo.

### Guardar contacto y compartir

- **Guardar contacto**: una vCard 3.0 marcada como empresa. En iPhone se abre la ficha
  de "Crear contacto"; en el resto se descarga `qrafta.vcf` y el móvil ofrece importarla.
- **Compartir**: el menú de compartir del propio móvil (Web Share API). Donde no existe
  (por ejemplo, Firefox de escritorio), copia el enlace y avisa con "Enlace copiado".
- **Copiar correo**: en un ordenador sin programa de correo configurado, un `mailto:`
  no hace nada; copiar la dirección siempre funciona.

### Maquetas en vez de casos reales

La sección de ejemplos muestra cuatro maquetas de móvil (artista, restaurante, evento,
tienda) dibujadas con CSS, cada una con su paleta, y rotuladas como maqueta de ejemplo.
La tarjeta de Qrafta es independiente y no enlaza a clientes. Cada maqueta se mide en
`em` a partir de un solo ancho (`--ancho-movil`), así que el lightbox la amplía cambiando
una variable, sin una segunda versión del dibujo.

### "Cómo funciona", en una frase

Nada de pasos numerados ni explicaciones técnicas: «Escaneas el QR con el móvil y ya
está». Es lo único que necesita saber quien la recibe.

### Detalles de uso

- **Barra fija** con resaltado de la sección visible mediante `IntersectionObserver`, no
  con un listener de `scroll`.
- **Ampliación** (*lightbox*) propia, sin librerías: se cierra con ✕, con `Esc` y tocando
  fuera, el foco no se escapa mientras está abierto y vuelve a la maqueta al cerrar.
- **Preguntas frecuentes** con `<details>`: se despliegan sin JavaScript y los lectores
  de pantalla las entienden de serie.
- **Accesibilidad**: navegación por teclado, enlace para saltar al contenido, zonas de
  toque de 44 px como mínimo (comprobadas una a una), decoración marcada como
  `aria-hidden`, avisos leídos por lectores de pantalla y respeto a
  `prefers-reduced-motion` (la Q no se anima).
- **El QR en pantalla** solo aparece en ordenador (pantalla ancha y ratón): desde el
  móvil ya se está dentro.

### Un solo origen para el QR

El QR impreso y el de la pantalla salen de la misma llamada a
`herramientas/generar-qr.py`, con la misma dirección: no puede haber uno impreso que
lleve a un sitio distinto del de la web. El de la pantalla queda escrito dentro del
HTML como un único trazo SVG (unos 1,5 KB), sin librerías ni imágenes. Va siempre
oscuro sobre blanco, también en modo oscuro, porque muchos lectores no reconocen un
QR invertido.

## Descartado a propósito

- **Selector de idioma**: el público es local.
- **Estadísticas de visitas**: GitHub Pages no da registros, así que cualquier contador
  sería un servicio externo. Si se añade algún día, la marca para distinguir las
  visitas del QR tiene que ir en el QR antes de imprimirlo.
- **Instalar como app / sin conexión (PWA)**: exige archivos aparte y un *service
  worker* que puede servir versiones viejas durante días. Nadie instala una tarjeta de
  visita; tiene sentido para la carta de un restaurante, no aquí.
- **Formulario de contacto**: necesitaría un servicio externo por el que pasarían los
  datos de quien escribe. El correo hace lo mismo.
- **Mapas incrustados, Google Fonts, píxeles de redes**: peso y rastreo de visitantes.

## Estructura

```
index.html                     La página entera: HTML, CSS, JS, logo, iconos y maquetas
imagenes/
  ├── icono-180.png            Icono para la pantalla de inicio del iPhone
  └── preview.jpg              Vista previa al compartir el enlace (1200 × 630)
herramientas/
  ├── procesar-fotos.py        Originales → versiones web limpias de metadatos
  └── generar-qr.py            Dirección → QR para imprimir y QR de la página
```

## Añadir imágenes

```bash
# 1. dejar los originales en "fotos originales/" (no se publica)
py herramientas/procesar-fotos.py
```

El script aplica la rotación, pasa a sRGB, limita a 1400 px, guarda en WebP por debajo
de 300 KB, borra EXIF y GPS y añade el © en XMP. Cada imagen conserva su nombre, en
minúsculas y sin tildes (`Mi Foto.JPG` → `mi-foto.webp`), así que añadir una nueva no
cambia el nombre de las demás. Después, declarar `width` y `height` en el `<img>`.

## Generar el QR

```bash
py -m pip install segno        # una sola vez, solo en este equipo
py herramientas/generar-qr.py https://qrafta.github.io/qrafta/
```

Deja en `qr/` (no se publica) un SVG para imprenta y un PNG de 2000 px, y reescribe
el QR de la página entre las marcas `<!-- QR:INICIO -->` y `<!-- QR:FIN -->`. Antes
de imprimir, escanear el PNG con un móvil y comprobar que abre la dirección buena:
un QR impreso ya no se puede corregir.

## Pendiente

- [ ] Diseño y tipografía definitivos
- [ ] Probar *Guardar contacto* y *Compartir* en un iPhone y un Android reales
- [ ] Quitar `<meta name="robots" content="noindex">` el día del lanzamiento

## Créditos

Marca, logo y página: **© Qrafta**. [@qrafta.studio](https://www.instagram.com/qrafta.studio/)
