# Crop and colour-grade the portrait for the site palette. Edit the crop box and
# the hue/saturation targets below, then: python3 tools/portrait-grade.py
# (expects the original photo path in the src variable; writes portrait_graded.png)

import numpy as np
from PIL import Image, ImageFilter
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb

src = '/root/.claude/uploads/ad241b1c-67fc-5294-9da7-c30480f67705/7e68299a-image.jpg'
im = Image.open(src).convert('RGB')
x0, y0, x1, y1 = 460, 150, 1200, 1075          # 4:5 crop, Marnie on the right
im = im.crop((x0, y0, x1, y1))
rgb = np.asarray(im).astype(np.float32) / 255
hsv = rgb_to_hsv(rgb)
h, s, v = hsv[..., 0] * 360, hsv[..., 1], hsv[..., 2]
Hh, Ww = h.shape
yy, xx = np.mgrid[0:Hh, 0:Ww]

def soft(mask, r=3, close=0, grow=0):
    m = Image.fromarray((np.clip(mask, 0, 1) * 255).astype(np.uint8))
    if close:
        m = m.filter(ImageFilter.MaxFilter(close)).filter(ImageFilter.MinFilter(close))
    if grow:
        m = m.filter(ImageFilter.MaxFilter(grow))
    m = m.filter(ImageFilter.GaussianBlur(r))
    return np.asarray(m).astype(np.float32) / 255

# protect skin and hair: warm hues with real saturation
skin = ((h < 45) | (h > 340)) & (s > 0.2) & (v > 0.12)
protect = soft(skin.astype(np.float32), 2)

# wall: pinkish, low saturation, bright
wall = (((h > 300) | (h < 60)) & (s < 0.2) & (v > 0.45)).astype(np.float32)
wall = soft(wall, 2) * (1 - protect)

# board: green
board = ((h > 110) & (h < 185) & (s > 0.08) & (v < 0.75)).astype(np.float32)
board = soft(board, 1.5) * (1 - protect)

# jeans: blue, mid value
jeans = ((h > 190) & (h < 300) & (s > 0.06) & (v > 0.28) & (v < 0.85)).astype(np.float32)
jeans = soft(jeans, 2) * (1 - protect)

# jumper: very dark, not warm and not board-green, inside her torso box (crop coordinates)
torso = (xx > 425) & (xx < 690) & (yy > 320) & (yy < 800)
jumper = (torso & (v < 0.30) & (((h > 175) & (h < 330)) | (s < 0.10))).astype(np.float32)
jumper = soft(jumper, 1.5, close=9, grow=5) * (1 - protect)

# chalk ledge: the grey band below the board
ledge = ((yy > 672) & (yy < 704) & (s < 0.15) & (v > 0.35) & (v < 0.9)).astype(np.float32)
ledge = soft(ledge, 1.5) * (1 - protect) * (1 - jeans)

def recolour(hue=None, sat=None, val=None):
    """Return an RGB image with the whole frame transformed; composited later by mask."""
    H2, S2, V2 = hsv[..., 0].copy(), hsv[..., 1].copy(), hsv[..., 2].copy()
    if hue is not None: H2[...] = hue / 360
    if sat is not None: S2[...] = sat(S2)
    if val is not None: V2[...] = val(V2)
    return hsv_to_rgb(np.stack([H2, S2, V2], axis=-1))

layers = [
    (wall,   recolour(30,  lambda S: np.minimum(S, 0.09), lambda V: 1 - (1 - V) * 0.8)),   # warm cream
    (board,  recolour(116, lambda S: S * 0.55,            lambda V: V * 0.93)),            # muted deep green
    (jeans,  recolour(219, lambda S: S * 1.1,             lambda V: V * 0.92)),            # denim blue
    (jumper, recolour(190, lambda S: np.maximum(S, 0.22), lambda V: np.clip(V + 0.10, 0, 1))),  # dark teal
    (ledge,  recolour(27,  lambda S: np.maximum(S, 0.45), lambda V: V * 0.9)),             # wood
]
res = rgb.copy()
for w, layer in layers:
    w3 = w[..., None]
    res = res * (1 - w3) + layer * w3

# gentle lift of the shadows everywhere (filmic, like the reference)
hs = rgb_to_hsv(np.clip(res, 0, 1))
hs[..., 2] = hs[..., 2] + 0.05 * (1 - hs[..., 2]) ** 2
res = hsv_to_rgb(hs)

res = (np.clip(res, 0, 1) * 255).round().astype(np.uint8)
Image.fromarray(res).save('portrait_graded.png')
print('ok', res.shape)
