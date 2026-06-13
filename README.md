# Generador de continente para Wonderdraft

Genera la máscara de un continente titánico formado por 6 islas con costas
orgánicas, pensada para importarse en Wonderdraft como **imagen de referencia**
y calcar la línea de costa con la herramienta de landmass (evitando el land
wizard).

## Uso

```bash
pip install numpy Pillow
python3 continent_generator.py            # parámetros por defecto
python3 continent_generator.py --seed 12  # otra variación
python3 continent_generator.py --width 4096 --height 2560 --seed 3
```

Salida en `out/`:

- `continent_mask.png` — blanco = tierra, negro = agua. Para importar/calcar.
- `continent_preview.png` — versión coloreada solo para previsualizar.

## Cómo usarlo en Wonderdraft

1. Nuevo mapa con las mismas proporciones (por defecto 3200×2000, ratio 1.6).
2. *Overlay / Reference image* → cargá `continent_mask.png`.
3. Calcá la costa con la herramienta de **landmass**, usando la máscara de guía.
4. Quitá la imagen de referencia y seguí con relieve, bosques, etiquetas.

## Ajustes rápidos (arriba del script)

- `ISLANDS`: posición `(x, y)` y `radio` de cada isla, en fracciones del lienzo.
  Acercá los centros para estrechos más angostos; alejalos para mar abierto.
- `COAST_ROUGHNESS`: cuán quebrada es la costa (más alto = más recortada).
- `BASE_SCALE` / `NOISE_OCTAVES`: escala y detalle del ruido de costa.
- `--seed`: cambia la variación manteniendo la composición.
