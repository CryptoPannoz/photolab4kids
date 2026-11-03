"""Disegna marchio, logo, icona per telefoni e immagine di condivisione (OG) con i font e i colori del sito.

Uso:  python3 -I tools/prepara-grafica.py
Serve: pip install pillow fonttools brotli

Il marchio è lo stesso di docs/assets/img/favicon.svg (metà verde, metà disegno, linea di taglio tratteggiata),
ridisegnato qui per non dipendere da un convertitore SVG.
"""
import io
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

RADICE = Path(__file__).resolve().parent.parent
FONT = RADICE / "docs" / "assets" / "fonts"
IMG = RADICE / "docs" / "assets" / "img"
LOGO = RADICE / "docs" / "assets" / "logo"

CARTA = (245, 242, 232)
VERDE = (14, 121, 74)
INCHIOSTRO = (27, 29, 31)
TENUE = (85, 83, 77)


def font(nome, corpo, assi):
    """Font variabile dal woff2 del sito, con gli assi nell'ordine di fvar."""
    ttf = TTFont(FONT / f"{nome}.woff2")
    ttf.flavor = None
    dati = io.BytesIO()
    ttf.save(dati)
    dati.seek(0)
    f = ImageFont.truetype(dati, corpo)
    f.set_variation_by_axes(assi)
    return f


def grotesk(corpo, peso=800):
    return font("bricolage-grotesque", corpo, [96, peso, 100])  # opsz, wght, wdth


def serif_corsivo(corpo, peso=400):
    return font("newsreader-italic", corpo, [peso, 72])  # wght, opsz


def bezier(p0, p1, p2, p3, passi=400):
    return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
                  for a, b, c, d in zip(p0, p1, p2, p3))
            for t in (i / passi for i in range(passi + 1))]


def marchio(lato):
    """Il marchio quadrato, angoli trasparenti. Disegnato a 4x e ridotto per avere bordi morbidi."""
    k = lato * 4 / 64
    img = Image.new("RGBA", (lato * 4, lato * 4), (0, 0, 0, 0))
    maschera = Image.new("L", img.size, 0)
    ImageDraw.Draw(maschera).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=14 * k, fill=255)
    fondo = Image.new("RGBA", img.size, CARTA + (255,))
    ImageDraw.Draw(fondo).rectangle([0, 0, 32 * k, img.height], fill=VERDE + (255,))
    img.paste(fondo, (0, 0), maschera)
    d = ImageDraw.Draw(img)
    # linea di taglio: x=32, trattini da 4 ogni 8, da y=6 a y=58
    for y in range(6, 58, 8):
        d.rectangle([31 * k, y * k, 33 * k, (y + 4) * k], fill=INCHIOSTRO)
    # il segno disegnato: «M38 18 c6 2 12 6 13 12 s-5 9 -11 11 -6 7 -1 9» con le curve risolte
    curve = [((38, 18), (44, 20), (50, 24), (51, 30)),
             ((51, 30), (52, 36), (46, 39), (40, 41)),
             ((40, 41), (34, 43), (34, 48), (39, 50))]
    # tracciato «a pennello»: tanti cerchi vicini, così il tratto resta pieno anche nelle curve strette
    r = 1.5 * k
    for c in curve:
        for x, y in bezier(*c):
            d.ellipse([x * k - r, y * k - r, x * k + r, y * k + r], fill=INCHIOSTRO)
    return img.resize((lato, lato), Image.LANCZOS)


def scritta(d, x, y, corpo, colore=INCHIOSTRO):
    """«Photolab» in grottesco nero e «for Kids» in corsivo; restituisce la larghezza totale."""
    g, s = grotesk(corpo), serif_corsivo(round(corpo * 0.78))
    d.text((x, y), "Photolab", font=g, fill=colore, anchor="ls")
    lg = d.textlength("Photolab", font=g)
    d.text((x + lg + corpo * 0.18, y), "for Kids", font=s, fill=colore, anchor="ls")
    return lg + corpo * 0.18 + d.textlength("for Kids", font=s)


def logo_orizzontale(colore, sfondo=None):
    corpo = 220
    tela = Image.new("RGBA", (2200, 420), sfondo + (255,) if sfondo else (0, 0, 0, 0))
    m = marchio(300)
    tela.paste(m, (60, 60), m)
    larghezza = scritta(ImageDraw.Draw(tela), 420, 290, corpo, colore)
    return tela.crop((0, 0, round(420 + larghezza + 70), 420))


def og():
    tela = Image.new("RGB", (1200, 630), CARTA)
    d = ImageDraw.Draw(tela)
    m = marchio(84)
    tela.paste(m, (72, 64), m)
    d.text((176, 118), "PHOTOLAB4KIDS.IT", font=font("bricolage-grotesque", 22, [12, 600, 75]), fill=TENUE, anchor="ls")
    scritta(d, 68, 300, 150)
    d.text((72, 372), "Laboratorio di fotografia e creatività", font=serif_corsivo(40), fill=INCHIOSTRO, anchor="ls")
    d.text((72, 420), "per le scuole primarie e secondarie", font=serif_corsivo(40), fill=INCHIOSTRO, anchor="ls")
    d.text((72, 520), "Impariamo a guardare.", font=grotesk(34, 700), fill=VERDE, anchor="ls")
    # il serpente metà foto e metà disegno attraversa l'immagine in basso a destra, testa compresa
    serpente = Image.open(IMG / "serpente.webp").convert("RGBA")
    serpente = serpente.resize((760, round(760 * serpente.height / serpente.width)), Image.LANCZOS).rotate(4, expand=True, resample=Image.BICUBIC)
    tela.paste(serpente, (420, 440), serpente)
    return tela


def main():
    LOGO.mkdir(parents=True, exist_ok=True)
    marchio(1024).save(LOGO / "photolab4kids-marchio.png")
    logo_orizzontale(INCHIOSTRO).save(LOGO / "photolab4kids-logo.png")
    logo_orizzontale(CARTA).save(LOGO / "photolab4kids-logo-chiaro.png")
    logo_orizzontale(INCHIOSTRO, CARTA).convert("RGB").save(LOGO / "photolab4kids-logo-su-carta.png")
    icona = Image.new("RGB", (180, 180), CARTA)
    m = marchio(180)
    icona.paste(m, (0, 0), m)
    icona.save(IMG / "apple-touch-icon.png")
    og().save(IMG / "og.jpg", quality=88, optimize=True)
    for f in sorted(LOGO.iterdir()) + [IMG / "apple-touch-icon.png", IMG / "og.jpg"]:
        print(f.relative_to(RADICE), Image.open(f).size, f.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
