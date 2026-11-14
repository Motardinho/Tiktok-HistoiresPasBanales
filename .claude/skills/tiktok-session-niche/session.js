// Session TikTok automatique dans l'onglet de Claude in Chrome.
// Coller tel quel dans javascript_tool, après avoir modifié CONFIG.
// Prérequis : l'onglet est sur une vidéo ouverte depuis une recherche TikTok
// (lecteur avec les flèches data-e2e="arrow-right" et le panneau de commentaires).
const CONFIG = {
  niches: ['sport insolite', 'triche dans le sport', 'gossip sportifs', 'scandale sportif', 'exploit sportif incroyable', 'histoire vraie sport', 'sport business', 'scandale sport'],
  nicheDepart: 0,        // index de la niche déjà ouverte dans l'onglet
  parNiche: 6,           // vidéos lues avant de passer à la niche suivante
  dureeMin: 25,          // arrêt automatique
  pauseMin: 5000, pauseMax: 10000, // attente après la fin de la vidéo
  pLike: 0.3, pPartage: 0.1, pCommentaire: 0.2, pSuivi: 0.1,
  pZap: 0.2, zapMin: 5, zapMax: 10, // vidéos passées après quelques secondes, sans aucune action
  dureeMaxSec: 180,      // au-delà de 3 min, la vidéo est zappée d'office
  mots: ['Incroyable !', "Je ne savais pas !", 'Quelle histoire 😮', 'Merci pour le partage', 'Génial !', 'Trop bien',
    'Fascinant ✨', "J'adore", 'Dingue 👌', "J'ai appris un truc", 'Bravo pour la vidéo', 'Wahou 👏'],
};

if (window.__autoNext) { for (const k of ['iv', 'stopIv', 'playIv', 'watchIv']) clearInterval(window.__autoNext[k]); }
// Recollé pendant une session en cours (correction à chaud) : on garde l'avancement, les stats et l'heure d'arrêt.
// Pour repartir de zéro dans le même onglet : `delete window.__autoNext` avant de coller.
const prev = window.__autoNext && !window.__autoNext.stopped ? window.__autoNext : null;
const st = window.__autoNext = {
  ...CONFIG, niche: prev ? prev.niche : CONFIG.nicheDepart, inNiche: prev ? prev.inNiche : 0, count: prev ? prev.count : 0,
  deja: prev ? prev.deja : {}, suivisDeja: prev ? prev.suivisDeja : {},
  stopAt: prev ? prev.stopAt : Date.now() + CONFIG.dureeMin * 60000,
  stats: prev ? prev.stats : { likes: 0, partages: 0, commentaires: 0, suivis: 0, zaps: 0, zapsLongs: 0, illisibles: 0, log: [] },
};
const sleep = ms => new Promise(r => setTimeout(r, ms));

// TikTok met la vidéo en pause dès que l'onglet est caché (fenêtre réduite, autre onglet devant).
// On fait croire à la page qu'elle reste visible et on relance la lecture si elle s'arrête.
Object.defineProperty(document, 'hidden', { configurable: true, get: () => false });
Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' });
Object.defineProperty(document, 'webkitHidden', { configurable: true, get: () => false });
document.hasFocus = () => true;
for (const ev of ['visibilitychange', 'webkitvisibilitychange', 'blur', 'pagehide', 'freeze']) {
  window.addEventListener(ev, e => e.stopImmediatePropagation(), true);
  document.addEventListener(ev, e => e.stopImmediatePropagation(), true);
}
// Une vidéo en sourdine dans un onglet caché est freinée par Chrome (8 novembre 2026 : 95 s lues en 11 min).
// TikTok garde la sourdine dans localStorage « webapp-video-mute » : on la lève et on rétablit le son.
try { localStorage.setItem('webapp-video-mute', JSON.stringify({ muted: false, volume: 0.7 })); } catch (e) {}
st.playIv = setInterval(() => {
  const v = [...document.querySelectorAll('video')].find(x => x.getBoundingClientRect().width > 0);
  if (v && v.muted) { v.muted = false; if (!v.volume) v.volume = 0.7; }
  if (v && v.paused && !v.ended) v.play().catch(() => {});
  if (Date.now() > st.stopAt) clearInterval(st.playIv);
}, 1000);

