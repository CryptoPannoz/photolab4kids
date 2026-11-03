"""Estrae dal PDF del laboratorio (impaginato in Canva) le immagini del sito e le salva in docs/assets/img come WebP.

Uso:  python3 -I tools/prepara-immagini.py ../PHOTOLAB4KIDS.pdf
Serve: pip install pymupdf pillow numpy

Finiscono nel sito SOLO le immagini in ELENCO. Le fotografie in cui gli alunni sono riconoscibili (ritratti delle
pagine 34-44 del PDF) restano fuori finché non ci sono le liberatorie delle famiglie per la pubblicazione sul web:
il repo è pubblico, quindi non vanno nemmeno committate.
"""
import sys
from pathlib import Path

import fitz
import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "docs" / "assets" / "img"

# nome → (pagina, xref, opzioni)
#   pezzi: nomi dei pezzi in ordine di lettura, quando l'immagine contiene foto e disegno separati da trasparenza
#   gap: fascia vuota minima (px) fra due pezzi (default 12)
#   ritagli: {nome: (x0, y0, x1, y1)} in frazioni dell'immagine già rifilata, quando i pezzi si toccano
#   lato: lato lungo massimo in px (default 1400)
ELENCO = {
    # copertina e «Immaginare ciò che non si vede»
    "serpente": (1, 388, {"lato": 1800}),
    "rana": (3, 399, {}),
    "fiori-meta": (4, 404, {}),
    # «Una fotografia tagliata a metà»: metà foto, metà disegno
    "meta-uomo-1": (5, 410, {}),
    "meta-uomo-2": (9, 429, {}),
    "meta-volto": (8, 425, {"ritagli": {"meta-volto": (0, .09, 1, 1)}}),  # via il nome scritto in alto
    "meta-fiori-1": (10, 433, {}),
    "meta-fiori-2": (11, 437, {"ritagli": {"meta-fiori-2": (0, .13, 1, 1)}}),  # via il nome scritto in alto
    # «La fantasia completa ciò che la fotografia non mostra»
    "gonna-1": (6, 415, {}),
    "gonna-2": (6, 416, {}),
    "gonna-3": (7, 421, {}),
    # «Io la vedo così!»: dalla fotografia al disegno
    "ricalco": (13, 446, {}),
    "mano": (12, 441, {"ritagli": {"mano-foto": (0, 0, .476, 1), "mano-disegno": (.481, 0, 1, 1)}}),
    "foglie": (14, 451, {"pezzi": ["foglie-disegno", "foglie-foto"]}),
    "tartaruga": (15, 456, {"ritagli": {"tartaruga-foto": (.106, .153, .465, .891),
                                         "tartaruga-disegno": (.510, .147, .878, .891)}}),
    "uomo": (16, 461, {"ritagli": {"uomo-foto": (0, 0, .492, 1), "uomo-disegno": (.506, 0, 1, 1)}}),
    "sentiero-a": (17, 466, {"ritagli": {"sentiero-disegno-a": (.112, .139, .858, .497)}}),
    "sentiero": (21, 486, {"pezzi": ["sentiero-disegno-b", "sentiero-foto"]}),
    "barca-disegno": (19, 476, {}),
    "barca-foto": (19, 477, {}),
    "albero-foto": (20, 481, {}),
    "albero-disegno": (20, 482, {}),
    "ragazza": (22, 491, {"pezzi": ["ragazza-foto", "ragazza-disegno"], "gap": 2}),
    # «Collage visivo»
    "collage-01": (23, 495, {"lato": 1600}),
    "collage-02": (24, 500, {}),
    "collage-03": (25, 505, {}),
    "collage-04": (26, 510, {}),
    "collage-05": (27, 515, {}),
    "collage-06": (27, 516, {}),
    "collage-07": (28, 520, {}),
    "collage-08": (28, 521, {}),
    "collage-09": (29, 525, {}),
    "collage-10": (29, 526, {}),
    # «Io sono, noi siamo»: autoritratti disegnati
    "autoritratto-01": (32, 554, {"lato": 900}),
    "autoritratto-02": (30, 532, {"lato": 900}),
    "autoritratto-03": (30, 533, {"lato": 900}),
    "autoritratto-04": (30, 534, {"lato": 900}),
    "autoritratto-05": (30, 535, {"lato": 900}),
    "autoritratto-06": (30, 536, {"lato": 900}),
    "autoritratto-07": (30, 537, {"lato": 900}),
    "autoritratto-08": (30, 538, {"lato": 900}),
    "autoritratto-09": (30, 539, {"lato": 900}),
    "autoritratto-10": (32, 552, {"lato": 900}),
    # «Dentro di me c'è…»: solo le scritte a gesso, senza volti
    "gesso-titolo": (33, 559, {}),
    "gesso-parole": (35, 602, {}),
    # «Ogni sogno merita spazio»: solo scritte e disegni, senza volti
    "sogno-esplorare": (39, 621, {}),
    "sogno-aiutare": (41, 666, {}),
    "sogno-stelle": (41, 667, {}),
}


