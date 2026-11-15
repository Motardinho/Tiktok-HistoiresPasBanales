// Session YouTube Shorts automatique (Claude in Chrome), même esprit que session.js (TikTok).
// Prérequis : l'onglet est sur un Short ouvert depuis une recherche YouTube (clic réel sur la vignette, pour que le son
// soit autorisé). Les Shorts suivants viennent de la recherche lue par fetch (file de parNiche Shorts par niche).
// Interface en français (aria-label). Les Shorts bouclent : on détecte le retour au début.
const CONFIG = {
  niches: ['sport insolite', 'triche dans le sport', 'gossip sportifs', 'scandale sportif', 'exploit sportif incroyable', 'histoire vraie sport', 'sport business', 'scandale sport'],
  nicheDepart: 0, parNiche: 6, dureeMin: 83,
  pauseMin: 5000, pauseMax: 10000,
  pLike: 0.3, pPartage: 0.1, pCommentaire: 0.2, pSuivi: 0.1,
  pZap: 0.2, zapMin: 5, zapMax: 10, dureeMaxSec: 180,
  mots: ['Incroyable !', 'Je ne savais pas !', 'Quelle histoire 😮', 'Merci pour le partage', 'Génial !', 'Trop bien',
    'Fascinant ✨', "J'adore", 'Dingue 👌', "J'ai appris un truc", 'Bravo pour la vidéo', 'Wahou 👏'],
};
if (window.__yt) { for (const k of ['iv', 'stopIv', 'playIv']) clearInterval(window.__yt[k]); }
const prev = window.__yt && !window.__yt.stopped ? window.__yt : null;
const st = window.__yt = {
  ...CONFIG, niche: prev ? prev.niche : CONFIG.nicheDepart, inNiche: prev ? prev.inNiche : 0, count: prev ? prev.count : 0,
  deja: prev ? prev.deja : {}, suivisDeja: prev ? prev.suivisDeja : {},
  stopAt: prev ? prev.stopAt : Date.now() + CONFIG.dureeMin * 60000,
  stats: prev ? prev.stats : { likes: 0, partages: 0, commentaires: 0, suivis: 0, zaps: 0, zapsLongs: 0, illisibles: 0, log: [] },
};
const sleep = ms => new Promise(r => setTimeout(r, ms));
const vis = e => e && e.getBoundingClientRect().width > 0;
const btn = pred => [...document.querySelectorAll('button')].find(b => vis(b) && pred((b.getAttribute('aria-label') || b.textContent || '').trim()));

Object.defineProperty(document, 'hidden', { configurable: true, get: () => false });
Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' });
document.hasFocus = () => true;
for (const ev of ['visibilitychange', 'blur', 'pagehide', 'freeze']) {
  window.addEventListener(ev, e => e.stopImmediatePropagation(), true);
  document.addEventListener(ev, e => e.stopImmediatePropagation(), true);
}
const video = () => [...document.querySelectorAll('video')].find(vis);
st.playIv = setInterval(() => {
  const v = video();
  if (v && v.muted) v.muted = false;
  if (v && v.paused && !v.ended) v.play().catch(() => {});
  if (Date.now() > st.stopAt) clearInterval(st.playIv);
}, 1000);

// Navigation sans affichage (14 novembre 2026). Onglet YouTube en arrière-plan derrière TikTok : Chrome ne dessine plus
// la page, la flèche « Vidéo suivante » échoue (2 sur 5 en 15 s) et la page de résultats ne montre aucun Short
// (12 passages en 83 min, « novideo » en série). On lit donc la recherche par fetch et on change de Short par
// l'événement interne yt-navigate : 4 sur 4 en 0,25 s onglet caché, la vidéo avance normalement.
st.file = prev && prev.file ? prev.file : [];
window.__remplir = async function (q) {
  const html = await (await fetch('/results?search_query=' + encodeURIComponent(q) + '&sp=EgIQCQ%253D%253D')).text();
  const ids = [...new Set([...html.matchAll(/\/shorts\/([\w-]{11})/g)].map(m => m[1]))].filter(id => !st.deja['/shorts/' + id]);
  st.file = ids.slice(0, st.parNiche);
  return st.file.length;
};
window.__go = async function (id) {
  document.querySelector('ytd-app').dispatchEvent(new CustomEvent('yt-navigate', { bubbles: true, composed: true, detail: { endpoint: {
    commandMetadata: { webCommandMetadata: { url: '/shorts/' + id, webPageType: 'WEB_PAGE_TYPE_SHORTS', rootVe: 37414 } },
    reelWatchEndpoint: { videoId: id } } } }));
  for (let i = 0; i < 20 && location.pathname !== '/shorts/' + id; i++) await sleep(500);
  return location.pathname === '/shorts/' + id;
};
// Nouvelle session : la file part de la niche de départ (celle de la recherche ouverte à la main).
if (!prev) window.__remplir(st.niches[st.niche]).catch(e => { st.err = String(e); });

