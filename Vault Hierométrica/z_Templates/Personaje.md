---
descripción: 
Título: 
Alias: 
Raza: 
Muerte: 
Afiliación: 
Grupo: 
Gracia: 
Dominio: 
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
> Muerte | `=this["Muerte"]` |
> Afiliación | `=this["Afiliación"]` |
> ###### [[Hierométrica]]
> Campo |  Valor |
> ---|---|
> Dominio | `=this["Dominio"]` |
> Gracia | `=this["Gracia"]` |

# `=this.file.name`

## Apariencia y Carácter

## Cualificaciones

## Historia

## Citas

## Estadísticas
<!-- Cambia SOLO los 5 números de "data" (escala 0–20). Requiere Dataview con "Enable JavaScript Queries". -->
```dataviewjs
const cfg = {
  type: "radar",
  data: {
    labels: ["Physical Capability","Intelligence","Fast Thinking","Adaptability","Durability"],
    datasets: [{ label: "Stats", data: [10,10,10,10,10], fill: true }]
  },
  options: {
    scales: { r: { min: 0, max: 20, ticks: { display: false } } },
    plugins: { legend: { display: false } }
  }
};
window.renderChart(cfg, this.container);
```

## Gracia & Stuff