// Changer de niche sans recharger la page (un rechargement tuerait le script).
window.__switchQ = async function (q) {
  const depuis = location.pathname;
  const c = document.querySelector('[data-e2e="browse-close"]'); if (c) { c.click(); await sleep(1500); }
  const inps = [...document.querySelectorAll('input[data-e2e="search-user-input"]')];
  const inp = inps.find(i => i.getBoundingClientRect().width > 0) || inps[0];
  if (!inp) return 'noinput';
  inp.focus();
  Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(inp, q);
  inp.dispatchEvent(new Event('input', { bubbles: true }));
  await sleep(500);
  inp.closest('form').requestSubmit();
  await sleep(4000);
  if (!/\/search\/video/.test(location.pathname)) {
    const tab = [...document.querySelectorAll('[role="tab"]')].find(e => e.textContent.trim() === 'Vidéos');
    if (tab) { tab.click(); await sleep(3500); }
  }
  // Première vignette pas encore vue dans cette session, sinon la première
  const liens = [...document.querySelectorAll('a[href*="/video/"]')].filter(x => x.getBoundingClientRect().width > 50);
  const a = liens.find(x => !st.deja[new URL(x.href).pathname]) || liens[0];
  if (!a) return 'novideo';
  a.click(); await sleep(3000);
  // 'same' : la page n'a pas changé (panneau pas fermé, clic sans effet) ; l'appelant réessaie avec une autre recherche
  return location.pathname === depuis ? 'same' : 'ok';
};

