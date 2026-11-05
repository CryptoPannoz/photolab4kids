"""Disegna marchio, logo, icona per telefoni, immagine di condivisione (OG) e il libro del laboratorio con i font e i
colori del sito.

Uso:  python3 -I tools/prepara-grafica.py
Serve: pip install pillow fonttools brotli

Il marchio è lo stesso di docs/assets/img/favicon.svg (metà verde, metà disegno, linea di taglio tratteggiata),
ridisegnato qui per non dipendere da un convertitore SVG. Il libro (chiuso e aperto) ha preso il posto delle foto del
quaderno a spirale il 05/11/2026, su richiesta di Vittoria: copertina in carta con il dorso in tela verde, come la metà
verde del marchio.
"""
import io
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

RADICE = Path(__file__).resolve().parent.parent
FONT = RADICE / "docs" / "assets" / "fonts"
IMG = RADICE / "docs" / "assets" / "img"
LOGO = RADICE / "docs" / "assets" / "logo"

CARTA = (245, 242, 232)
CARTA_CHIARA = (251, 250, 246)
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
    """«PhotoLab» in grottesco nero e «4Kids» in corsivo, attaccati come nel dominio; restituisce la larghezza."""
    g, s = grotesk(corpo), serif_corsivo(round(corpo * 0.86))
    d.text((x, y), "PhotoLab", font=g, fill=colore, anchor="ls")
    lg = d.textlength("PhotoLab", font=g) + corpo * 0.04
    d.text((x + lg, y), "4Kids", font=s, fill=colore, anchor="ls")
    return lg + d.textlength("4Kids", font=s)


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