# Foto del libro stampato (WhatsApp del 03/11/2026), nella cartella del PDF: nome → (file, riquadro in px)
FOTO_LIBRO = {
    "libro": ("WhatsApp Image 2026-11-03 at 18.43.41 (3).jpeg", (40, 520, 1290, 1720)),
    "libro-aperto": ("WhatsApp Image 2026-11-03 at 18.43.41 (2).jpeg", (0, 780, 1500, 1720)),
}


def carica(doc, xref):
    """Pixmap dell'immagine con la sua maschera di trasparenza, come immagine PIL."""
    smask = doc.extract_image(xref).get("smask", 0)
    pix = fitz.Pixmap(doc, xref)
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    if smask:
        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask))
    mode = "RGBA" if pix.alpha else "RGB"
    return Image.frombytes(mode, (pix.width, pix.height), pix.samples)


def raddrizza(img, page, xref):
    """Canva salva alcune immagini ruotate di 90° e le raddrizza con la matrice di posizionamento."""
    a, b = next(i["transform"] for i in page.get_image_info(xrefs=True) if i["xref"] == xref)[:2]
    if abs(b) > abs(a):
        return img.transpose(Image.Transpose.ROTATE_90 if b < 0 else Image.Transpose.ROTATE_270)
    return img


def tratti(occupato, gap=12):
    """Intervalli [inizio, fine) di valori True separati da almeno `gap` False."""
    idx = np.flatnonzero(occupato)
    if not len(idx):
        return []
    tagli = np.flatnonzero(np.diff(idx) > gap)
    inizi = np.r_[idx[0], idx[tagli + 1]]
    fini = np.r_[idx[tagli], idx[-1]] + 1
    return list(zip(inizi, fini))


def pezzi(mask, gap, x0=0, y0=0):
    """Taglio XY ricorsivo sulla trasparenza: riquadri dei pezzi separati da fasce vuote, in ordine di lettura."""
    righe = tratti(mask.any(1), gap)
    if len(righe) > 1:
        return [p for r0, r1 in righe for p in pezzi(mask[r0:r1], gap, x0, y0 + r0)]
    colonne = tratti(mask.any(0), gap)
    if len(colonne) > 1:
        return [p for c0, c1 in colonne for p in pezzi(mask[:, c0:c1], gap, x0 + c0, y0)]
    r0, r1 = righe[0]
    c0, c1 = colonne[0]
    return [(x0 + c0, y0 + r0, x0 + c1, y0 + r1)]


def salva(img, nome, lato):
    if img.mode == "RGBA" and img.getchannel("A").getextrema()[0] == 255:
        img = img.convert("RGB")
    img.thumbnail((lato, lato), Image.LANCZOS)
    dest = OUT / f"{nome}.webp"
    img.save(dest, "WEBP", quality=80, method=6)
    print(f"{dest.name:28} {img.width}×{img.height}  {dest.stat().st_size // 1024} KB")


def main(pdf):
    doc = fitz.open(pdf)
    OUT.mkdir(parents=True, exist_ok=True)
    for nome, (pagina, xref, opz) in ELENCO.items():
        page = doc[pagina - 1]
        img = raddrizza(carica(doc, xref), page, xref)
        lato = opz.get("lato", 1400)
        if img.mode == "RGBA":
            img = img.crop(img.getchannel("A").point(lambda v: 255 if v > 16 else 0).getbbox())
        if "ritagli" in opz:
            w, h = img.size
            for n, (fx0, fy0, fx1, fy1) in opz["ritagli"].items():
                salva(img.crop((round(fx0 * w), round(fy0 * h), round(fx1 * w), round(fy1 * h))), n, lato)
            continue
        if img.mode != "RGBA":
            salva(img, nome, lato)
            continue
        mask = np.asarray(img.getchannel("A")) > 16
        riquadri = pezzi(mask, opz.get("gap", 12))
        grande = max((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in riquadri)
        riquadri = [r for r in riquadri if (r[2] - r[0]) * (r[3] - r[1]) > grande * 0.02]
        nomi = opz.get("pezzi")
        if nomi:
            if len(riquadri) != len(nomi):
                sys.exit(f"{nome}: attesi {len(nomi)} pezzi, trovati {len(riquadri)}")
            for n, r in zip(nomi, riquadri):
                salva(img.crop(r), n, lato)
        else:
            x0, y0, x1, y1 = zip(*riquadri)
            salva(img.crop((min(x0), min(y0), max(x1), max(y1))), nome, lato)
    for nome, (file, riquadro) in FOTO_LIBRO.items():
        salva(Image.open(Path(pdf).parent / file).crop(riquadro), nome, 1400)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "../PHOTOLAB4KIDS.pdf")
