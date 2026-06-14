---
descripción: Ferviente de fé en Cristo.
Rol: Protagonista
Alias: «Enlighted One»
Raza: Humano
Muerte: Inexistencia
Afiliación: Sisifista
Ideología: Cristianismo
Gracia: ¡Destello!
Dominio: Extremo
Familia: Desiderio
Edad: 40 años
Histórico: false
NoteIcon: main-charactrer
PhysicalCapability: 8
Intelligence: 15
FastThinking: 16
Adaptability: 18
Durability: 6
---

> [!infobox]
> # `=this.file.name`
> # <font size=3>*`=this["descripción"]`*</font>
> ![[IMG_7169.webp]]
> ###### Información Básica
> Campo |  Valor |
> ---|---|
> Rol | `=this["Rol"]` |
> Edad | `=this["Edad"]` |
> Alias | `=this["Alias"]` |
> Raza | `=this["Raza"]` |
> Muerte | `=this["Muerte"]` |
> Afiliación | `=this["Afiliación"]` |
> Ideología | `=this["Ideología"]` |
> ###### [[Hierométrica]]
> Campo |  Valor |
> ---|---|
> Gracia | `=this["Gracia"]` |
> Dominio | `=this["Dominio"]` |

# `=this.file.name`

## Apariencia y Carácter
Dante Desiderio tiende a vestir un ropaje llamativo, con prendas largas como túnicas o trajes costosos confeccionados con el más fino hilo. Se preocupa bastante por su apariencia física, aunque siempre se muestra con un semblante descuidado; de hecho, su rostro y su cabello son los únicos aspectos desalineados de su ser.

Mide 1,79 metros de altura, posee una complexión delgada y carece de una masa muscular desarrollada. Sus ojos son de un color anaranjado brillante, aunque suele cambiar su tonalidad frente a las personas que acaba de conocer utilizando su Gracia, con el único fin de confundirlas. Tiende a cambiar de apariencia facial muy usualmente.

Dante es incapaz de percibir las diferencias entre el bien y el mal debido al uso excesivo de su Gracia durante sus tiempos como militante. Esto le provocó un daño neuronal que afectó sus percepciones morales; a raíz de ello, se reencaminó por un sendero en el que intenta buscar el bienestar de los demás para, de ese modo, sentirse integrado.

Mantiene una conducta sarcástica pero directa, y suele aclarar su propio sarcasmo justo después de expresarlo. A pesar de su apatía biológica, se preocupa genuinamente por quienes considera cercanos, o al menos eso es lo que él cree.

## Cualificaciones
- 11 años de Experiencia Militar como Estratega y posteriormente Militante estatal.
- 7 años de Experiencia como «Pater peccati» (Padre del Pecado), el máximo rol evangélico dentro del Imperio Sisifista.
- Expertise en combate a medias y larga distancia.
- Doctorado en Psicología y mágister en Hierométrica

## Historia
Nacido de una familia burgués, Dante creció rodeado de lujos en el Imperio Sisifista

## Citas


## Estadísticas
<!-- Edita los 5 números en el panel de Propiedades (PhysicalCapability, Intelligence, FastThinking, Adaptability, Durability). El gráfico se actualiza solo. -->
```dataviewjs
const p = dv.current();
const cfg = {
  type: "radar",
  data: {
    labels: ["Physical Capability","Intelligence","Fast Thinking","Adaptability","Durability"],
    datasets: [{
      label: "Stats",
      data: [p.PhysicalCapability, p.Intelligence, p.FastThinking, p.Adaptability, p.Durability],
      fill: true,
      backgroundColor: "rgba(163,113,247,0.35)",
      borderColor: "#a371f7",
      borderWidth: 2,
      pointBackgroundColor: "#a371f7",
      pointRadius: 3
    }]
  },
  options: {
    scales: { r: {
      min: 0, max: 20,
      ticks: { display: false },
      grid: { color: "rgba(255,255,255,0.15)" },
      angleLines: { color: "rgba(255,255,255,0.15)" },
      pointLabels: { color: "#e0e0e0", font: { size: 13 } }
    }},
    plugins: { legend: { display: false } }
  }
};
window.renderChart(cfg, this.container);
```

## Gracia & Stuff
