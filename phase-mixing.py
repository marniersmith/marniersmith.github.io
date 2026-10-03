"""Draw the header image: level sets of a free-transport solution.

The solution of the free transport equation  d_t f + v d_x f = 0  with
initial datum  f_0(x, v) = exp(-v^2/2) (1 + a cos(k x))  is
f(t, x, v) = f_0(x - v t, v).  As t grows the level sets shear into thin
filaments in phase space, which is the mechanism behind phase mixing and
Landau damping.  This script writes phase-mixing.svg in the repository root.

Requires numpy and matplotlib:  python3 tools/phase-mixing.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

T, A, K = 3.2, 0.7, 1.0          # time, perturbation amplitude, wavenumber
W, H = 1600, 480                  # SVG viewBox size (aspect ratio matters)
NLEVELS = 11

x = np.linspace(0, 5 * np.pi, 700)
v = np.linspace(-2.4, 2.4, 240)
X, V = np.meshgrid(x, v)
F = np.exp(-V**2 / 2) * (1 + A * np.cos(K * (X - V * T)))
levels = np.linspace(0.08, 1.55, NLEVELS)

cs = plt.contour(X, V, F, levels=levels)
paths = []
for segs in cs.allsegs:
    for s in segs:
        s = s[::2] if len(s) > 6 else s
        px = s[:, 0] / (5 * np.pi) * W
        py = (1 - (s[:, 1] + 2.4) / 4.8) * H
        pts = " ".join(f"{a:.1f},{b:.1f}" for a, b in zip(px, py))
        paths.append(f'<polyline points="{pts}"/>')

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    'fill="none" stroke="#717b70" stroke-width="1.2" stroke-linejoin="round">\n'
    "<title>Phase mixing under free transport: level sets of "
    "f(t,x,v) = f_0(x - vt, v)</title>\n"
    + "\n".join(paths)
    + "\n</svg>\n"
)
with open("phase-mixing.svg", "w") as fh:
    fh.write(svg)
print(f"wrote phase-mixing.svg ({len(svg) // 1024} KB, {len(paths)} curves)")
