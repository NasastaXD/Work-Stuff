# Vault traducido — "Vault Hierométrica"

Traducción al español de la plantilla de Vault de Obsidian que venía en `Archivo.zip`.
El vault traducido está en la carpeta **`Vault Hierométrica/`**. El zip original se conserva como respaldo.

## Qué se hizo

- **Todo el contenido al español**: carpetas, nombres de archivo, propiedades (frontmatter), títulos de sección, etiquetas de los infobox y botones del panel de inicio.
- **Sistema de magia**: se renombró el sistema del template (*Thaumaturgy / Thaumaturgic*) a **Hierométrica / hierométrico**. Se creó la página central `1. Enciclopedia/Hierométrica.md` (a ella enlazan las fichas de personaje con `[[Hierométrica]]`).
- **Eliminado** (a tu pedido): la sección **Cultura** (costumbres, lenguas, tradiciones, mitos, sociedad, profesiones, títulos) y la nota **Travel Calculator** (cálculo de viajes de PF2e). Plantillas borradas: `Culture`, `Myth`, `Profession`, `Title`, `Tradition`.
- **Rescatado a secciones propias** (porque son importantes en tu obra): **Religión** (Deidades + Religiones) y **Tecnología** (Objetos), antes anidadas dentro de Cultura.
- **Calendario**: se conservó (no lo marcaste para eliminar).
- **Bugs corregidos del original**: la plantilla de Personaje venía a medio traducir y con referencias rotas; también `PerentLocation` (typo), `=this.Wealth` y `=fc-end`. Todo quedó funcionando.

## Decisiones técnicas importantes (para que nada se rompa)

1. **Carpetas de sistema sin renombrar**: `z_Templates/` y `z_Assets/` mantienen su nombre original. Tu configuración de Templater (carpeta de plantillas) y las imágenes apuntan a ellas desde tu carpeta `.obsidian`, que **no** venía en el zip. Si las renombras, actualiza esas rutas en los ajustes de Obsidian.
2. **Propiedades con acentos**: las claves del frontmatter están en español (p. ej. `Líder`, `Población`). En los infobox se usan con notación de corchetes — `` `=this["Líder"]` `` — para que Dataview soporte acentos y espacios sin fallar.
3. **Calendario (Calendarium)**: las plantillas usan `fc-calendar: Calendario`. Ese valor debe coincidir con el nombre del calendario que crees en el plugin Calendarium. Nombra tu calendario **"Calendario"** o cambia ese valor en las plantillas.
4. **Líneas de tiempo (Timelines)**: se tradujeron de forma consistente — `grand timeline` → `cronología magna`, `main timeline` → `cronología principal` — tanto en el frontmatter como en los bloques `aat-vertical`.
5. **Prompts de Copilot** (`copilot/`): se dejaron en inglés porque son comandos del plugin de IA, no contenido de worldbuilding.

## Cómo usarlo

Abre la carpeta `Vault Hierométrica/` como vault en Obsidian (o copia su contenido dentro de tu vault actual). Necesitarás los plugins: Dataview, Templater, Meta Bind, Calendarium, Timelines (AAT), Leaflet, Charts, Banners y Excalidraw.
