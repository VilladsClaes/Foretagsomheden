"""Genererer eventurs aktivitetsmærker som SVG.

Hvert mærke er en rund, broderet "patch" med ikon i midten og tekst langs kanten.
Skriver både et inline-fragment til src/partials/maerker/ og en selvstændig fil
til public/assets/img/maerker/. Kør: python tools/generer-maerker.py
"""
from pathlib import Path

ROD = Path(__file__).resolve().parent.parent
P = "#fbf7ee"  # pergament

IKONER = {
    "haengekoeje": f'''<g fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
<path d="M64 142V70M136 142V70"/><path d="M58 88L100 64l42 24"/><path d="M64 96q36 40 72 0"/>
<path d="M54 142h20M126 142h20" stroke-width="4"/></g>
<path d="M150 58a9 9 0 1 1-9-9a7 7 0 0 0 9 9z" fill="{P}"/>''',
    "natteloeb": f'''<circle cx="90" cy="92" r="28" fill="{P}"/><circle cx="103" cy="83" r="25" fill="var(--maerke-farve)"/>
<g fill="{P}"><path d="M134 62l3 8 8 3-8 3-3 8-3-8-8-3 8-3z"/><path d="M128 108l2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/><circle cx="114" cy="56" r="2.5"/></g>
<path d="M58 140q22-14 44-6t44-4" fill="none" stroke="{P}" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 9"/>''',
    "luftgevaer": f'''<g fill="none" stroke="{P}" stroke-linecap="round"><circle cx="100" cy="100" r="38" stroke-width="5"/><circle cx="100" cy="100" r="23" stroke-width="5"/>
<path d="M100 50v18M100 132v18M50 100h18M132 100h18" stroke-width="4"/></g><circle cx="100" cy="100" r="8" fill="{P}"/>''',
    "bow": f'''<g fill="none" stroke="{P}" stroke-linecap="round" stroke-linejoin="round"><path d="M62 58q84-6 80 84" stroke-width="6"/><path d="M62 58l80 84" stroke-width="2" opacity=".75"/>
<path d="M66 136l52-52" stroke-width="5"/><path d="M66 136l-12 2 2-12M66 136l-4-13M66 136l13 4" stroke-width="4"/></g><circle cx="124" cy="78" r="10" fill="{P}"/>''',
    "kaffe": f'''<g fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M58 98h68l-6 14q-28 8-56 0z"/><path d="M126 100l28-12"/>
<path d="M76 66q-5 6 0 12M92 60q-5 7 0 14M108 66q-5 6 0 12" stroke-width="3.5"/></g>
<g fill="{P}"><ellipse cx="78" cy="90" rx="8" ry="5.5" transform="rotate(-18 78 90)"/><ellipse cx="96" cy="88" rx="8" ry="5.5" transform="rotate(12 96 88)"/><ellipse cx="112" cy="91" rx="8" ry="5.5" transform="rotate(-8 112 91)"/>
<path d="M78 146c-9-9-1-17 2-26c7 9 10 17 3 26z"/><path d="M96 148c-11-11-1-22 3-32c8 11 12 21 4 32z"/><path d="M114 146c-8-8-1-15 2-23c6 8 9 15 3 23z"/></g>''',
    "natur": f'''<g fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M100 52c34 18 34 64 0 86c-34-22-34-68 0-86z"/><path d="M100 62v88"/>
<path d="M100 86l14-10M100 86l-14-10M100 106l18-12M100 106l-18-12M100 124l12-9M100 124l-12-9" stroke-width="3.5"/></g>''',
    "oekse": f'''<g fill="none" stroke="{P}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M62 118v20q38 14 76 0v-20"/><ellipse cx="100" cy="118" rx="38" ry="11"/>
<ellipse cx="100" cy="118" rx="16" ry="4" stroke-width="3"/><path d="M96 106L66 56" stroke-width="6"/></g>
<path d="M80 104l26-17 12 22q-12 10-28 9z" fill="{P}"/><g fill="{P}"><rect x="134" y="80" width="10" height="5" rx="1" transform="rotate(-30 139 82)"/><rect x="142" y="98" width="8" height="4" rx="1" transform="rotate(20 146 100)"/><rect x="124" y="66" width="7" height="4" rx="1" transform="rotate(50 127 68)"/></g>''',
}

MAERKER = [
    ("haengekoeje", "#2a4634", "#1d3125", "TELTHÆNGEKØJE", "SOV I TRÆERNE"),
    ("natteloeb", "#22395a", "#0f171d", "NATTELØB", "FIND VEJ I MØRKET"),
    ("luftgevaer", "#77894a", "#4f5d2c", "LUFTGEVÆR", "RO PÅ HÅNDEN"),
    ("bow", "#e0602a", "#a83e14", "BOW COMBAT", "SKUMPIL &amp; MOD"),
    ("kaffe", "#7a4a2c", "#4a2a16", "KAFFERISTNING", "OVER ÅBEN ILD"),
    ("natur", "#3d5e47", "#22392a", "NATURVANDRING", "MED ANEMETTE"),
    ("oekse", "#a8742a", "#6f4a14", "ØKSEHUGNING", "MED DANIEL"),
]


def svg(key, farve, ring, top, bund, standalone):
    ns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ''
    titel = f"{top.title()} – {bund.lower()}".replace("&Amp;", "&amp;")
    font = 'font-family="Instrument Sans, Arial, sans-serif" font-weight="700"'
    return f'''<svg{ns} class="maerke" viewBox="0 0 200 200" role="img" aria-label="Mærke: {titel}" style="--maerke-farve:{farve}">
<defs><path id="mt-{key}" d="M21 100a79 79 0 0 1 158 0"/><path id="mb-{key}" d="M10 100a90 90 0 0 0 180 0"/></defs>
<circle cx="100" cy="100" r="99" fill="{ring}"/>
<circle cx="100" cy="100" r="94" fill="none" stroke="{P}" stroke-width="1.6" stroke-dasharray="4 4" opacity=".55"/>
<circle cx="100" cy="100" r="71" fill="{farve}"/>
<circle cx="100" cy="100" r="74.5" fill="none" stroke="{P}" stroke-width="1.6" stroke-dasharray="4 4" opacity=".55"/>
<text fill="{P}" {font} font-size="15" letter-spacing="2.2" text-anchor="middle"><textPath href="#mt-{key}" startOffset="50%">{top}</textPath></text>
<text fill="{P}" {font} font-size="11.5" letter-spacing="2" text-anchor="middle" opacity=".85"><textPath href="#mb-{key}" startOffset="50%">{bund}</textPath></text>
<circle cx="19" cy="100" r="2.5" fill="{P}"/><circle cx="181" cy="100" r="2.5" fill="{P}"/>
{IKONER[key].replace("var(--maerke-farve)", farve)}
</svg>
'''


for key, farve, ring, top, bund in MAERKER:
    (ROD / "src/partials/maerker" / f"{key}.html").write_text(svg(key, farve, ring, top, bund, False), encoding="utf-8", newline="\n")
    (ROD / "public/assets/img/maerker" / f"{key}.svg").write_text(svg(key, farve, ring, top, bund, True), encoding="utf-8", newline="\n")
print("Skrev", len(MAERKER), "mærker")
