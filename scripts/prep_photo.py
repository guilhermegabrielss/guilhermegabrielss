#!/usr/bin/env python3
"""
Prepare the portrait photo for clean ASCII conversion:
  1. Handles transparency (RGBA) and composites onto pure white
  2. Crops around the upper body / portrait area
  3. Stretches tones and adjusts contrast so skin lands near white
     and hair/facial features/dark clothing stay dark
  4. Saves square source-prepped.png for make_ascii_svg.py
"""
import os
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.webp")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

im = Image.open(INP)

# If transparent WebP or PNG, composite onto pure white
if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
    im_rgba = im.convert("RGBA")
    alpha = im_rgba.split()[-1]
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im_rgba, mask=alpha)
    rgb = bg
else:
    rgb = im.convert("RGB")

w, h = rgb.size

# Focused square crop on upper body / head & shoulders
# For portrait.webp (731x887): upper body square from y=25 to 725
if w == 731 and h == 887:
    side = 700
    crop_box = (15, 25, 15 + side, 25 + side)
    rgb = rgb.crop(crop_box)
else:
    # Generic center crop
    side = min(w, h)
    left = (w - side) // 2
    top = max(0, int(h * 0.05))
    top = min(top, h - side)
    rgb = rgb.crop((left, top, left + side, top + side))

# Convert to grayscale
gray = rgb.convert("L")

# Autocontrast to expand dynamic range
gray = ImageOps.autocontrast(gray, cutoff=2)

# Slight contrast boost
enhancer = ImageEnhance.Contrast(gray)
gray = enhancer.enhance(1.15)

gray.save(OUT)
print(f"Prepped photo saved to {OUT} ({gray.size[0]}x{gray.size[1]})")
