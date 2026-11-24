#!/usr/bin/env python3
"""Ideological Rivals thumbnail: a spiral galaxy split diagonally (writes the SVG; seeded, reproducible).
Lower left (us) white, upper right (the rivals) red; the four stars sit on arm dots of their side.
Usage: assets/thumbnail.py assets/thumbnail.svg && rsvg-convert -w 512 assets/thumbnail.svg -o ideological_rivals/thumbnail.png
"""
import math, random, sys
from pathlib import Path

W, CX, CY, R = 512, 256, 232, 215
WHITE = ("#c9d2e4", "#ffffff")
RED = ("#ff5a3c", "#ffc4b0")

def seam_y(x):  # the split: top left to bottom right, through the core
    return x + (CY - CX) + 9 * math.sin(x / 21)

def side(x, y):
    return "us" if y > seam_y(x) else "them"

def galaxy(seed, rot, n=1900):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        arm = i % 2
        t = rnd.random() ** 0.8
        ang = rot + arm * math.pi + t * 3.6 * math.pi / 2 + rnd.gauss(0, 0.28 * (1 - t) + 0.10)
        rad = R * (0.08 + 0.92 * t) + rnd.gauss(0, R * 0.045)
        x, y = CX + rad * math.cos(ang), CY + rad * math.sin(ang) * 0.62
        out.append(dict(x=x, y=y, r=rnd.uniform(0.5, 1.7) * (1.3 - 0.6 * t), op=rnd.uniform(0.35, 0.95), t=t))
    for _ in range(550):  # core haze
        a = rnd.uniform(0, 2 * math.pi); d = abs(rnd.gauss(0, R * 0.12))
        out.append(dict(x=CX + d * math.cos(a), y=CY + d * math.sin(a) * 0.62, r=rnd.uniform(0.6, 1.6), op=rnd.uniform(0.3, 0.8), t=0))
    for d in out:
        d["side"] = side(d["x"], d["y"])
    return out

def arm_dot_near(dots, want_side, tx, ty):
    """The bright arm dot of a side closest to (tx, ty), away from the seam and the core."""
    ok = [d for d in dots if d["side"] == want_side and 0.45 < d["t"] < 0.95 and d["op"] > 0.6
          and abs(d["y"] - seam_y(d["x"])) > 30]
    return min(ok, key=lambda d: (d["x"] - tx) ** 2 + (d["y"] - ty) ** 2)

def star(d, col, gid, r, glow):
    x, y = round(d["x"], 1), round(d["y"], 1)
    return (f'<circle cx="{x}" cy="{y}" r="{glow}" fill="url(#glow{gid})"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>'
            f'<circle cx="{x}" cy="{y}" r="{r + 2}" fill="none" stroke="{col}" stroke-width="2"/>')

def main(out):
    dots = galaxy(seed=11, rot=1.1)
    rnd = random.Random(2)
    field = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, W):.0f}" r="{rnd.uniform(.4, 1.2):.1f}" fill="#fff" opacity="{rnd.uniform(.2, .55):.2f}"/>' for _ in range(90))
    body = [f"""<defs>
  <radialGradient id="bg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#141a2e"/><stop offset="1" stop-color="#05070e"/></radialGradient>
  <radialGradient id="glowus"><stop offset="0" stop-color="#ffffff" stop-opacity=".9"/><stop offset="1" stop-color="#c9d2e4" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowthem"><stop offset="0" stop-color="{RED[1]}" stop-opacity=".9"/><stop offset="1" stop-color="{RED[0]}" stop-opacity="0"/></radialGradient>
  <radialGradient id="core"><stop offset="0" stop-color="#fff" stop-opacity=".8"/><stop offset=".4" stop-color="#f0e6ee" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{W}" fill="url(#bg)"/>""", field]
    for d in dots:
        pal = WHITE if d["side"] == "us" else RED
        body.append(f'<circle cx="{d["x"]:.1f}" cy="{d["y"]:.1f}" r="{d["r"]:.2f}" fill="{pal[0 if d["op"] < 0.75 else 1]}" opacity="{d["op"]:.2f}"/>')
    body.append(f'<circle cx="{CX}" cy="{CY}" r="62" fill="url(#core)"/>')
    seam = " ".join(f"{x},{seam_y(x):.1f}" for x in range(125, 390, 5))
    body.append(f'<polyline points="{seam}" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="9"/>')
    body.append(f'<polyline points="{seam}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="2"/>')
    # us: lower left; the rivals: spread over the upper right arms
    body.append(star(arm_dot_near(dots, "us", 110, 300), WHITE[0], "us", 6, 26))
    for tx, ty in ((250, 120), (420, 170), (440, 290)):
        body.append(star(arm_dot_near(dots, "them", tx, ty), RED[0], "them", 5, 22))
    body.append('<text x="256" y="436" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="700" font-size="44" letter-spacing="2" fill="#f2f5fb">IDEOLOGICAL</text>')
    body.append(f'<text x="256" y="478" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="400" font-size="34" letter-spacing="14" fill="{RED[1]}">RIVALS</text>')
    Path(out).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}">\n' + "\n".join(body) + "\n</svg>\n")

main(sys.argv[1])
