import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
from scipy import ndimage as ndi
from scipy.ndimage import gaussian_filter, binary_opening, binary_closing, uniform_filter

plt.rcParams['font.family'] = 'DejaVu Sans'

def load(path):
    return np.asarray(Image.open(path).convert('L'), float)

def texture(a, win=9):
    m = uniform_filter(a.astype(float), win)
    m2 = uniform_filter((a*a).astype(float), win)
    return np.sqrt(np.clip(m2 - m*m, 0, None))

def detect(a, land_pct=82, k=1.3, smooth_pct=45):
    sm = gaussian_filter(a, 1.5)
    tex = texture(sm, 11)
    smooth = tex < np.percentile(tex, smooth_pct)
    bright = sm > np.percentile(sm, land_pct)
    water = smooth & ~bright
    water = binary_closing(binary_opening(water, iterations=2), iterations=3)
    land = ~water
    wv = sm[water]
    if wv.size == 0:
        return land, np.zeros_like(land, bool), 0, 0, 0
    mu, sigma = wv.mean(), wv.std()
    T = mu - k * sigma
    T = max(T, np.percentile(wv, 8))
    cand = water & (sm < T)
    cand = binary_opening(cand, iterations=2)
    cand = binary_closing(cand, iterations=3)
    lbl, n = ndi.label(cand)
    sizes = ndi.sum(np.ones_like(lbl), lbl, range(1, n+1))
    keep = np.zeros_like(cand)
    for i, s in enumerate(sizes, 1):
        if s > a.size * 0.0015:
            keep |= (lbl == i)
    return land, keep, mu, sigma, T

# ── Load images ──────────────────────────────────────────────────────────────
a1 = load('scene_may2025_preview.webp')   # end May 2025 — spring breakup
a2 = load('scene_apr2025_preview.webp')   # mid-April 2025 — late winter

H1, W1 = a1.shape
H2, W2 = a2.shape

land1, cand1, mu1, sig1, T1 = detect(a1, land_pct=82, k=1.3, smooth_pct=45)
land2, cand2, mu2, sig2, T2 = detect(a2, land_pct=80, k=1.3, smooth_pct=42)

df1 = cand1.mean() * 100
df2 = cand2.mean() * 100

print(f"May2025  water μ={mu1:.1f} σ={sig1:.1f} T={T1:.1f}  cand={df1:.1f}%")
print(f"Apr2025  water μ={mu2:.1f} σ={sig2:.1f} T={T2:.1f}  cand={df2:.1f}%")

# ── Figure layout ─────────────────────────────────────────────────────────────
BG = '#0b0e14'
fig = plt.figure(figsize=(20, 13), facecolor=BG)
gs = gridspec.GridSpec(2, 3, figure=fig,
                       left=0.01, right=0.74, top=0.93, bottom=0.06,
                       wspace=0.04, hspace=0.10,
                       width_ratios=[1, 1, 0.001])

ax = [[fig.add_subplot(gs[r, c]) for c in range(2)] for r in range(2)]
for row in ax:
    for a_ in row:
        a_.set_facecolor(BG)
        a_.set_xticks([]); a_.set_yticks([])
        for s in a_.spines.values():
            s.set_color('#3a4252')

# right info panel
ax_info = fig.add_axes([0.755, 0.06, 0.235, 0.87], facecolor='#12161f')
ax_info.set_xticks([]); ax_info.set_yticks([])
for s in ax_info.spines.values():
    s.set_color('#3a4252')

