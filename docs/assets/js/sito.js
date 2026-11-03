// Photolab for Kids — piccole interazioni. Senza JS il sito mostra tutto lo stesso.
document.documentElement.classList.add('js');

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

// «Guarda»: conta i secondi passati davanti alla fotografia, poi fa la domanda e mostra i disegni
(() => {
  const foto = document.querySelector('[data-sguardo]');
  if (!foto) return;
  const testo = foto.querySelector('[data-sguardo-testo]');
  const domanda = document.querySelector('[data-sguardo-domanda]');
  const disegni = document.querySelector('[data-sguardo-disegni]');
  let secondi = 0;
  let visibile = false;
  let svelato = false;

  const svela = () => {
    if (svelato) return;
    svelato = true;
    domanda.classList.add('visibile');
    setTimeout(() => disegni.classList.add('visibile'), 1200);
  };

  setInterval(() => {
    if (!visibile || document.hidden) return;
    secondi += 1;
    testo.textContent = `La stai guardando da ${secondi} ${secondi === 1 ? 'secondo' : 'secondi'}`;
    if (secondi === 7) svela();
  }, 1000);

  new IntersectionObserver(([voce]) => { visibile = voce.isIntersecting; }, { threshold: 0.6 }).observe(foto);
  // chi scorre oltre senza fermarsi trova comunque i disegni
  new IntersectionObserver(([voce]) => { if (voce.isIntersecting) svela(); }, { threshold: 0.5 }).observe(disegni);
})();

// «La metà che manca»: il cursore toglie il foglio bianco dalla metà disegnata
(() => {
  const opera = document.querySelector('[data-meta]');
  if (!opera) return;
  const img = opera.querySelector('[data-meta-img]');
  const cursore = document.querySelector('[data-meta-cursore]');
  const risposta = document.querySelector('[data-meta-risposta]');
  const bottoni = document.querySelectorAll('.meta__scelta button');

  const aggiorna = () => {
    opera.style.setProperty('--svela', cursore.value);
    risposta.classList.toggle('visibile', Number(cursore.value) > 60);
  };

  cursore.addEventListener('input', () => {
    opera.classList.remove('anima');
    aggiorna();
  });

  // un clic sull'opera apre o richiude la metà nascosta
  opera.addEventListener('click', () => {
    opera.classList.add('anima');
    cursore.value = Number(cursore.value) > 50 ? 0 : 100;
    aggiorna();
  });

  bottoni.forEach((bottone) => bottone.addEventListener('click', () => {
    bottoni.forEach((b) => b.setAttribute('aria-pressed', String(b === bottone)));
    const { src, w, h, alt, lato, taglio } = bottone.dataset;
    opera.classList.remove('anima');
    cursore.value = 0;
    aggiorna();
    Object.assign(img, { src, width: w, height: h, alt });
    opera.dataset.lato = lato;
    opera.style.setProperty('--taglio', `${taglio}%`);
  }));

  aggiorna();
})();