(function () {
  let cur = null, last = 0, pending = false, plan = null;
  function visibleVideo() {
    let best = null, area = 0;
    for (const v of document.querySelectorAll('video')) {
      const r = v.getBoundingClientRect();
      const h = Math.max(0, Math.min(r.bottom, innerHeight) - Math.max(r.top, 0));
      const w = Math.max(0, Math.min(r.right, innerWidth) - Math.max(r.left, 0));
      if (h * w > area) { area = h * w; best = v; }
    }
    return best;
  }
  const healthy = () => !!document.querySelector('[data-e2e="browse-like-icon"]');
  async function engage(p) {
    const u = location.pathname;
    if (st.deja[u]) return;
    st.deja[u] = true;
    if (p.like) {
      const i = document.querySelector('[data-e2e="browse-like-icon"]'); const b = i && i.closest('button');
      if (b && b.getAttribute('aria-pressed') !== 'true') { b.click(); st.stats.likes++; st.stats.log.push('like ' + u); }
      await sleep(800 + Math.random() * 1500);
    }
    if (p.partage) {
      // « Copier le lien » compte comme un partage sans rien publier.
      const b = document.querySelector('[data-e2e="browse-copy"]');
      if (b) { b.click(); st.stats.partages++; st.stats.log.push('partage ' + u); }
      await sleep(800 + Math.random() * 1500);
    }
    if (p.commentaire) {
      // Éditeur Draft.js : seul un événement « paste » marche. execCommand('insertText') fait planter le panneau.
      const ce = document.querySelector('.public-DraftEditor-content');
      if (ce) {
        const m = st.mots[Math.floor(Math.random() * st.mots.length)];
        ce.focus(); await sleep(300);
        const dt = new DataTransfer(); dt.setData('text/plain', m);
        ce.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
        await sleep(1200 + Math.random() * 1500);
        const b = document.querySelector('[data-e2e="comment-post"]');
        if (b && ce.textContent.trim()) { b.click(); st.stats.commentaires++; st.stats.log.push('commentaire "' + m + '" ' + u); }
        await sleep(1000);
      }
    }
    if (p.suivi) {
      // Bouton « Suivre » en haut à droite du lecteur ; absent ou « Suivi(e) » si le compte est déjà suivi.
      const auteur = (u.match(/^\/@([^/]+)/) || [])[1];
      const b = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Suivre'
        && b.getBoundingClientRect().x > innerWidth / 2 && b.getBoundingClientRect().width > 0);
      if (auteur && !st.suivisDeja[auteur] && b) {
        await sleep(800 + Math.random() * 1500);
        b.click(); st.suivisDeja[auteur] = true; st.stats.suivis++; st.stats.log.push('suivi @' + auteur);
      }
    }
  }
  async function goNext() {
    if (Date.now() > st.stopAt) return;
    st.count++; st.inNiche++;
    const avant = location.pathname;
    const b = document.querySelector('[data-e2e="arrow-right"]');
    // Pas de healthy() ici : onglet en arrière-plan, TikTok ne dessine pas le panneau de droite (like, commentaires)
    // alors que la flèche marche. Le compter comme un panneau planté relançait une recherche après chaque vidéo
    // (9 novembre 2026 : 6 likes sur 61 vidéos au lieu d'environ 15).
    let finNiche = st.inNiche >= st.parNiche || !b || b.disabled;
    if (!finNiche) {
      b.click(); await sleep(2500);
      // La flèche n'a pas changé de vidéo (fin des résultats chargés) : recherche suivante
      finNiche = location.pathname === avant;
      if (finNiche) st.stats.log.push('flèche sans effet sur ' + avant);
    }
    if (finNiche) {
      // Si la recherche ne change pas de page, la suivante, trois essais au plus. Sans cela, la même vidéo longue
      // était rezappée en boucle, une minute perdue par cas (7 novembre 2026).
      for (let k = 0; k < 3; k++) {
        st.niche = (st.niche + 1) % st.niches.length; st.inNiche = 0;
        try { st.lastSwitch = await window.__switchQ(st.niches[st.niche]); } catch (e) { st.err = String(e); st.lastSwitch = 'err'; }
        st.stats.log.push('recherche « ' + st.niches[st.niche] + ' » : ' + st.lastSwitch);
        if (st.lastSwitch === 'ok') break;
        st.stats.coinces = (st.stats.coinces || 0) + 1;
      }
    }
    cur = null; last = 0; pending = false;
  }
  function finished() {
    if (pending) return;
    pending = true;
    setTimeout(goNext, st.pauseMin + Math.random() * (st.pauseMax - st.pauseMin));
  }
  st.iv = setInterval(() => {
    if (pending) return;
    const v = visibleVideo(); if (!v) return;
    if (v !== cur) {
      cur = v; last = v.currentTime;
      plan = { at: 0.3 + Math.random() * 0.55, like: Math.random() < st.pLike, partage: Math.random() < st.pPartage,
        commentaire: Math.random() < st.pCommentaire, suivi: Math.random() < st.pSuivi, done: false };
      if (!st.deja[location.pathname] && Math.random() < st.pZap) {
        plan.zapAt = st.zapMin + Math.random() * (st.zapMax - st.zapMin);
        plan.done = true; st.deja[location.pathname] = true;
      }
      return;
    }
    const t = v.currentTime, dur = v.duration;
    // La durée n'est connue qu'une fois la vidéo chargée : la règle des 3 min se vérifie ici, pas au tirage.
    if (plan && !plan.zapAt && dur > st.dureeMaxSec) {
      plan.zapAt = st.zapMin + Math.random() * (st.zapMax - st.zapMin);
      plan.done = true; plan.longue = true; st.deja[location.pathname] = true;
    }
    if (plan && plan.zapAt && t >= plan.zapAt) {
      pending = true;
      if (plan.longue) { st.stats.zapsLongs++; st.stats.log.push('zap longue ' + Math.round(dur) + ' s ' + location.pathname); }
      else { st.stats.zaps++; st.stats.log.push('zap ' + location.pathname); }
      goNext();
      return;
    }
    // Panneau absent au moment tiré (onglet en arrière-plan) : on retente jusqu'à la fin de la vidéo.
    if (plan && !plan.done && dur && t / dur >= plan.at && healthy()) { plan.done = true; engage(plan); }
    // TikTok relance la vidéo en boucle : « ended » ne vient pas, on détecte le retour au début.
    if ((dur && last > dur - 1.5 && t < last - 1) || v.ended) finished();
    last = t;
  }, 250);
  // Vidéo illisible (« Nous éprouvons des difficultés à lancer cette vidéo ») : la page n'a plus de <video>.
  // Après 15 s sans vidéo, on passe à la suivante.
  let sansVideo = 0;
  st.watchIv = setInterval(() => {
    if (Date.now() > st.stopAt) { clearInterval(st.watchIv); return; }
    const ok = [...document.querySelectorAll('video')].some(v => v.getBoundingClientRect().width > 0)
      || location.pathname.startsWith('/search'); // page de résultats pendant un changement de niche
    sansVideo = ok || pending ? 0 : sansVideo + 1;
    if (sansVideo >= 15) { sansVideo = 0; pending = true; st.stats.illisibles++; st.stats.log.push('illisible ' + location.pathname); goNext(); }
  }, 1000);
  st.stopIv = setInterval(() => {
    if (Date.now() > st.stopAt) { clearInterval(st.iv); clearInterval(st.stopIv); st.stopped = new Date().toLocaleTimeString(); }
  }, 1000);
})();
({ stopAt: new Date(st.stopAt).toLocaleTimeString(), niche: st.niches[st.niche] });
