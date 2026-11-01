import re, os, sys, math, base64
HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS = os.path.join(HERE, "..", "..", "katharo-logo")
DIST = sys.argv[1]
os.makedirs(DIST, exist_ok=True)

def inner(name):
    s = open(os.path.join(LOGOS, name)).read()
    return re.search(r'<g fill="[^"]*">(.*)</g></svg>', s, re.S).group(1)

mark = inner("katharo-icon-gold-transparent.svg")
stack = inner("katharo-logo-gold-transparent.svg")
word_src = inner("katharo-logo-gold-transparent.svg")
# wordmark only = the path elements after the K + sparkle (first two paths)
paths = re.findall(r'<path[^>]*/>', word_src)
word = "".join(paths[2:])

CHECK = '<svg viewBox="0 0 256 256" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" d="M40 136l56 56L216 72"/></svg>'

# olive branch: a curved stem with paired leaves
def branch():
    out = ['<path d="M20 310 C60 230 90 150 170 20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>']
    def pt(t):
        p0, p1, p2, p3 = (20, 310), (60, 230), (90, 150), (170, 20)
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        dx = -3*(1-t)**2*p0[0] + 3*(1-t)**2*p1[0] - 6*(1-t)*t*p1[0] + 6*(1-t)*t*p2[0] - 3*t**2*p2[0] + 3*t**2*p3[0]
        dy = -3*(1-t)**2*p0[1] + 3*(1-t)**2*p1[1] - 6*(1-t)*t*p1[1] + 6*(1-t)*t*p2[1] - 3*t**2*p2[1] + 3*t**2*p3[1]
        return x, y, math.degrees(math.atan2(dy, dx))
    for i, t in enumerate([0.12, 0.22, 0.32, 0.42, 0.52, 0.62, 0.72, 0.82, 0.9]):
        x, y, a = pt(t)
        L = 30 - i * 1.6
        for side in (-1, 1):
            ang = a + side * (38 + (i % 2) * 6)
            cx = x + math.cos(math.radians(ang)) * L * 0.55
            cy = y + math.sin(math.radians(ang)) * L * 0.55
            out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{L*0.55:.1f}" ry="{L*0.16:.1f}" transform="rotate({ang:.1f} {cx:.1f} {cy:.1f})" fill="currentColor" opacity="{0.55 + 0.05*(i%3):.2f}"/>')
    x, y, a = pt(1.0)
    out.append(f'<ellipse cx="{x+4:.1f}" cy="{y-8:.1f}" rx="14" ry="4.5" transform="rotate({a:.1f} {x+4:.1f} {y-8:.1f})" fill="currentColor" opacity="0.6"/>')
    return "".join(out)

fav_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><rect width="1000" height="1000" rx="200" fill="#131209"/>'
           f'<g fill="#D4AF6A">{mark}</g></svg>')
favicon = "data:image/svg+xml;base64," + base64.b64encode(fav_svg.encode()).decode()

tpl = open(os.path.join(HERE, "index.tpl.html")).read()
tpl = tpl.replace('<legend style="padding:0;margin-bottom:8px"><label as="span">Tip de curățenie</label></legend>',
                  '<legend class="lg">Tip de curățenie</legend>')
tpl = tpl.replace('label .opt {', '.lg { padding: 0; margin-bottom: 8px; font-size: 14px; line-height: 20px; font-weight: 600; color: var(--on-ink); }\nlabel .opt {')
page = (tpl.replace("{{MARK}}", mark).replace("{{MARK_VB}}", "190 215 680 570")
        .replace("{{STACK}}", stack).replace("{{STACK_VB}}", "250 105 700 615")
        .replace("{{WORD}}", word).replace("{{WORD_VB}}", "260 520 680 195")
        .replace("{{BRANCH}}", branch()).replace("{{CHECK}}", CHECK).replace("{{FAVICON}}", favicon))
assert "{{" not in page, re.findall(r"\{\{\w+\}\}", page)

# Artifact preview body (skeleton is added at publish time)
open(os.path.join(DIST, "preview.html"), "w").write(page)

# Deployable full document
split = page.index('<a class="skip"')
head, body = page[:split], page[split:]
def doc(head, body, lang="ro"):
    return (f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}</head>\n<body>\n{body}\n</body>\n</html>\n')
open(os.path.join(DIST, "index.html"), "w").write(doc(head, body))

