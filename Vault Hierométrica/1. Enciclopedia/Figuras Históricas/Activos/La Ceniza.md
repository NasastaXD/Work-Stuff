---
descripción: La Heredera del Fuego Silente
Título: Archicanciller de la Orden
Alias: La Ceniza
Raza: Humana
Muerte: 
Afiliación: "[[Orden del Verbo]]"
Grupo: Consejo Hierométrico
Gracia: Combustión Axiomática
Dominio: Calor / Entropía
Familia: 
Histórico: false
NoteIcon: npc
---

> [!infobox]
> # `=this.file.name`
> # <font size=3>*`=this["descripción"]`*</font>
> ![[z_Assets/Misc/ImagePlaceholder.webp|cover hsmall]]
> ###### Información Básica
> Campo |  Valor |
> ---|---|
> Título | `=this["Título"]` |
> Alias | `=this["Alias"]` |
> Raza | `=this["Raza"]` |
> Afiliación | `=this["Afiliación"]` |
> ###### [[Hierométrica]]
> Campo |  Valor |
> ---|---|
> Dominio | `=this["Dominio"]` |
> Gracia | `=this["Gracia"]` |

# `=this.file.name`

## Apariencia y Carácter
Alta, de mirada cansada y manos siempre cubiertas de hollín. Habla poco y mide cada palabra como si gastarlas tuviera un precio. Pertenece a la [[Orden del Verbo]].

## Cualificaciones
Domina la combustión axiomática a un nivel que la Orden considera peligroso. Capaz de leer una estructura hierométrica y deshacerla por dentro.

## Historia
Renunció a su apellido tras el incendio de la Biblioteca Baja. Desde entonces sirve a la Orden, aunque nadie sabe si por convicción o por penitencia.

## Citas
> "El fuego no destruye. Solo termina de leer lo que ya estaba escrito."

## Estadísticas
```dataviewjs
const cfg = {
  type: "radar",
  data: {
    labels: ["Physical Capability","Intelligence","Fast Thinking","Adaptability","Durability"],
    datasets: [{ label: "Stats", data: [8,18,15,12,9] }]
  }
};
window.renderChart(cfg, this.container);
```
