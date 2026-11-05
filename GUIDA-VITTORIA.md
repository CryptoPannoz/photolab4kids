# PhotoLab4Kids — guida per Vittoria

Il sito è tuo: questa guida spiega dove sta, come entrarci e come cambiarlo da sola.

## Dove sta il sito

- **Indirizzo**: https://photolab4kids.it
- **Codice**: https://github.com/CryptoPannoz/photolab4kids. La cartella `docs/` è il sito; il resto sono
  strumenti e note.
- **Hosting**: GitHub Pages, gratis. Ogni modifica salvata su GitHub va online da sola in 1-2 minuti.
- **Dominio**: photolab4kids.it, registrato su Aruba il 03/11/2026 a nome di Alberto, con rinnovo automatico
  ogni 3 novembre (11,99 € + IVA l'anno).
- **Donazioni**: la pagina https://photolab4kids.it/sostieni/ porta al tuo PayPal.me (paypal.me/vlorenzetti982).
  Il testo sta in `docs/sostieni/index.html` e si cambia come quello della pagina principale.
- **Logo**: in `docs/assets/logo/` (marchio quadrato e logo orizzontale, scuro e chiaro), scaricabili anche da
  https://photolab4kids.it/assets/logo/photolab4kids-logo.png

## 1. Crea il tuo account GitHub (5 minuti)

1. Vai su https://github.com/signup e registrati con la tua email (per esempio info@vittorialorenzetti.com).
   Scegli uno username semplice, per esempio `vittorialorenzetti`.
2. GitHub ti chiederà di attivare la **verifica in due passaggi**: fallo con l'app di autenticazione del telefono
   o con una passkey.
3. Manda ad Alberto il tuo username.

## 2. Accetta l'invito al progetto

Alberto ti aggiunge come collaboratrice del progetto. Ti arriva un'email da GitHub: apri il link e premi
**Accept invitation**. Da quel momento puoi cambiare il sito.

Più avanti, se vuoi che il progetto stia proprio sul tuo account, Alberto può trasferirtelo: il sito resta su
photolab4kids.it, cambia solo l'indirizzo su GitHub.

## 3. Cambiare un testo

1. Apri https://github.com/CryptoPannoz/photolab4kids/blob/main/docs/index.html
2. Premi la **matita** in alto a destra («Edit this file»).
3. Trova il testo con Cmd+F (su Windows Ctrl+F) e cambialo. Tocca solo le parole: i pezzi tra `<` e `>` sono
   codice e vanno lasciati com'erano.
4. Premi **Commit changes…**, scrivi in due parole cosa hai cambiato e conferma con **Commit changes**.
5. Dopo 1-2 minuti la modifica è online.

Se qualcosa si rompe, niente paura: GitHub tiene tutte le versioni e si torna indietro in un attimo (basta dirlo
ad Alberto).

## 4. Aggiungere o cambiare una foto

1. Prepara la foto: lato lungo al massimo 1600 px e peso sotto i 400 KB. Su https://squoosh.app la trascini
   dentro, scegli WebP o JPG e la scarichi già leggera.
2. Su GitHub apri la cartella `docs/assets/img`, premi **Add file → Upload files**, trascina la foto e premi
   **Commit changes**.
3. In `docs/index.html` cerca la foto da sostituire e cambia il nome del file dentro `src="assets/img/…"`.
   Aggiorna anche la descrizione dentro `alt="…"`, che serve a chi non vede le immagini.

## 5. Le parti ancora da completare

Sul sito pubblico sono nascoste. Per vederle apri https://photolab4kids.it/?bozza: compaiono evidenziate in
giallo. Oggi mancano:

- numero di incontri e durata dei percorsi da 6 mesi e da 3 mesi;
- programma e luogo del laboratorio nel weekend;
- scuola e anno del laboratorio, nel piede della pagina.

Per riempirle cerca nel file la parola `da-completare`: sostituisci la frase gialla con il testo vero e togli
`class="da-completare"`.

## 6. Il modo più semplice: chiederlo a Claude

Con Claude (claude.ai, piano Pro) puoi chiedere le modifiche a parole, per esempio «cambia la durata del percorso
breve in 10 incontri» o «aggiungi questa foto alla sezione dei collage». Claude Code apre il progetto, fa la
modifica e la pubblica. La prima configurazione la fa Alberto con te.

## Regole da tenere sempre

- **Foto di bambini**: solo quelle coperte dalle liberatorie delle famiglie per il web.
- **Nomi dei bambini**: mai, né nei testi né scritti sui disegni (vanno tagliati dalla foto).
- **Il progetto è pubblico**: chiunque può vedere i file su GitHub. Non caricare contratti, liberatorie, dati delle
  famiglie o altri documenti privati.

## Costi

- GitHub e GitHub Pages: gratis.
- Dominio photolab4kids.it: 11,99 € + IVA l'anno, rinnovo automatico sul conto Aruba di Alberto. Se vuoi
  intestarlo a te, si chiede ad Aruba il cambio di intestatario.
