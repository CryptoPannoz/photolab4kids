# Photolab for Kids

Sito del laboratorio di fotografia e creatività ideato da Vittoria Lorenzetti per la scuola primaria e
secondaria di primo grado. Sito statico in `docs/`: HTML, CSS e JS senza dipendenze, font self-hosted
(Bricolage Grotesque e Newsreader), nessuna chiamata a terze parti, nessun cookie.

**Stato**: scheletro del 03/11/2026, con `noindex` e `robots.txt` che blocca i motori di ricerca. Al passaggio
sul dominio definitivo vanno tolti entrambi. I punti da completare sono evidenziati in giallo nella pagina
(classe `da-completare`) e nei riquadri tratteggiati (classe `segnaposto`).

## Il concept: «L'altra metà»

L'esercizio simbolo del laboratorio è una fotografia tagliata a metà che i bambini completano con la fantasia.
Il sito ne fa il suo linguaggio:

- **Copertina**: come il libro stampato, con il serpente metà fotografia e metà disegno.
- **Guarda**: il sito conta i secondi passati davanti a una fotografia, poi chiede se si è vista la persona
  nella radura e mostra come l'hanno disegnata due bambini. È l'obiettivo del laboratorio (soffermarsi,
  leggere le immagini) fatto provare a chi legge.
- **La metà che manca**: un foglio bianco copre la metà disegnata; il cursore a forbice lo toglie.
- **I capitoli delle opere** hanno i colori delle sezioni del libro: salvia (la metà che manca), carta (io la
  vedo così), rosa (collage), confetto (autoritratti), lavagna (dentro di me c'è), bianco con stelle d'oro
  (ogni sogno merita spazio).
- **Formati**: tre rullini (36, 24, 12 pose) per i percorsi di 6 mesi, 3 mesi e un weekend.

Testi: dal PDF del libro (`../PHOTOLAB4KIDS.pdf`, Canva, agosto 2026) e dal racconto di Vittoria.

## Immagini

Estratte dal PDF con `tools/prepara-immagini.py` (PyMuPDF + Pillow + numpy) e salvate in WebP in
`docs/assets/img/`. Lo script raddrizza le immagini che Canva salva ruotate, separa foto e disegno quando stanno
nello stesso file e taglia i nomi dei bambini scritti sui fogli.

```bash
python3 -I tools/prepara-immagini.py ../PHOTOLAB4KIDS.pdf
```

**Ritratti degli alunni**: le fotografie in cui i bambini sono riconoscibili (set su sfondo nero e bianco,
pagine 34-44 del PDF) **non sono nel repo** e non vanno committate finché non ci sono le liberatorie delle
famiglie per la pubblicazione online. Il repo è pubblico.

## Lavorarci

Anteprima locale: configurazione `photolab4kids` in `../.claude/launch.json`, oppure

```bash
node tools/serve.mjs
```

e poi http://127.0.0.1:4321.
