// Session YouTube Shorts automatique (Claude in Chrome), même esprit que session.js (TikTok).
// Prérequis : l'onglet est sur un Short ouvert depuis une recherche YouTube (clic réel sur la vignette).
// Interface en français (aria-label). Les Shorts bouclent : on détecte le retour au début.
const CONFIG = {
  niches: ['sport insolite', 'triche dans le sport', 'gossip sportifs', 'scandale sportif', 'exploit sportif incroyable', 'histoire vraie sport'],
  nicheDepart: 0, parNiche: 6, dureeMin: 42,
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

window.__switchQ = async function (q) {
  const depuis = location.pathname;
  const inp = [...document.querySelectorAll('input[name="search_query"], input#search')].find(vis);
  if (!inp) return 'noinput';
  inp.focus();
  Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(inp, q);
  inp.dispatchEvent(new Event('input', { bubbles: true }));
  await sleep(500);
  const sb = btn(t => /^(Search|Rechercher)$/.test(t)) || document.querySelector('button#search-icon-legacy');
  if (sb) sb.click(); else inp.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true }));
  await sleep(4000);
  const chip = [...document.querySelectorAll('yt-chip-cloud-chip-renderer, chip-shape, button')].find(e => vis(e) && e.textContent.trim() === 'Shorts');
  if (chip) { chip.click(); await sleep(3500); }
  const liens = [...document.querySelectorAll('a[href*="/shorts/"]')].filter(vis);
  const a = liens.find(x => !st.deja[new URL(x.href).pathname]) || liens[0];
  if (!a) return 'novideo';
  a.click(); await sleep(3500);
  return location.pathname === depuis ? 'same' : 'ok';
};

(function () {
  let cur = null, last = 0, pending = false, plan = null;
  async function engage(p) {
    const u = location.pathname;
    if (st.deja[u]) return;
    st.deja[u] = true;
    try {
      if (p.like) {
        const b = btn(t => /^J'aime cette vidéo/.test(t));
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
        const b = btn(t => /^Afficher .*commentaire/.test(t));
        if (b) {
          b.click(); await sleep(2500);
          const ph = document.querySelector('#placeholder-area'); if (ph && vis(ph)) { ph.click(); await sleep(800); }
          const ce = [...document.querySelectorAll('#contenteditable-root')].find(vis);
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
    st.count++; st.inNiche++;
    const avant = location.pathname;
    const b = btn(t => t === 'Vidéo suivante');
    let finNiche = st.inNiche >= st.parNiche || !b;
    if (!finNiche) {
      b.click(); await sleep(2500);
      finNiche = location.pathname === avant;
      if (finNiche) st.stats.log.push('suivante sans effet sur ' + avant);
    }
    if (finNiche) {
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
  function finished() { if (pending) return; pending = true; setTimeout(goNext, st.pauseMin + Math.random() * (st.pauseMax - st.pauseMin)); }
  st.iv = setInterval(() => {
    if (pending) return;
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