(function () {
  let cur = null, last = 0, pending = false, plan = null;
  async function engage(p) {
    const u = location.pathname;
    if (st.deja[u]) return;
    st.deja[u] = true;
    try {
      if (p.like) {
        const b = btn(t => /J'aime cette vidéo/.test(t));
        if (b && b.getAttribute('aria-pressed') !== 'true') { b.click(); st.stats.likes++; st.stats.log.push('like ' + u); }
        await sleep(800 + Math.random() * 1500);
      }
      if (p.partage) {
        const b = btn(t => t === 'Partager');
        if (b) {
          b.click(); await sleep(1500);
          const c = btn(t => /^Copier/.test(t));
          if (c) { c.click(); st.stats.partages++; st.stats.log.push('partage ' + u); await sleep(1000); }
          const f = btn(t => /^(Fermer|Annuler)/.test(t)); if (f) f.click();
          await sleep(1000);
        }
      }
      if (p.commentaire) {
        // Libellé parfois préfixé par YouTube : « [=1]Afficher 1 commentaire » (14 novembre 2026, d'où 0 commentaire en 83 min).
        const b = btn(t => /Afficher .*commentaire/.test(t));
        if (b) {
          b.click();
          let ph = null;
          for (let i = 0; i < 10 && !ph; i++) { await sleep(500); ph = [...document.querySelectorAll('#placeholder-area')].find(vis); }
          if (ph) { ph.click(); await sleep(1000); }
          let ce = null;
          for (let i = 0; i < 6 && !ce; i++) { ce = [...document.querySelectorAll('#contenteditable-root')].find(vis); if (!ce) await sleep(500); }
          if (ce) {
            const m = st.mots[Math.floor(Math.random() * st.mots.length)];
            ce.focus(); await sleep(300);
            document.execCommand('insertText', false, m);
            await sleep(1200 + Math.random() * 1500);
            const s = [...document.querySelectorAll('#submit-button button, button[aria-label="Commenter"]')].find(vis);
            if (s && ce.textContent.trim()) { s.click(); st.stats.commentaires++; st.stats.log.push('commentaire "' + m + '" ' + u); }
            await sleep(1500);
          }
          const f = btn(t => /^Fermer/.test(t)); if (f) f.click();
          await sleep(800);
        }
      }
      if (p.suivi) {
        const b = btn(t => /^S.abonner à/.test(t));
        const auteur = b && b.getAttribute('aria-label').replace(/^S.abonner à /, '');
        if (b && !st.suivisDeja[auteur]) {
          await sleep(800 + Math.random() * 1500);
          b.click(); st.suivisDeja[auteur] = true; st.stats.suivis++; st.stats.log.push('abonné ' + auteur);
        }
      }
    } catch (e) { st.err = String(e); }
  }
  async function goNext() {
    if (Date.now() > st.stopAt) return;
    st.count++;
    for (let essai = 0; essai < 6; essai++) {
      if (!st.file.length) {
        st.niche = (st.niche + 1) % st.niches.length;
        let n = 0; try { n = await window.__remplir(st.niches[st.niche]); } catch (e) { st.err = String(e); }
        st.stats.log.push('recherche « ' + st.niches[st.niche] + ' » : ' + n + ' Shorts');
        if (!n) { st.stats.coinces = (st.stats.coinces || 0) + 1; continue; }
      }
      const id = st.file.shift();
      if (await window.__go(id)) break;
      st.stats.log.push('navigation sans effet vers ' + id);
    }
    await sleep(1500);
    cur = null; last = 0; pending = false;
  }
  function finished() { if (pending) return; pending = true; setTimeout(goNext, st.pauseMin + Math.random() * (st.pauseMax - st.pauseMin)); }
  st.iv = setInterval(() => {
    if (pending) return;
    // Sur la page de résultats, l'aperçu d'une vidéo longue était pris pour un Short (« zap longue 1566 s /results »).
    if (!location.pathname.startsWith('/shorts/')) return;
    const v = video(); if (!v) return;
    if (v !== cur || v.dataset.ytPath !== location.pathname) {
      cur = v; v.dataset.ytPath = location.pathname; last = v.currentTime;
      plan = { at: 0.3 + Math.random() * 0.55, like: Math.random() < st.pLike, partage: Math.random() < st.pPartage,
        commentaire: Math.random() < st.pCommentaire, suivi: Math.random() < st.pSuivi, done: false };
      if (!st.deja[location.pathname] && Math.random() < st.pZap) {
        plan.zapAt = st.zapMin + Math.random() * (st.zapMax - st.zapMin); plan.done = true; st.deja[location.pathname] = true;
      }
      return;
    }
    const t = v.currentTime, dur = v.duration;
    if (plan && !plan.zapAt && dur > st.dureeMaxSec) {
      plan.zapAt = st.zapMin + Math.random() * (st.zapMax - st.zapMin); plan.done = true; plan.longue = true; st.deja[location.pathname] = true;
    }
    if (plan && plan.zapAt && t >= plan.zapAt) {
      pending = true;
      if (plan.longue) { st.stats.zapsLongs++; st.stats.log.push('zap longue ' + Math.round(dur) + ' s ' + location.pathname); }
      else { st.stats.zaps++; st.stats.log.push('zap ' + location.pathname); }
      goNext(); return;
    }
    if (plan && !plan.done && dur && t / dur >= plan.at) { plan.done = true; engage(plan); }
    if ((dur && last > dur - 1.5 && t < last - 1) || v.ended) finished();
    last = t;
  }, 250);
  st.stopIv = setInterval(() => {
    if (Date.now() > st.stopAt) { clearInterval(st.iv); clearInterval(st.stopIv); st.stopped = new Date().toLocaleTimeString(); }
  }, 1000);
})();
({ stopAt: new Date(st.stopAt).toLocaleTimeString(), niche: st.niches[st.niche] });
