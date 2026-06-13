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
<!-- Requiere Dataview con "Enable JavaScript Queries". Cambia los valores en "data" y los colores comentados abajo. -->
```dataviewjs
const cfg = {
  type: "radar",
  data: {
    labels: ["Physical Capability","Intelligence","Fast Thinking","Adaptability","Durability"], // nombres de los ejes
    datasets: [{
      label: "Stats",
      data: [10,10,10,10,10],                       // <-- los 5 valores (0 a 20)
      fill: true,
      backgroundColor: "rgba(163,113,247,0.35)",     // relleno (último número = opacidad 0–1)
      borderColor: "#a371f7",                         // color de la línea
      borderWidth: 2,
      pointBackgroundColor: "#a371f7",                // color de los puntos
      pointRadius: 3
    }]
  },
  options: {
    scales: { r: {
      min: 0, max: 20,                                // <-- tope de la escala
      ticks: { display: false },                      // números ocultos
      grid: { color: "rgba(255,255,255,0.15)" },      // color de la telaraña
      angleLines: { color: "rgba(255,255,255,0.15)" },// líneas radiales
      pointLabels: { color: "#e0e0e0", font: { size: 13 } } // color y tamaño de los nombres
    }},
    plugins: { legend: { display: false } }           // leyenda oculta
  }
};
window.renderChart(cfg, this.container);
```

## Gracia & Stuff
