#!/usr/bin/env python3
"""
Build a neofetch-style info card SVG that sits beside the ASCII portrait.
Matching 840 x 880 canvas for pixel-perfect symmetrical alignment.

Shows system info, role, tech stack, and highlights with subtle staggered
slide-and-fade animations that GitHub renders natively via SMIL/CSS.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 840, 880
PAD = 32
TITLEBAR_H = 38
KEY_X = PAD + 12
VAL_X = PAD + 180
LINE_H = 31

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
KEY = "#ffa657"
SECTION = "#58a6ff"
GREEN = "#39d353"
ACCENT = "#22d3ee"

ROWS = [
    ("host",),
    ("gap",),
    ("kv", "OS", "macOS Sonoma (Darwin arm64)"),
    ("kv", "Host", "Guilherme Gabriel (GG)"),
    ("kv", "Role", "Fullstack Developer & AI Builder"),
    ("kv", "Education", "Análise e Desenv. de Sistemas"),
    ("kv", "Location", "Pimenta Bueno, RO · Brasil"),
    ("kv", "Timezone", "America/Cuiaba (UTC-4)"),
    ("kv", "Experience", "4 years coding (since 2022)"),
    ("kv", "Portfolio", "https://guilhermegabriel.tech"),
    ("gap",),
    ("sec", "Tech Stack"),
    ("kv", "Frontend", "React, Next.js, Vue, TypeScript, Tailwind"),
    ("kv", "Backend", "Node.js, Express, Python, Zod, REST APIs"),
    ("kv", "AI & LLMs", "OpenAI API, Function Calling, Prompt Eng"),
    ("kv", "Cloud & Ops", "Cloudflare Workers, Git, GitLab, Docker"),
    ("kv", "Environment", "VS Code, Terminal (Zsh + Catppuccin)"),
    ("gap",),
    ("sec", "Highlights & Projects"),
    ("bul", "Estoque IA: TypeScript API com OpenAI structured output"),
    ("bul", "Rocketseat: 6 Certificações em IA, Node.js e Fullstack"),
    ("bul", "Portfólio: Next.js + Cloudflare Custom Domain"),
    ("gap",),
    ("palette",),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*18}" cy="{TITLEBAR_H/2}" r="6" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 5}" fill="{MUTED}" font-size="13" text-anchor="middle">guilherme@github: ~$ neofetch</text>')

y = TITLEBAR_H + 42
for i, row in enumerate(ROWS):
    kind = row[0]
    delay = 0.15 + i * 0.04
    if kind == "gap":
        y += LINE_H * 0.5
        continue
    if kind == "host":
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="20" font-weight="700">'
                 f'<tspan fill="{GREEN}">guilherme</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">github</tspan></text>'
                 f'<line x1="{KEY_X+185}" y1="{y-6:.1f}" x2="{W-PAD}" y2="{y-6:.1f}" stroke="{FRAME}" stroke-opacity="0.8" stroke-width="1.5"/>')
    elif kind == "sec":
        title = html.escape(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="17" font-weight="700">'
                 f'&#8212; {title}</text>'
                 f'<line x1="{KEY_X + 20 + len(row[1])*11}" y1="{y-6:.1f}" x2="{W-PAD}" y2="{y-6:.1f}" stroke="{FRAME}" stroke-opacity="0.8" stroke-width="1.5"/>')
    elif kind == "kv":
        key, val = html.escape(row[1]), html.escape(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="16.5" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="16.5">{val}</text>')
    elif kind == "bul":
        txt = html.escape(row[1])
        inner = (f'<circle cx="{KEY_X+6}" cy="{y-5:.1f}" r="3.5" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+22}" y="{y:.1f}" fill="{INK}" font-size="16.5">{txt}</text>')
    elif kind == "palette":
        colors1 = ["#21262d", "#ff5f56", "#39d353", "#f2cc60", "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3"]
        colors2 = ["#484f58", "#ff7b72", "#56d364", "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", "#ffffff"]
        boxes = []
        bx = KEY_X
        bw = 42
        bh = 20
        for c in colors1:
            boxes.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" rx="4" fill="{c}"/>')
            bx += bw + 8
        bx = KEY_X
        for c in colors2:
            boxes.append(f'<rect x="{bx}" y="{y+bh+6}" width="{bw}" height="{bh}" rx="4" fill="{c}"/>')
            bx += bw + 8
        inner = "".join(boxes)
        y += bh + 14
    else:
        continue

    if STATIC:
        parts.append(f"<g>{inner}</g>")
    else:
        anim = (f'<g opacity="0" transform="translate(0,8)">{inner}'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')
        parts.append(anim)
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)} bytes")
