"""
Gera as artes em pixel do README (pasta assets/).
Rode de novo sempre que quiser mudar um texto:  python gen_assets.py
"""
import os, random

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

RED, RED_DIM, RED_GHOST = "#E8132B", "#5C0A13", "#1E0508"
BLACK, PANEL = "#0A0A0A", "#111111"
WHITE, GRAY = "#F2EDE4", "#8C8782"
MONO = "'Courier New', Consolas, 'Liberation Mono', monospace"

# ---------- fonte bitmap 5x7 ----------
F = {
 "A":".###.|#...#|#...#|#####|#...#|#...#|#...#","B":"####.|#...#|#...#|####.|#...#|#...#|####.",
 "C":".###.|#...#|#....|#....|#....|#...#|.###.","D":"####.|#...#|#...#|#...#|#...#|#...#|####.",
 "E":"#####|#....|#....|####.|#....|#....|#####","F":"#####|#....|#....|####.|#....|#....|#....",
 "G":".###.|#...#|#....|#.###|#...#|#...#|.####","H":"#...#|#...#|#...#|#####|#...#|#...#|#...#",
 "I":".###.|..#..|..#..|..#..|..#..|..#..|.###.","J":"..###|...#.|...#.|...#.|...#.|#..#.|.##..",
 "K":"#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#","L":"#....|#....|#....|#....|#....|#....|#####",
 "M":"#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#","N":"#...#|#...#|##..#|#.#.#|#..##|#...#|#...#",
 "O":".###.|#...#|#...#|#...#|#...#|#...#|.###.","P":"####.|#...#|#...#|####.|#....|#....|#....",
 "Q":".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#","R":"####.|#...#|#...#|####.|#.#..|#..#.|#...#",
 "S":".####|#....|#....|.###.|....#|....#|####.","T":"#####|..#..|..#..|..#..|..#..|..#..|..#..",
 "U":"#...#|#...#|#...#|#...#|#...#|#...#|.###.","V":"#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
 "W":"#...#|#...#|#...#|#.#.#|#.#.#|#.#.#|.#.#.","X":"#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
 "Y":"#...#|#...#|.#.#.|..#..|..#..|..#..|..#..","Z":"#####|....#|...#.|..#..|.#...|#....|#####",
 "0":".###.|#...#|#..##|#.#.#|##..#|#...#|.###.","1":"..#..|.##..|..#..|..#..|..#..|..#..|.###.",
 "2":".###.|#...#|....#|...#.|..#..|.#...|#####","3":"####.|....#|....#|.###.|....#|....#|####.",
 "4":"...#.|..##.|.#.#.|#..#.|#####|...#.|...#.","5":"#####|#....|####.|....#|....#|#...#|.###.",
 "6":".###.|#....|#....|####.|#...#|#...#|.###.","7":"#####|....#|...#.|..#..|.#...|.#...|.#...",
 "8":".###.|#...#|#...#|.###.|#...#|#...#|.###.","9":".###.|#...#|#...#|.####|....#|....#|.###.",
 "/":"....#|....#|...#.|..#..|.#...|#....|#....","_":".....|.....|.....|.....|.....|.....|#####",
 "-":".....|.....|.....|#####|.....|.....|.....",".":".....|.....|.....|.....|.....|.....|..#..",
 "!":"..#..|..#..|..#..|..#..|..#..|.....|..#..","?":".###.|#...#|....#|...#.|..#..|.....|..#..",
 ":":".....|..#..|..#..|.....|..#..|..#..|.....","<":"...#.|..#..|.#...|#....|.#...|..#..|...#.",
 ">":".#...|..#..|...#.|....#|...#.|..#..|.#...","(":"...#.|..#..|.#...|.#...|.#...|..#..|...#.",
 ")":".#...|..#..|...#.|...#.|...#.|..#..|.#...","#":".#.#.|.#.#.|#####|.#.#.|#####|.#.#.|.#.#.",
 "{":"..##.|.#...|.#...|#....|.#...|.#...|..##.","}":".##..|...#.|...#.|....#|...#.|...#.|.##..",
 "+":".....|..#..|..#..|#####|..#..|..#..|.....","=":".....|.....|#####|.....|#####|.....|.....",
 "*":".....|#.#.#|.###.|#####|.###.|#.#.#|.....","'":"..#..|..#..|.....|.....|.....|.....|.....",
 " ":".....|.....|.....|.....|.....|.....|.....",
}
F = {k: v.split("|") for k, v in F.items()}

