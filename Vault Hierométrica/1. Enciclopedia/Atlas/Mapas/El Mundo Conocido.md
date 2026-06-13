```leaflet  
### Tutorial: [https://youtu.be/54EyMzJP5DU](https://youtu.be/54EyMzJP5DU)  
### El id debe ser único  
id: Mapa_Mundo_Conocido  
### Bloquea los marcadores para que no se puedan mover  
lock: true  
### Si es true, la vista del mapa se recentra al alejar el zoom.  
recenter: true  
### Si es true, desactiva el scroll del ratón para hacer zoom. Los botones de control siguen funcionando.  
noScrollZoom: true  
image: [[z_Assets/Misc/fantasy map.webp]]  
### Alto del mapa en píxeles x 1 / (Píxeles entre la barra de escala / 100)  
### Ancho del mapa en píxeles x 1 / (Píxeles entre la barra de escala / 100)  
### Esta fórmula requiere ajustes según tu mapa. La idea es determinar el número de unidades entre la barra de escala. Aquí dividimos entre 100 porque mi barra de escala mide en unidades de 100. Si la barra de tu mapa mide en unidades de 50, divide entre 50. El objetivo es calcular cuántos píxeles equivalen a 1 unidad.  
### Bounds se introduce como [Alto, Ancho]  
bounds: [[0,0], [1815.07, 2805.48]]  
height: 900px  
width: 95%  
### Define dónde empieza el mapa por defecto. Ponlo en el centro (la mitad) de tus bounds.  
lat: 907.53  
long: 1402.74  
### 0 es sin zoom. El zoom negativo aleja del mapa. El zoom positivo acerca al mapa.  
minZoom: -1.5  
### El zoom máximo es 18.  
maxZoom: 1.5  
### Pasa el ratón por encima del icono de Restablecer Zoom para ver tu nivel de zoom actual.  
defaultZoom: -1  
### Cuánto se acerca o aleja en cada paso. Puede llevar decimales.  
zoomDelta: 0.5  
### Es un texto, así que puede ser cualquier cosa. Cámbialo para que coincida con la escala de medida de tu mapa.  
unit: millas  
scale: 1  
darkMode: false  
```
