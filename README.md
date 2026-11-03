# Photolab for Kids

Sito del laboratorio di fotografia e creatività ideato da Vittoria Lorenzetti per la scuola primaria e
secondaria di primo grado. Sito statico in `docs/`: HTML, CSS e JS senza dipendenze, font self-hosted
(Bricolage Grotesque e Newsreader), nessuna chiamata a terze parti, nessun cookie.

**Online** su https://photolab4kids.it (GitHub Pages da `docs/`, dominio registrato su Aruba il 03/11/2026,
intestato ad Alberto Broggi). I punti ancora da completare (classe `da-completare`) sono nascosti sul sito pubblico
e compaiono in giallo nell'anteprima locale o aggiungendo `?bozza` all'indirizzo.

## Il concept: «L'altra metà»

L'esercizio simbolo del laboratorio è una fotografia tagliata a metà che i bambini completano con la fantasia.
Il sito ne fa il suo linguaggio:

- **Copertina**: come il libro stampato, con il serpente metà fotografia e metà disegno. All'apertura il serpente si
  ricompone a strisce (il disegno arriva da sinistra, la foto da destra) e poi ondeggia; senza JS o con «riduci
  movimento» resta l'immagine ferma.
- **Guarda**: due nastri di fotografie dei reportage di Vittoria scorrono come un feed; poi il sito chiede di
  fermarsi su una sola foto e, dopo qualche secondo, domanda se si è vista la persona nella radura e mostra come
  l'hanno disegnata due bambini. È l'obiettivo del laboratorio (soffermarsi, leggere le immagini) fatto provare.
- **La metà che manca**: un foglio bianco copre la metà disegnata; la forbice sulla foto si trascina (o si
  scorre col dito) verso destra e taglia via il foglio. Uno swipe finisce da solo, un tocco apre e richiude.
- **I capitoli delle opere** hanno i colori delle sezioni del libro: salvia (la metà che manca), carta (io la
  vedo così), rosa (collage), confetto (autoritratti), lavagna (dentro di me c'è), bianco con stelle d'oro
  (ogni sogno merita spazio).
- **Ritratti**: i set su sfondo nero e bianco sono due provini su pellicola, con il numero di ogni fotogramma.
- **Formati**: tre rullini (36, 24, 12 pose) per i percorsi di 6 mesi, 3 mesi e un weekend.

Testi: dal PDF del libro (`../PHOTOLAB4KIDS.pdf`, Canva, agosto 2026) e dal racconto di Vittoria. Foto, biografia e
contatti di Vittoria dal suo sito (vittorialorenzetti.com/about), come le 22 foto del flusso (`flusso-NN.webp`);
logo dal sito della Fondazione Comoli Ferrari.

## Immagini

Estratte dal PDF con `tools/prepara-immagini.py` (PyMuPDF + Pillow + numpy) e salvate in WebP in
`docs/assets/img/`. Lo script raddrizza le immagini che Canva salva ruotate, separa foto e disegno quando stanno
nello stesso file e taglia i nomi dei bambini scritti sui fogli.

```bash
python3 -I tools/prepara-immagini.py ../PHOTOLAB4KIDS.pdf
```

**Ritratti degli alunni**: pubblicati dal 03/11/2026, dopo la conferma di Vittoria che ci sono le liberatorie delle
famiglie e il contratto con la scuola. I nomi scritti sui disegni restano comunque tagliati.

## Logo e immagine di condivisione

`tools/prepara-grafica.py` disegna con i font e i colori del sito il marchio (`docs/assets/logo/
photolab4kids-marchio.png`, 1024 px), il logo orizzontale (scuro, chiaro e su carta), l'icona per i telefoni
(`apple-touch-icon.png`) e l'immagine di condivisione `og.jpg` (1200×630).

```bash
python3 -I tools/prepara-grafica.py
```

Per Vittoria, che gestisce il sito: [GUIDA-VITTORIA.md](GUIDA-VITTORIA.md).

## Lavorarci

Anteprima locale: configurazione `photolab4kids` in `../.claude/launch.json`, oppure

```bash
node tools/serve.mjs
```

e poi http://127.0.0.1:4321.
