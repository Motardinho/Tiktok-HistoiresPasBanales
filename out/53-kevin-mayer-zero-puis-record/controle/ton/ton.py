"""Mesure du débit, des pauses et du mouvement de la voix : narrateur de Bolt (anglais) contre nos prises (français)."""
import re, sys, wave
import numpy as np
from faster_whisper import WhisperModel

m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8')
print(f"{'fichier':22s} {'durée':>6s} {'mots/s':>6s} {'syll/s':>6s} {'artic':>6s} {'pauses':>7s} {'%sil':>5s} {'f0':>5s} {'étendue':>8s} {'dyn dB':>6s}")
for f in sys.argv[1:]:
    w = wave.open(f); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    lang = 'en' if 'bolt' in f else 'fr'
    segs, _ = m.transcribe(x, language=lang, word_timestamps=True)
    mots = [(a.start, a.end, a.word.strip()) for s in segs for a in s.words]
    if not mots:
        continue
    t0, t1 = mots[0][0], mots[-1][1]
    syll = sum(max(1, len(re.findall(r'[aeiouyàâéèêëîïôöùûü]+', re.sub(r'(?<=[b-df-hj-np-tv-z])e(s|nt)?$', '', a[2].lower()) if lang == 'fr' else a[2].lower()))) for a in mots)
    pauses = [b[0] - a[1] for a, b in zip(mots, mots[1:]) if b[0] - a[1] >= 0.25]
    parle = (t1 - t0) - sum(pauses)
    sr, n, pas, f0, rms = 16000, 800, 160, [], []
    seuil = 0.3 * np.sqrt(np.mean(x ** 2))
    for i in range(int(t0 * sr), min(len(x), int(t1 * sr)) - n, pas):
        t = x[i:i + n] - np.mean(x[i:i + n]); e = np.sqrt(np.mean(t ** 2))
        if e < seuil:
            continue
        rms.append(20 * np.log10(e))
        ac = np.correlate(t, t, 'full')[n - 1:]
        k = 53 + int(np.argmax(ac[53:290]))
        if ac[k] / ac[0] > 0.5:
            f0.append(sr / k)
    et = 12 * np.log2(np.percentile(f0, 90) / np.percentile(f0, 10))
    print(f"{f.split('/')[-1]:22s} {t1 - t0:6.1f} {len(mots) / (t1 - t0):6.2f} {syll / (t1 - t0):6.2f} {syll / parle:6.2f} {len(pauses):3d}x{(np.mean(pauses) if pauses else 0):.2f} {100 * sum(pauses) / (t1 - t0):5.0f} {np.median(f0):5.0f} {et:6.1f} dt {np.percentile(rms, 90) - np.percentile(rms, 10):6.1f}")
    print('   ', ' '.join(a[2] for a in mots)[:230].encode('ascii', 'replace').decode())
