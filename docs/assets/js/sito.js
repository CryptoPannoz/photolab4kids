// PhotoLab4Kids — piccole interazioni. Senza JS il sito mostra tutto lo stesso.
document.documentElement.classList.add('js');
// in bozza (anteprima locale o ?bozza) si vedono i promemoria gialli «da completare»
if (['localhost', '127.0.0.1'].includes(location.hostname) || new URLSearchParams(location.search).has('bozza')) {
  document.documentElement.classList.add('bozza');
}

// Copertina: il serpente si ricompone a strisce (il disegno dalla coda, la foto dalla testa) e poi ondeggia
(() => {
  const figura = document.querySelector('.copertina__serpente');
  if (!figura || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const img = figura.querySelector('img');
  const STRISCE = 40;
  const GIUNTURA = 0.53; // da qui in poi l'immagine è fotografia
  const caso = (min, max) => min + Math.random() * (max - min);

  const strato = document.createElement('div');
  strato.className = 'serpente-anim';
  strato.setAttribute('aria-hidden', 'true');
  const strisce = Array.from({ length: STRISCE }, (_, i) => {
    const striscia = document.createElement('span');
    const foto = i / STRISCE >= GIUNTURA;
    const passo = foto ? STRISCE - 1 - i : i;
    striscia.style.setProperty('--i', i);
    striscia.style.setProperty('--amp', `${((1 - i / STRISCE) * 2.6 + 0.5).toFixed(2)}%`);
    striscia.style.setProperty('--dx', `${(foto ? 1 : -1) * caso(40, 160)}px`);
    striscia.style.setProperty('--dy', `${caso(-60, 60)}px`);
    striscia.style.setProperty('--rot', `${caso(-25, 25)}deg`);
    striscia.style.setProperty('--ritardo', `${passo * 35}ms`);
    strato.append(striscia);
    return striscia;
  });

  // misure di layout (offsetWidth ignora la rotazione della figura)
  const disponi = () => {
    const larghezza = img.offsetWidth;
    const altezza = img.offsetHeight;
    const passo = larghezza / STRISCE;
    strisce.forEach((striscia, i) => Object.assign(striscia.style, {
      left: `${i * passo}px`,
      width: `${Math.ceil(passo) + 1}px`,
      backgroundSize: `${larghezza}px ${altezza}px`,
      backgroundPosition: `${-i * passo}px 0`,
    }));
  };

  const parti = () => {
    const url = `url("${img.currentSrc || img.src}")`;
    strisce.forEach((striscia) => { striscia.style.backgroundImage = url; });
    disponi();
    figura.append(strato);
    figura.classList.add('animato');
    requestAnimationFrame(() => requestAnimationFrame(() => figura.classList.add('composto')));
  };

  new ResizeObserver(disponi).observe(img);
  new IntersectionObserver(([voce]) => strato.classList.toggle('fermo', !voce.isIntersecting)).observe(figura);
  if (img.complete) parti();
  else img.addEventListener('load', parti, { once: true });
})();

// Il flusso di immagini: quando si avvicina carica tutte le foto, anche quelle ancora fuori dal bordo
(() => {
  const flusso = document.querySelector('.flusso');
  if (!flusso) return;
  const osserva = new IntersectionObserver(([voce]) => {
    if (!voce.isIntersecting) return;
    flusso.querySelectorAll('img[loading="lazy"]').forEach((img) => { img.loading = 'eager'; });
    osserva.disconnect();
  }, { rootMargin: '600px 0px' });
  osserva.observe(flusso);
})();

// «Guarda»: dopo qualche secondo davanti alla fotografia arrivano la domanda e i disegni
(() => {
  const foto = document.querySelector('[data-sguardo]');
  if (!foto) return;
  const domanda = document.querySelector('[data-sguardo-domanda]');
  const disegni = document.querySelector('[data-sguardo-disegni]');
  let attesa = null;
  let svelato = false;

  const svela = () => {
    if (svelato) return;
    svelato = true;
    domanda.classList.add('visibile');
    setTimeout(() => disegni.classList.add('visibile'), 1200);
  };

  new IntersectionObserver(([voce]) => {
    clearTimeout(attesa);
    if (voce.isIntersecting) attesa = setTimeout(svela, 3500);
  }, { threshold: 0.6 }).observe(foto);
  // chi scorre oltre senza fermarsi trova comunque i disegni
  new IntersectionObserver(([voce]) => { if (voce.isIntersecting) svela(); }, { threshold: 0.5 }).observe(disegni);
})();

// «La metà che manca»: la forbice taglia via il foglio bianco trascinandola (o scorrendo col dito) verso destra
(() => {
  const opera = document.querySelector('[data-meta]');
  if (!opera) return;
  const img = opera.querySelector('[data-meta-img]');
  const velo = opera.querySelector('.meta__velo');
  const cursore = document.querySelector('[data-meta-cursore]');
  const risposta = document.querySelector('[data-meta-risposta]');
  const bottoni = document.querySelectorAll('.meta__scelta button');
  let gesto = null;

  const aggiorna = () => {
    opera.style.setProperty('--svela', cursore.value);
    risposta.classList.toggle('visibile', Number(cursore.value) > 50);
  };
  const imposta = (valore, animato) => {
    opera.classList.toggle('anima', animato);
    cursore.value = Math.round(Math.min(100, Math.max(0, valore)));
    aggiorna();
  };

  cursore.addEventListener('input', () => {
    opera.classList.add('toccata');
    imposta(cursore.value, false);
  });

  // trascinamento relativo: conta lo spostamento del dito, non il punto in cui si appoggia
  opera.addEventListener('pointerdown', (e) => {
    if (e.button > 0) return;
    gesto = { x: e.clientX, partenza: Number(cursore.value), mosso: false, id: e.pointerId };
  });
  opera.addEventListener('pointermove', (e) => {
    if (!gesto || e.pointerId !== gesto.id) return;
    const dx = e.clientX - gesto.x;
    if (!gesto.mosso) {
      if (Math.abs(dx) < 6) return;
      gesto.mosso = true;
      opera.setPointerCapture(e.pointerId);
      opera.classList.add('toccata', 'trascina');
    }
    imposta(gesto.partenza + (dx / velo.offsetWidth) * 100, false);
  });
  const fine = (e) => {
    if (!gesto || e.pointerId !== gesto.id) return;
    const valore = Number(cursore.value);
    if (!gesto.mosso && e.type === 'pointerup') {
      // un tocco senza trascinare apre o richiude la metà nascosta
      opera.classList.add('toccata');
      imposta(valore > 50 ? 0 : 100, true);
    } else if (gesto.mosso) {
      // uno swipe finisce da solo: verso destra apre tutto, verso sinistra richiude
      const destra = e.clientX >= gesto.x;
      imposta(destra ? (valore > 20 ? 100 : 0) : (valore < 80 ? 0 : 100), true);
    }
    opera.classList.remove('trascina');
    gesto = null;
  };
  opera.addEventListener('pointerup', fine);
  opera.addEventListener('pointercancel', fine);

  bottoni.forEach((bottone) => bottone.addEventListener('click', () => {
    bottoni.forEach((b) => b.setAttribute('aria-pressed', String(b === bottone)));
    const { src, w, h, alt, lato, taglio } = bottone.dataset;
    imposta(0, false);
    Object.assign(img, { src, width: w, height: h, alt });
    opera.dataset.lato = lato;
    opera.style.setProperty('--taglio', `${taglio}%`);
  }));

  aggiorna();
})();
