#!/usr/bin/env python3
"""Genera la mascara de un continente titanico formado por varias islas.

Salida:
  - out/continent_mask.png   -> blanco = tierra, negro = agua (para calcar/importar)
  - out/continent_preview.png -> version coloreada para previsualizar

La mascara esta pensada para importarse en Wonderdraft como imagen de
referencia y calcar la costa con la herramienta de landmass, evitando el
land wizard.
"""

from __future__ import annotations

import argparse
import os

import numpy as np
from PIL import Image, ImageFilter

# --------------------------------------------------------------------------
# Parametros por defecto. Todo es ajustable por linea de comandos.
# --------------------------------------------------------------------------
DEFAULT_W = 3200
DEFAULT_H = 2000
DEFAULT_SEED = 7

# Islas: (x, y, radio) en fracciones del ancho/alto. Radio en fraccion del
# lado menor. Pensadas para solaparse apenas y leerse como un continente
# unico partido por estrechos.
ISLANDS = [
    (0.30, 0.40, 0.17),  # oeste grande
    (0.50, 0.27, 0.15),  # norte
    (0.69, 0.38, 0.16),  # este grande
    (0.40, 0.64, 0.14),  # suroeste
    (0.58, 0.60, 0.14),  # sur-centro
    (0.76, 0.66, 0.13),  # sureste
]

COAST_ROUGHNESS = 0.78  # cuanto deforma el ruido la linea de costa
NOISE_OCTAVES = 6
BASE_SCALE = 260        # px de la frecuencia mas baja del ruido


def smooth_noise(shape, scale, rng):
    """Ruido suave: grilla aleatoria de baja resolucion reescalada con bicubica."""
    h, w = shape
    gh = max(2, int(h / scale))
    gw = max(2, int(w / scale))
    grid = (rng.random((gh, gw)) * 255).astype("uint8")
    img = Image.fromarray(grid).resize((w, h), Image.BICUBIC)
    return np.asarray(img, dtype="float32") / 255.0


def fractal_noise(shape, rng, octaves=NOISE_OCTAVES, base_scale=BASE_SCALE,
                  persistence=0.5):
    """Suma de octavas de ruido -> campo fractal en [0, 1]."""
    total = np.zeros(shape, dtype="float32")
    amp, norm, scale = 1.0, 0.0, float(base_scale)
    for _ in range(octaves):
        total += amp * smooth_noise(shape, max(1.0, scale), rng)
        norm += amp
        amp *= persistence
        scale /= 2.0
    return total / norm


def build_landmask(w, h, seed):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype("float32")
    short = min(w, h)

    coast = fractal_noise((h, w), rng)            # detalle fino de la costa
    warp = fractal_noise((h, w), rng, base_scale=BASE_SCALE * 2)  # ondas grandes

    land = np.zeros((h, w), dtype="float32")
    for fx, fy, fr in ISLANDS:
        cx, cy, r = fx * w, fy * h, fr * short
        dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r  # 0 centro, 1 borde
        # Deforma la costa con ruido + desplazamiento de baja frecuencia.
        edge = dist + (coast - 0.5) * COAST_ROUGHNESS + (warp - 0.5) * 0.4
        # Cada isla aporta su "altura"; al sumar, las cercanas se funden.
        land = np.maximum(land, 1.0 - edge)

    mask = land > 0.0

    # Limpia islotes minusculos de ruido suelto en el agua.
    img = Image.fromarray((mask * 255).astype("uint8"))
    img = img.filter(ImageFilter.MedianFilter(size=5))
    return np.asarray(img, dtype="uint8") > 127


def colorize(mask):
    """Preview: agua azul, tierra verde, costa mas clara."""
    h, w = mask.shape
    out = np.zeros((h, w, 3), dtype="uint8")
    out[~mask] = (38, 78, 120)   # agua
    out[mask] = (96, 132, 86)    # tierra

    edge = Image.fromarray((mask * 255).astype("uint8")).filter(
        ImageFilter.FIND_EDGES)
    edge = np.asarray(edge) > 40
    out[edge] = (224, 214, 180)  # costa clara
    return Image.fromarray(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--width", type=int, default=DEFAULT_W)
    ap.add_argument("--height", type=int, default=DEFAULT_H)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    mask = build_landmask(args.width, args.height, args.seed)

    mask_img = Image.fromarray((mask * 255).astype("uint8"))
    mask_path = os.path.join(args.out, "continent_mask.png")
    preview_path = os.path.join(args.out, "continent_preview.png")
    mask_img.save(mask_path)
    colorize(mask).save(preview_path)

    pct = 100.0 * mask.mean()
    print(f"Tierra: {pct:.1f}% del lienzo")
    print(f"Mascara:  {mask_path}")
    print(f"Preview:  {preview_path}")


if __name__ == "__main__":
    main()