# Simple secondary pages sharing the brand
SUB_CSS = """<style>
:root{--ink:#131209;--line:#2E2A1C;--gold:#CDA45E;--gold-soft:#E9D3A0;--fg:#F2ECDF;--muted:#A69E8B;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--ink);color:var(--fg);font:16px/24px Manrope,"Segoe UI",system-ui,sans-serif}
.wrap{max-width:760px;margin:0 auto;padding:64px max(24px,env(safe-area-inset-right,0px)) 96px max(24px,env(safe-area-inset-left,0px))}
a{color:var(--gold-soft)}h1,h2{font-family:"Cormorant Garamond",Garamond,serif;font-weight:500;text-wrap:balance}
h1{font-size:60px;line-height:1;margin:48px 0 24px}h2{font-size:30px;line-height:36px;margin:40px 0 12px}p,li{color:var(--muted);text-wrap:pretty}
.back{display:inline-flex;gap:8px;align-items:center;text-decoration:none;font-weight:600;font-size:14px}
.note{border:1px solid var(--line);border-radius:16px;padding:16px 24px;color:var(--gold-soft);font-size:14px;line-height:20px}
.mark{width:56px;color:var(--gold)}
.btn{display:inline-flex;margin-top:32px;background:var(--gold);color:var(--ink);padding:12px 24px;border-radius:999px;font-weight:600;text-decoration:none}
:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
@media(max-width:600px){h1{font-size:48px}}
</style>"""
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500&family=Manrope:wght@400;600&display=swap">'
MARK_SVG = f'<svg class="mark" viewBox="190 215 680 570" aria-hidden="true"><g fill="currentColor">{mark}</g></svg>'
def sub(title, body):
    h = f'<title>{title} · Katharo Cleaning</title>\n<meta name="robots" content="noindex">\n<link rel="icon" href="{favicon}">\n{FONTS}\n{SUB_CSS}\n'
    b = f'<main class="wrap"><a class="back" href="index.html">← Înapoi la pagina principală</a>{body}</main>'
    return h, b

pages = {
 "confidentialitate.html": sub("Politica de confidențialitate", f"""
<h1>Politica de confidențialitate</h1>
<p class="note">Schiță. Completați datele firmei și verificați textul cu un consultant GDPR înainte de publicare.</p>
<h2>Ce date colectăm</h2><p>Prin formularul de ofertă colectăm numele, numărul de telefon, adresa de email (opțional), localitatea și detaliile despre spațiul de curățat.</p>
<h2>De ce le folosim</h2><p>Doar pentru a-ți trimite oferta și a programa lucrarea. Nu trimitem mesaje de marketing fără acordul tău și nu vindem datele.</p>
<h2>Cât le păstrăm</h2><p>Datele unei cereri fără comandă se șterg după 12 luni. Datele clienților se păstrează cât timp o cere legislația fiscală.</p>
<h2>Drepturile tale</h2><p>Poți cere oricând acces, rectificare sau ștergerea datelor. Operator: [denumirea firmei], CUI [cod], [adresă], [email de contact].</p>
"""),
 "termeni.html": sub("Termeni și condiții", f"""
<h1>Termeni și condiții</h1>
<p class="note">Schiță. Completați datele firmei și condițiile comerciale reale înainte de publicare.</p>
<h2>Oferta și prețul</h2><p>Prețul comunicat în oferta scrisă este fix pentru serviciile descrise. Lucrările suplimentare se fac doar cu acordul tău prealabil.</p>
<h2>Programare și anulare</h2><p>Poți reprograma sau anula gratuit cu cel puțin [24] de ore înainte de vizită.</p>
<h2>Garanția</h2><p>Dacă o zonă nu corespunde standardului promis, ne anunți în 24 de ore de la vizită și revenim să o refacem fără cost.</p>
<h2>Prestator</h2><p>[Denumirea firmei], CUI [cod], [nr. Registrul Comerțului], [adresă].</p>
"""),
 "404.html": sub("Pagina nu a fost găsită", f"""
<div style="margin-top:64px">{MARK_SVG}</div>
<h1>Aici nu e nimic de curățat.</h1>
<p>Pagina pe care o cauți nu există sau a fost mutată. Verifică adresa sau întoarce-te la pagina principală.</p>
<a class="btn" href="index.html">Mergi la pagina principală</a>
"""),
}
for fn, (h, b) in pages.items():
    open(os.path.join(DIST, fn), "w").write(doc(h, b))
    # artifact-friendly copies (multi-file artifacts need full documents for extra pages)
print("ok", os.listdir(DIST))
