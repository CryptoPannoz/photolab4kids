// Photolab for Kids — piccole interazioni. Senza JS il sito mostra tutto lo stesso.
document.documentElement.classList.add('js');

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