def grana(img, forza=6, stira=(1, 1)):
    """Grana della carta (o trama della tela, con `stira`): rumore sommato al colore, centrato sullo zero."""
    w, h = img.size
    rumore = Image.effect_noise((max(1, w // stira[0]), max(1, h // stira[1])), forza).resize((w, h), Image.BILINEAR)
    return ImageChops.add(img.convert("RGB"), Image.merge("RGB", [rumore] * 3), 1.0, -128)


def tela_verde(w, h):
    """Tela da legatoria: due trame incrociate, fili lunghi in verticale e in orizzontale."""
    t = Image.new("RGB", (w, h), VERDE)
    t = grana(t, 9, (1, 6))
    return grana(t, 7, (6, 1))


def luce(img, scuro=0.9):
    """Luce dall'alto a sinistra: il colore resta pieno in alto a sinistra e scurisce fino a `scuro` in basso a destra."""
    w, h = img.size
    v = Image.linear_gradient("L").resize((w, h))
    diagonale = ImageChops.add(v, v.transpose(Image.Transpose.ROTATE_90).resize((w, h)), 2.0)
    lum = diagonale.point(lambda p: round(255 - p * (1 - scuro)))
    return ImageChops.multiply(img.convert("RGB"), Image.merge("RGB", [lum] * 3))


def copertina(lato=1000):
    """La copertina piatta: carta con dorso in tela verde, il titolo con i font del sito e il serpente."""
    img = grana(Image.new("RGB", (lato, lato), CARTA), 5)
    dorso = 104
    img.paste(tela_verde(dorso, lato), (0, 0))
    d = ImageDraw.Draw(img)
    # la cerniera del cartone (incavo e bordo in luce) e l'ombra della tela sulla carta
    d.line([(36, 0), (36, lato)], fill=(8, 84, 52), width=5)
    d.line([(41, 0), (41, lato)], fill=(52, 156, 108), width=2)
    for i in range(10):
        d.line([(dorso + i, 0), (dorso + i, lato)], fill=tuple(round(c * (0.86 + 0.014 * i)) for c in CARTA))

    x = 168
    m = marchio(58)
    img.paste(m, (x, 92), m)
    scritta(d, x + 78, 139, 40)
    # il titolo occupa la larghezza utile: il corpo si ricava dalla riga più lunga
    utile = lato - x - 84
    corpo = 120
    while d.textlength("Laboratorio di", font=grotesk(corpo)) > utile:
        corpo -= 2
    g, s = grotesk(corpo), serif_corsivo(round(corpo * 1.08))
    y = 368
    for riga, f, colore in (("Laboratorio di", g, INCHIOSTRO), ("fotografia", g, INCHIOSTRO),
                            ("e creatività", s, VERDE), ("per bambini", s, VERDE)):
        d.text((x - (0 if f is g else -4), y), riga, font=f, fill=colore, anchor="ls")
        y += round(corpo * (0.98 if f is g else 1.02))

    serpente = Image.open(IMG / "serpente.webp").convert("RGBA")
    serpente = serpente.resize((690, round(690 * serpente.height / serpente.width)), Image.LANCZOS)
    serpente = serpente.rotate(3, expand=True, resample=Image.BICUBIC)
    img.paste(serpente, (lato - serpente.width - 70, lato - serpente.height - 34), serpente)
    return luce(img, 0.9)


def ombra_e_ruota(oggetto, sagoma, angolo, spostamento=(22, 34), sfocatura=28, intensita=170):
    """Mette l'oggetto (RGBA) su fondo trasparente con l'ombra morbida della sua sagoma, poi lo ruota."""
    margine = 110
    tela = Image.new("RGBA", (oggetto.width + 2 * margine, oggetto.height + 2 * margine), (0, 0, 0, 0))
    ombra = Image.new("L", tela.size, 0)
    ombra.paste(sagoma.point(lambda a: a * intensita // 255), (margine + spostamento[0], margine + spostamento[1]))
    ombra = ombra.filter(ImageFilter.GaussianBlur(sfocatura))
    tela = Image.composite(Image.new("RGBA", tela.size, (10, 6, 3, 255)), tela, ombra)
    tela.alpha_composite(oggetto, (margine, margine))
    tela = tela.rotate(angolo, expand=True, resample=Image.BICUBIC)
    return tela.crop(tela.getbbox())


def libro_chiuso():
    """Il libro rilegato visto dall'alto, un po' di sbieco: si vedono il taglio delle pagine e lo spessore dei piatti."""
    cop = copertina()
    W, H = cop.size
    dx, dy = 12, 18
    libro = Image.new("RGBA", (W + dx, H + dy), (0, 0, 0, 0))
    d = ImageDraw.Draw(libro)
    passi = 48
    # dal piatto di dietro verso quello davanti: cartone, pagine (righe alterne), cartone
    for i in range(passi, -1, -1):
        f = i / passi
        x, y = round(f * dx), round(f * dy)
        if f < 0.2 or f > 0.84:
            fianco, sotto, rientro = (176, 168, 150), (198, 190, 172), 0
        else:
            chiaro = i % 2 == 0
            fianco = (214, 207, 190) if chiaro else (190, 182, 164)
            sotto = (232, 226, 211) if chiaro else (208, 200, 183)
            rientro = 5
        d.line([(x + W - 1, y + rientro), (x + W - 1, y + H - 1 - rientro)], fill=fianco, width=2)
        d.line([(x + 30, y + H - 1), (x + W - 1 - rientro, y + H - 1)], fill=sotto, width=2)
        d.line([(x, y + H - 1), (x + 30, y + H - 1)], fill=(9, 78, 48), width=2)  # il dorso in tela
    maschera = Image.new("L", cop.size, 0)
    ImageDraw.Draw(maschera).rounded_rectangle([0, 0, W - 1, H - 1], radius=7, fill=255)
    libro.paste(cop, (0, 0), maschera)
    return ombra_e_ruota(libro, libro.getchannel("A"), -4)


def libro_aperto():
    """Il libro aperto sulla pagina della metà che manca: ombra nella cucitura, pagine che si sollevano."""
    P, bordo = 640, 16
    pagine = grana(Image.new("RGB", (2 * P, P), CARTA_CHIARA), 4)
    d = ImageDraw.Draw(pagine)
    g, s = grotesk(50), serif_corsivo(54)
    for k, (riga, f, colore) in enumerate((("Una fotografia", g, VERDE), ("tagliata a metà.", g, VERDE),
                                           ("E l'altra metà?", s, INCHIOSTRO), ("Esiste?", s, INCHIOSTRO))):
        d.text((96, 250 + k * 56 + (14 if f is s else 0)), riga, font=f, fill=colore, anchor="ls")
    opera = Image.open(IMG / "meta-fiori-1.webp").convert("RGB")
    alta = P - 150
    opera = opera.resize((round(opera.width * alta / opera.height), alta), Image.LANCZOS)
    pagine.paste(opera, (P + (P - opera.width) // 2 + 14, 75))
    # la carta curva: buio stretto nella cucitura, una spalla di luce, i bordi esterni un po' più scuri
    profilo = []
    for x in range(2 * P):
        t = abs(x + 0.5 - P) / P
        v = 1 - 0.42 * 2.718 ** (-t / 0.03) - 0.08 * 2.718 ** (-t / 0.16) + 0.03 * 2.718 ** (-((t - 0.2) / 0.08) ** 2)
        v -= 0.06 * 2.718 ** (-(1 - t) / 0.025)
        profilo.append(max(0, min(255, round(v * 255))))
    riga = Image.new("L", (2 * P, 1))
    riga.putdata(profilo)
    pagine = ImageChops.multiply(pagine, Image.merge("RGB", [riga.resize((2 * P, P))] * 3))

    W, H = 2 * P + 2 * bordo, P + 2 * bordo
    libro = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    piatti = Image.new("L", (W, H), 0)
    ImageDraw.Draw(piatti).rounded_rectangle([0, 0, W - 1, H - 1], radius=8, fill=255)
    fondo = grana(Image.new("RGB", (W, H), (226, 218, 200)), 5)
    fondo.paste(tela_verde(220, H), (W // 2 - 110, 0))  # i risvolti della tela del dorso
    libro.paste(fondo, (0, 0), piatti)
    d = ImageDraw.Draw(libro)
    # i tagli delle pagine sui lati esterni
    for i in range(9):
        colore = (236, 231, 218, 255) if i % 2 else (200, 192, 175, 255)
        d.line([(bordo - 9 + i, bordo - 2), (bordo - 9 + i, H - bordo + 1)], fill=colore)
        d.line([(W - bordo + 8 - i, bordo - 2), (W - bordo + 8 - i, H - bordo + 1)], fill=colore)
    libro.paste(pagine, (bordo, bordo))
    return ombra_e_ruota(libro, piatti, 2.5, (18, 28), 24, 160)


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
    og().save(IMG / "og-photolab4kids.jpg", quality=88, optimize=True)
    chiuso = libro_chiuso()
    chiuso.resize((1100, round(1100 * chiuso.height / chiuso.width)), Image.LANCZOS).save(IMG / "libro-copertina.webp", quality=86, method=6)
    aperto = libro_aperto()
    aperto.resize((1400, round(1400 * aperto.height / aperto.width)), Image.LANCZOS).save(IMG / "libro-pagine.webp", quality=86, method=6)
    for f in sorted(LOGO.iterdir()) + [IMG / f for f in ("apple-touch-icon.png", "og-photolab4kids.jpg", "libro-copertina.webp", "libro-pagine.webp")]:
        print(f.relative_to(RADICE), Image.open(f).size, f.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