def text_w(t, s):  # largura em px de um texto pixel
    return (len(t) * 6 - 1) * s

def pixel_text(t, x, y, s, fill, gap=None, extra=""):
    """Desenha texto como blocos de pixel (estilo LCD, com pequeno espaço entre pixels)."""
    if gap is None:
        gap = 0 if s < 4 else max(1, s // 7)
    out = []
    for i, ch in enumerate(t.upper()):
        g = F.get(ch, F["?"])
        for r, row in enumerate(g):
            for c, px in enumerate(row):
                if px == "#":
                    out.append(f'<rect x="{x + (i*6 + c)*s}" y="{y + r*s}" width="{s-gap}" height="{s-gap}"/>')
    return f'<g fill="{fill}" {extra}>' + "".join(out) + "</g>"

def sprite(rows, x, y, s, colors, gap=0, extra=""):
    out = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in colors:
                out.append(f'<rect x="{x+c*s}" y="{y+r*s}" width="{s-gap}" height="{s-gap}" fill="{colors[ch]}"/>')
    return f"<g {extra}>" + "".join(out) + "</g>"

def defs(extra_css=""):
    return f"""<defs>
  <pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="1" height="1" fill="#1C1C1C"/></pattern>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect y="3" width="4" height="1" fill="#000" opacity=".35"/></pattern>
</defs>
<style>
  .blink {{ animation: blink 1.1s steps(1) infinite; }}
  .flick {{ animation: flick 2.4s steps(1) infinite; }}
  .flick2 {{ animation: flick 2.4s steps(1) -1.2s infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes flick {{ 0%,100% {{ opacity: 1; }} 33% {{ opacity: .25; }} 66% {{ opacity: .7; }} }}
  {extra_css}
  @media (prefers-reduced-motion: reduce) {{ .blink, .flick, .flick2 {{ animation: none; }} }}
</style>"""

def save(name, w, h, body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges">{body}</svg>'
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)

# ---------- ícones do "visor" ----------
SIGNAL = ["....#", "...##", "..###", ".####", "#####"]
BATTERY = [".##.", "####", "#..#", "####", "#..#", "####", "#..#", "####"]
CUP = [
    "..s..s..s.....",
    ".s..s..s......",
    "..s..s..s.....",
    "..............",
    "##########....",
    "#cccccccc###..",
    "#cccccccc#..#.",
    "#cccccccc#..#.",
    "#cccccccc###..",
    ".#cccccc#.....",
    "..######......",
    "##############",
]

# ---------- BANNER ----------
def banner():
    W, H = 1280, 468
    random.seed(7)
    b = [defs(), f'<rect width="{W}" height="{H}" fill="{BLACK}"/>', f'<rect width="{W}" height="{H}" fill="url(#dots)"/>']
    # fantasma ao fundo (como os números apagados do print da Nokia)
    # faixa superior (o "visor") + ícones
    b.append(f'<rect width="{W}" height="64" fill="{RED}"/>')
    b.append(sprite(SIGNAL, 32, 18, 6, {"#": BLACK}))
    b.append(sprite(BATTERY, W - 58, 14, 5, {"#": BLACK}))
    mw = text_w("MENU", 3) + 24
    b.append(f'<rect x="{(W-mw)//2}" y="16" width="{mw}" height="33" fill="none" stroke="{BLACK}" stroke-width="3"/>')
    b.append(pixel_text("MENU", (W-mw)//2 + 12, 22, 3, BLACK))
    b.append(pixel_text("GUILHERMEFONTESDEV", 82, 22, 3, BLACK))
    b.append(pixel_text("SSA-BR", W - 58 - 16 - text_w("SSA-BR", 3), 22, 3, BLACK))
    # dissolve em pixels do vermelho para o preto
    cell = 12
    for row in range(5):
        dens = [0.80, 0.55, 0.33, 0.17, 0.07][row]
        for col in range(W // cell):
            if random.random() < dens:
                cls = ' class="flick"' if random.random() < .06 else (' class="flick2"' if random.random() < .06 else "")
                b.append(f'<rect{cls} x="{col*cell}" y="{64 + row*cell}" width="{cell}" height="{cell}" fill="{RED}"/>')
    # etiqueta //LAUNCH-style
    tag = "//HELLO_WORLD"
    tw = text_w(tag, 3) + 20
    b.append(f'<rect x="64" y="136" width="{tw}" height="37" fill="{RED}"/>')
    b.append(pixel_text(tag, 74, 144, 3, BLACK))
    # nome
    b.append(pixel_text("GUILHERME", 64, 192, 14, RED))
    b.append(pixel_text("FONTES", 64, 304, 14, RED))
    cx = 64 + text_w("FONTES", 14) + 2 * 14
    b.append(f'<rect class="blink" x="{cx}" y="304" width="{5*14-2}" height="{7*14-2}" fill="{RED}"/>')
    # xícara (Java) com vapor piscando
    b.append(sprite(CUP[:3], 1000, 210, 12, {"s": GRAY}, gap=2, extra='class="flick"'))
    b.append(sprite(CUP[3:], 1000, 210 + 36, 12, {"#": RED, "c": RED_DIM}, gap=2))
    # subtítulo
    b.append(pixel_text("BACK-END DEVELOPER  //  JAVA . SPRING . NODE.JS . SQL", 64, 304 + 98 + 28, 3, WHITE))
    b.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    save("banner.svg", W, H, "".join(b))

# ---------- CABEÇALHOS DE SEÇÃO ----------
def header(slug, label, num):
    W, H = 1280, 64
    s = 4
    tw = text_w(label, s) + 28
    b = [defs(), f'<rect width="{W}" height="{H}" fill="{BLACK}"/>']
    b.append(f'<rect x="0" y="8" width="{tw}" height="48" fill="{RED}"/>')
    b.append(f'<rect x="{tw}" y="8" width="8" height="8" fill="{RED}"/><rect x="{tw}" y="48" width="8" height="8" fill="{RED}"/>')
    b.append(pixel_text(label, 14, 18, s, BLACK))
    nw = text_w(num, 4)
    x = tw + 32
    while x < W - nw - 40:
        b.append(f'<rect x="{x}" y="30" width="6" height="6" fill="{RED_DIM}"/>')
        x += 16
    b.append(f'<rect class="blink" x="{W - nw - 30}" y="18" width="4" height="28" fill="{RED}"/>')
    b.append(pixel_text(num, W - nw - 8, 18, 4, RED))
    save(f"h-{slug}.svg", W, H, "".join(b))

# ---------- CARDS DE PROJETO ----------
def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > n:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def notched(x, y, w, h, n):
    return (f"{x+n},{y} {x+w-n},{y} {x+w-n},{y+n} {x+w},{y+n} {x+w},{y+h-n} {x+w-n},{y+h-n} "
            f"{x+w-n},{y+h} {x+n},{y+h} {x+n},{y+h-n} {x},{y+h-n} {x},{y+n} {x+n},{y+n}")

def card(slug, title, tag, role, desc, chips, status, w=640, h=340, title_s=5, desc_chars=48, blink_status=False):
    b = [defs(), f'<rect width="{w}" height="{h}" fill="{BLACK}"/>']
    b.append(f'<polygon points="{notched(4, 4, w-8, h-8, 8)}" fill="{PANEL}" stroke="{RED}" stroke-width="4"/>')
    # barra de título
    b.append(f'<rect x="12" y="12" width="{w-24}" height="28" fill="{RED}"/>')
    b.append(pixel_text(f"> {slug}.EXE", 22, 19, 2, BLACK))
    b.append(sprite(["#.#.#", ".....", "#.#.#"], w - 46, 21, 3, {"#": BLACK}))
    # título
    b.append(pixel_text(title, 28, 62, title_s, RED))
    ty = 62 + 7 * title_s + 18
    b.append(f'<text x="28" y="{ty}" font-family="{MONO}" font-size="15" font-weight="700" fill="{RED}">{esc(tag)}</text>')
    if role:
        ty += 22
        b.append(f'<text x="28" y="{ty}" font-family="{MONO}" font-size="15" fill="{GRAY}">{esc(role)}</text>')
    ty += 30
    for line in wrap(desc, desc_chars):
        b.append(f'<text x="28" y="{ty}" font-family="{MONO}" font-size="16" fill="{WHITE}">{esc(line)}</text>')
        ty += 22
    # chips
    cx, cy = 28, h - 62
    for c in chips:
        cw = len(c) * 9 + 20
        if cx + cw > w - 28:
            cx, cy = 28, cy + 0  # sem quebra; mantém numa linha
            break
        b.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="26" fill="none" stroke="{RED}" stroke-width="2"/>')
        b.append(f'<text x="{cx + cw/2}" y="{cy + 18}" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{RED}">{esc(c)}</text>')
        cx += cw + 8
    # status
    if status:
        sw = len(status) * 9 + 34
        b.append(f'<rect x="{w - sw - 24}" y="56" width="{sw}" height="26" fill="{RED}"/>')
        cls = 'class="blink" ' if blink_status else ""
        b.append(f'<rect {cls}x="{w - sw - 14}" y="65" width="8" height="8" fill="{BLACK}"/>')
        b.append(f'<text x="{w - 24 - 10}" y="74" text-anchor="end" font-family="{MONO}" font-size="14" font-weight="700" fill="{BLACK}">{esc(status)}</text>')
    b.append(f'<rect width="{w}" height="{h}" fill="url(#scan)" opacity=".5"/>')
    save(f"card-{slug.lower()}.svg", w, h, "".join(b))

# ---------- RODAPÉ ----------
def footer():
    W, H = 1280, 200
    random.seed(3)
    b = [defs(), f'<rect width="{W}" height="{H}" fill="{BLACK}"/>', f'<rect width="{W}" height="{H}" fill="url(#dots)"/>']
    cell = 12
    for row in range(4):
        dens = [0.07, 0.17, 0.4, 0.75][row]
        for col in range(W // cell):
            if random.random() < dens:
                b.append(f'<rect x="{col*cell}" y="{H - 40 - (4-row)*cell}" width="{cell}" height="{cell}" fill="{RED}"/>')
    b.append(f'<rect y="{H-40}" width="{W}" height="40" fill="{RED}"/>')
    t1 = "THANKS FOR VISITING"
    b.append(pixel_text(t1, (W - text_w(t1, 5)) // 2, 26, 5, WHITE))
    t2 = "PRESS START TO CONTINUE"
    b.append(pixel_text(t2, (W - text_w(t2, 3)) // 2, 76, 3, RED, extra='class="blink"'))
    t3 = "(C) 2026 GUILHERME FONTES"
    b.append(pixel_text(t3, (W - text_w(t3, 2)) // 2, H - 27, 2, BLACK))
    b.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    save("footer.svg", W, H, "".join(b))

if __name__ == "__main__":
    banner()
    for i, (slug, label) in enumerate([
        ("about", "//ABOUT_ME"), ("stack", "//TECH_STACK"), ("projects", "//FEATURED_PROJECTS"),
        ("building", "//BUILDING_NOW"), ("learning", "//CURRENTLY_LEARNING"), ("stats", "//GITHUB_STATS"),
        ("education", "//EDUCATION"), ("hobbies", "//OFFLINE_MODE"), ("contact", "//CONTACT"),
    ], 1):
        header(slug, label, f"{i:02d}")
    card("ECOFLUX", "ECOFLUX", "TCC // SENAI CIMATEC", "role: project manager + back-end dev",
         "Full-stack IoT energy management system. Reads real consumption data from a Tuya smart plug through a Python (tinytuya) pipeline into a Node.js API, with an AI chatbot built in.",
         ["Node.js", "Express", "PostgreSQL", "Supabase", "Tuya IoT"], "SHIPPED")
    card("PSICOGEST", "PSICOGEST", "CLINIC MANAGEMENT SYSTEM", "full-stack // node.js + express",
         "Full-stack clinic management system: a Node.js + Express API with an HTML, CSS and JavaScript front-end, MVC architecture, JWT authentication and role-based access control. Fully documented.",
         ["Node.js", "Express", "HTML", "CSS", "JS", "MVC", "JWT", "RBAC"], "PORTFOLIO")
    small = dict(w=420, h=300, title_s=4, desc_chars=30, blink_status=True)
    card("NEXUSBANK", "NEXUSBANK", "BANKING SIMULATOR", "",
         "Pure Java banking simulator applying SOLID, records, sealed classes, generics and the Stream API.",
         ["Java", "SOLID", "Streams"], "IN PROGRESS", **small)
    card("LIVEQUIZ", "LIVE QUIZ", "KAHOOT-STYLE QUIZ", "",
         "Live quiz platform with real-time rooms, built to study Spring and real-time back-end in depth.",
         ["Java", "Spring Boot"], "IN PROGRESS", **small)
    card("HEMOCENTRO", "HEMOCENTRO", "BLOOD BANK SYSTEM", "",
         "Blood bank management system with 5+ entities, wired to a relational database with pure JDBC.",
         ["Java", "JDBC", "SQL"], "UP NEXT", **small)
    footer()
    print("ok:", sorted(os.listdir(OUT)))
