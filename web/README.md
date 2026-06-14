# Códice web de Hierométrica

Generador de sitio estático que convierte el vault de Obsidian
(`Vault Hierométrica/`) en una web navegable: un códice/wiki de tu mundo.

## Qué hace

- Lee todas las notas `.md` del vault (omite plantillas, assets, copilot, etc.).
- Reconstruye los **infobox** de Dataview resolviendo `=this["Campo"]` con el frontmatter.
- Convierte los bloques `chart` y `dataviewjs` (radar) en **gráficos interactivos** con Chart.js.
- Hace **clicables los enlaces `[[wiki]]`** entre notas.
- Arma la **navegación por categorías** según las carpetas y un **buscador** en cliente.

## Generar el sitio localmente

```bash
pip install pyyaml
python3 web/build.py
```

Esto crea la carpeta `web/_site/`. Abrila con cualquier servidor estático, por ejemplo:

```bash
python3 -m http.server -d web/_site 8000
# y entrá a http://localhost:8000
```

> El sitio usa enlaces relativos planos, así que también podés abrir
> `web/_site/index.html` directamente, aunque un servidor local funciona mejor.

## Publicación automática (GitHub Pages)

El workflow `.github/workflows/pages.yml` reconstruye y publica el sitio en cada
push que toque el vault o la carpeta `web/`.

**Paso único manual** (una sola vez, en GitHub): andá a
**Settings → Pages → Build and deployment → Source** y elegí **GitHub Actions**.
Después de eso, cada cambio que subas al vault se publica solo.

## Cómo crece

El sitio se arma desde el vault tal cual. A medida que escribís notas nuevas
(personajes, lugares, etc.) y las subís, el códice se actualiza automáticamente.
No hace falta tocar el generador para agregar contenido.

### Notas de ejemplo

Se incluyeron unas notas de muestra para que el sitio no saliera vacío
(*La Ceniza*, *Orden del Verbo*, *Vael el Lector*, *Las Tierras Cenizas*).
Podés borrarlas o reemplazarlas cuando quieras; son solo demostración.

## Personalización

- **Estilo / colores**: `web/theme/style.css` (las variables de color están arriba).
- **Buscador y gráficos**: `web/theme/app.js`.
- **Banner de portada**: `web/theme/banner.webp`.