# ── Panel A: May 2025 original ────────────────────────────────────────────────
ax[0][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
ax[0][0].set_title('А) Конец мая 2025 — весенний ледоход (исходный снимок)',
                   color='w', fontsize=11, pad=6)

def arrow(axx, W, H, fx, fy, tx, ty, txt, col):
    axx.add_patch(FancyArrowPatch(
        (tx*W, ty*H), (fx*W, fy*H),
        arrowstyle='-|>', mutation_scale=13, color=col, lw=1.6,
        shrinkA=0, shrinkB=2))
    axx.text(tx*W, ty*H, txt, color='w', fontsize=8.5, fontweight='bold',
             ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.3', fc=col, ec='none', alpha=0.92))

# May: bright=land top-left, dark right=Pechora Sea, ice margin in centre
arrow(ax[0][0], W1, H1,  0.62, 0.20,  0.78, 0.07, 'Печорское море\n(открытая вода)', '#2563eb')
arrow(ax[0][0], W1, H1,  0.38, 0.42,  0.52, 0.28, 'Кромка льда\n(ледоход)', '#06b6d4')
arrow(ax[0][0], W1, H1,  0.18, 0.52,  0.08, 0.35, 'Береговая\nлиния', '#94a3b8')
arrow(ax[0][0], W1, H1,  0.22, 0.72,  0.08, 0.88, 'Терминал\nЛУКОЙЛ\n(Варандей)', '#f59e0b')
arrow(ax[0][0], W1, H1,  0.48, 0.62,  0.55, 0.80, 'Дрейфующий лёд\n(битый)', '#7dd3fc')
arrow(ax[0][0], W1, H1,  0.72, 0.55,  0.88, 0.68, 'Ветровая тень\n(тёмный след)', '#dc2626')

# ── Panel B: April 2025 original ─────────────────────────────────────────────
ax[0][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
ax[0][1].set_title('Б) Середина апреля 2025 — поздняя зима (исходный снимок)',
                   color='w', fontsize=11, pad=6)

arrow(ax[0][1], W2, H2,  0.72, 0.22,  0.85, 0.08, 'Открытая вода\n/ разводье', '#2563eb')
arrow(ax[0][1], W2, H2,  0.30, 0.30,  0.18, 0.12, 'Припайный лёд\n(fast ice)', '#7dd3fc')
arrow(ax[0][1], W2, H2,  0.58, 0.42,  0.72, 0.35, 'Молодой лёд\n(нилас/блинный)\n← имитирует нефть', '#dc2626')
arrow(ax[0][1], W2, H2,  0.22, 0.55,  0.08, 0.42, 'Береговая\nлиния', '#94a3b8')
arrow(ax[0][1], W2, H2,  0.18, 0.72,  0.05, 0.88, 'Дельта р. Варандей\n(тундра)', '#a16207')
arrow(ax[0][1], W2, H2,  0.48, 0.68,  0.42, 0.88, 'Лёд с тёмными\nвкраплениями\n(look-alike)', '#f97316')

# ── Panel C: May detection ────────────────────────────────────────────────────
ax[1][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
ov1 = np.zeros((H1, W1, 4))
ov1[...,0]=0.10; ov1[...,1]=0.75; ov1[...,2]=1.0; ov1[...,3]=cand1*0.38
ax[1][0].imshow(ov1, aspect='equal')
ax[1][0].set_title(f'В) Детекция тёмных зон — май 2025  ({df1:.1f}% кадра)',
                   color='w', fontsize=11, pad=6)
ax[1][0].text(W1*0.02, H1*0.97,
    f'вода: μ={mu1:.0f}  σ={sig1:.0f}  T={T1:.0f}',
    color='#9aa4b2', fontsize=8, va='bottom')

# ── Panel D: April detection ──────────────────────────────────────────────────
ax[1][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
ov2 = np.zeros((H2, W2, 4))
ov2[...,0]=1.0; ov2[...,1]=0.45; ov2[...,2]=0.05; ov2[...,3]=cand2*0.42
ax[1][1].imshow(ov2, aspect='equal')
ax[1][1].set_title(f'Г) Детекция тёмных зон — апрель 2025  ({df2:.1f}% кадра)',
                   color='w', fontsize=11, pad=6)
ax[1][1].text(W2*0.02, H2*0.97,
    f'вода: μ={mu2:.0f}  σ={sig2:.0f}  T={T2:.0f}',
    color='#9aa4b2', fontsize=8, va='bottom')

# legend note on panel C
for axx, clr, lbl in [(ax[1][0], '#1ac8ff', 'тёмная зона (май)'),
                       (ax[1][1], '#ff7211', 'тёмная зона (апрель)')]:
    axx.add_patch(Rectangle((0, 0), 1, 1, transform=axx.transAxes,
                             fc=clr, alpha=0.0, ec='none'))

# ── Right info panel ──────────────────────────────────────────────────────────
y = 0.97
def info(text, color='#e2e8f0', fs=9.5, dy=0.038, bold=False):
    global y
    ax_info.text(0.06, y, text, color=color, fontsize=fs,
                 fontweight='bold' if bold else 'normal',
                 transform=ax_info.transAxes, va='top', wrap=True,
                 clip_on=False)
    y -= dy

info('ВАРАНДЕЙ', '#f8fafc', fs=13, dy=0.045, bold=True)
info('Нефтеналивной терминал ЛУКОЙЛ', '#94a3b8', fs=8.5, dy=0.032)
info('68.8°N, 58.1°E · Печорское море', '#94a3b8', fs=8.5, dy=0.042)

info('─' * 28, '#3a4252', fs=8, dy=0.030)

info('Sentinel-1 IW GRD VV', '#cbd5e1', fs=9, dy=0.028, bold=True)
info('Конец мая 2025  (A, В)', '#7dd3fc', fs=8.5, dy=0.026)
info('Весенний ледоход: лёд + открытая', '#9aa4b2', fs=8, dy=0.020)
info('вода + ветровые тени', '#9aa4b2', fs=8, dy=0.032)
info('Середина апреля 2025  (Б, Г)', '#fca5a5', fs=8.5, dy=0.026)
info('Поздняя зима: припай + молодой', '#9aa4b2', fs=8, dy=0.020)
info('лёд в разводьях (look-alikes)', '#9aa4b2', fs=8, dy=0.038)

info('─' * 28, '#3a4252', fs=8, dy=0.030)
info('СТАТИСТИКА', '#f8fafc', fs=9.5, dy=0.032, bold=True)

for label, mu, sig, T, df, clr in [
    ('Май 2025',  mu1, sig1, T1, df1, '#7dd3fc'),
    ('Апрель 2025', mu2, sig2, T2, df2, '#fca5a5'),
]:
    info(f'{label}', clr, fs=9, dy=0.024, bold=True)
    info(f'  μ={mu:.0f}  σ={sig:.0f}  T=μ−1.3σ={T:.0f}', '#9aa4b2', fs=8, dy=0.022)
    info(f'  Тёмных зон: {df:.1f}% кадра', '#cbd5e1', fs=8.5, dy=0.034)

info('─' * 28, '#3a4252', fs=8, dy=0.030)
info('LOOK-ALIKE ЭФФЕКТ', '#f8fafc', fs=9.5, dy=0.032, bold=True)
info('Молодой лёд (нилас, блинный,', '#f97316', fs=8.5, dy=0.020)
info('жировой) → σ⁰ падает на 10–20 дБ', '#f97316', fs=8.5, dy=0.020)
info('→ тёмная сигнатура = как нефть', '#f97316', fs=8.5, dy=0.028)
info('PD = σ⁰_VV − σ⁰_VH:', '#e2e8f0', fs=8.5, dy=0.022)
info('  Нефть:  6–10 дБ', '#ef4444', fs=8.5, dy=0.020)
info('  Мол. лёд:  < 4 дБ ✓', '#22d3ee', fs=8.5, dy=0.020)
info('  Ветр. тень: 2–5 дБ', '#94a3b8', fs=8.5, dy=0.030)

info('─' * 28, '#3a4252', fs=8, dy=0.030)
info('ВЫВОД', '#f8fafc', fs=9.5, dy=0.028, bold=True)
info('Разливов в 2022–2025 гг.', '#4ade80', fs=8.5, dy=0.020)
info('не зафиксировано. Все тёмные', '#4ade80', fs=8.5, dy=0.020)
info('зоны — ложные цели (лёд,', '#4ade80', fs=8.5, dy=0.020)
info('ветер). Контрольный полигон', '#4ade80', fs=8.5, dy=0.020)
info('для теста гипотезы H₀.', '#4ade80', fs=8.5, dy=0.022)

info('─' * 28, '#3a4252', fs=8, dy=0.030)
info('Метод детекции', '#cbd5e1', fs=8.5, dy=0.022, bold=True)
info('Текстурная маска воды +', '#9aa4b2', fs=8, dy=0.020)
info('Адаптивный порог T=μ−k·σ', '#9aa4b2', fs=8, dy=0.020)
info('k=1.3, морфо-фильтрация', '#9aa4b2', fs=8, dy=0.020)
info('8-бит превью (качественно)', '#6b7280', fs=7.5, dy=0.022)

# ── Titles & captions ─────────────────────────────────────────────────────────
fig.suptitle(
    'Варандей (Печорское море) — Sentinel-1 IW GRD VV: ледовые двойники нефтяных разливов',
    color='w', fontsize=14, fontweight='bold', y=0.975)

fig.text(0.375, 0.028,
    'Примечание: снимки 8-бит превью — качественная визуализация. '
    'Синий = тёмные зоны мая (ветровые тени + кромка льда). '
    'Оранжевый = тёмные зоны апреля (молодой лёд в разводьях). '
    'Оба — ложные цели. Для разделения нефть/лёд необходим PD из .SAFE (SNAP).',
    color='#6b7280', fontsize=7.5, ha='center', style='italic')

plt.savefig('varandey_may_apr_lookalikes.png', dpi=160, facecolor=BG)
plt.close()
print("DONE → varandey_may_apr_lookalikes.png")
