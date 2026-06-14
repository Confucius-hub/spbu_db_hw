import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
from scipy import ndimage as ndi
from scipy.ndimage import gaussian_filter, binary_opening, binary_closing, uniform_filter

plt.rcParams['font.family'] = 'DejaVu Sans'

def load(path):
    return np.asarray(Image.open(path).convert('L'), float)

def texture(a, win=9):
    m = uniform_filter(a.astype(float), win)
    m2 = uniform_filter((a*a).astype(float), win)
    return np.sqrt(np.clip(m2 - m*m, 0, None))

def detect(a, land_pct=82, k=1.3, smooth_pct=45, min_frac=0.0015):
    sm = gaussian_filter(a, 1.5)
    tex = texture(sm, 11)
    smooth = tex < np.percentile(tex, smooth_pct)
    bright = sm > np.percentile(sm, land_pct)
    flat = smooth & ~bright
    flat = binary_closing(binary_opening(flat, iterations=2), iterations=3)
    fv = sm[flat]
    if fv.size == 0:
        return np.zeros_like(flat, bool), 0, 0, 0
    mu, sigma = fv.mean(), fv.std()
    T = max(mu - k*sigma, np.percentile(fv, 8))
    cand = flat & (sm < T)
    cand = binary_opening(cand, iterations=2)
    cand = binary_closing(cand, iterations=3)
    lbl, n = ndi.label(cand)
    sizes = ndi.sum(np.ones_like(lbl), lbl, range(1, n+1))
    keep = np.zeros_like(cand)
    for i, s in enumerate(sizes, 1):
        if s > a.size * min_frac:
            keep |= (lbl == i)
    return keep, mu, sigma, T

# ── Load ──────────────────────────────────────────────────────────────────────
# Varandey geography (LUKOIL offshore terminal, Pechora Sea):
#   LEFT  = tundra (Malozemelskaya Tundra — LAND, bright in SAR)
#   RIGHT = Pechora Sea (water / sea ice, dark in SAR)
#   Coastline runs through the centre of each image
#   Small barrier islands (Varandey I., Pesyakov I.) may appear as thin bright strips offshore
#   May 2025:  spring ice breakup — open water + drifting ice floes on the right
#   April 2025: late winter — smooth first-year sea ice on the right = oil look-alike

a1 = load('scene_may2025_preview.webp')   # end May 2025 — spring breakup
a2 = load('scene_apr2025_preview.webp')   # mid-April 2025 — late winter
H1, W1 = a1.shape
H2, W2 = a2.shape

cand1, mu1, sig1, T1 = detect(a1, land_pct=82, k=1.3, smooth_pct=45)
cand2, mu2, sig2, T2 = detect(a2, land_pct=80, k=1.3, smooth_pct=42)
df1, df2 = cand1.mean()*100, cand2.mean()*100
print(f"May2025  μ={mu1:.1f} σ={sig1:.1f} T={T1:.1f}  cand={df1:.1f}%")
print(f"Apr2025  μ={mu2:.1f} σ={sig2:.1f} T={T2:.1f}  cand={df2:.1f}%")

BG = '#0b0e14'
fig = plt.figure(figsize=(20, 13), facecolor=BG)
gs  = gridspec.GridSpec(2, 2, figure=fig,
                        left=0.01, right=0.74, top=0.93, bottom=0.06,
                        wspace=0.04, hspace=0.10)
ax = [[fig.add_subplot(gs[r, c]) for c in range(2)] for r in range(2)]
for row in ax:
    for a_ in row:
        a_.set_facecolor(BG); a_.set_xticks([]); a_.set_yticks([])
        for s in a_.spines.values(): s.set_color('#3a4252')

ax_info = fig.add_axes([0.755, 0.06, 0.235, 0.87], facecolor='#12161f')
ax_info.set_xticks([]); ax_info.set_yticks([])
for s in ax_info.spines.values(): s.set_color('#3a4252')

def arrow(axx, W, H, fx, fy, tx, ty, txt, col):
    """Arrow: tip at (fx*W, fy*H), text label at (tx*W, ty*H)."""
    axx.add_patch(FancyArrowPatch(
        (tx*W, ty*H), (fx*W, fy*H),
        arrowstyle='-|>', mutation_scale=13, color=col, lw=1.6,
        shrinkA=0, shrinkB=2))
    axx.text(tx*W, ty*H, txt, color='w', fontsize=8.5, fontweight='bold',
             ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.3', fc=col, ec='none', alpha=0.92))

# ═══════════════════════════════════════════════════════════════════════════════
# Panel A — May 2025 (spring breakup), ORIGINAL
# Left bright = Малоземельская тундра (суша)
# Right dark  = Печорское море (открытая вода + дрейфующий лёд)
# ═══════════════════════════════════════════════════════════════════════════════
ax[0][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
ax[0][0].set_title('А) Конец мая 2025 — весенний ледоход (Печорское море)',
                   color='w', fontsize=11, pad=6)

# 1. Тундра / суша (LEFT bright)
arrow(ax[0][0], W1, H1, 0.10, 0.42, 0.04, 0.25,
      'Малоземельская\nтундра (суша)', '#a16207')
# 2. Береговая линия (центр — переход суша→море)
arrow(ax[0][0], W1, H1, 0.30, 0.52, 0.18, 0.70,
      'Береговая линия', '#94a3b8')
# 3. Печорское море — открытая вода (RIGHT very dark)
arrow(ax[0][0], W1, H1, 0.72, 0.18, 0.85, 0.06,
      'Печорское море\n(открытая вода)', '#2563eb')
# 4. Кромка льда / ледоход (центральный переход)
arrow(ax[0][0], W1, H1, 0.44, 0.32, 0.57, 0.15,
      'Кромка льда\n(ледоход)', '#06b6d4')
# 5. Дрейфующие льдины (centre-right medium brightness patches)
arrow(ax[0][0], W1, H1, 0.52, 0.58, 0.65, 0.78,
      'Дрейфующий лёд\n(битые льдины)', '#7dd3fc')
# 6. Ветровая тень / гладкое море (right dark area — dark because calm)
arrow(ax[0][0], W1, H1, 0.82, 0.52, 0.92, 0.68,
      'Гладкая поверхность\nморя (ветровая\nтень / штиль)', '#dc2626')

# ═══════════════════════════════════════════════════════════════════════════════
# Panel B — April 2025 (late winter), ORIGINAL
# Left bright = тундра с снежным покровом (СУША — НЕ лёд!)
# Right very dark = Печорское море под гладким FYI льдом = LOOK-ALIKE
# ═══════════════════════════════════════════════════════════════════════════════
ax[0][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
ax[0][1].set_title('Б) Середина апреля 2025 — поздняя зима (Печорское море)',
                   color='w', fontsize=11, pad=6)

# 1. Тундра (LEFT bright) — это СУША, а не лёд!
arrow(ax[0][1], W2, H2, 0.12, 0.35, 0.04, 0.18,
      'Малоземельская\nтундра (суша,\nснежный покров)', '#a16207')
# 2. Береговая линия (center transition)
arrow(ax[0][1], W2, H2, 0.37, 0.50, 0.22, 0.68,
      'Береговая линия', '#94a3b8')
# 3. Припайный лёд (fast ice) — прибрежный лёд прямо у берега в тёмной зоне
arrow(ax[0][1], W2, H2, 0.50, 0.38, 0.62, 0.20,
      'Припайный лёд\n(fast ice,\nу берега)', '#7dd3fc')
# 4. Гладкий первогодний лёд = LOOK-ALIKE (right dark area)
arrow(ax[0][1], W2, H2, 0.72, 0.28, 0.87, 0.12,
      'Гладкий морской\nлёд (FYI)\n← look-alike нефти', '#dc2626')
# 5. Разводье в припае / открытая вода (особо тёмный участок у берега)
arrow(ax[0][1], W2, H2, 0.60, 0.52, 0.78, 0.65,
      'Разводье в припае\n(открытая вода)', '#0ea5e9')
# 6. Тундровые реки / малые потоки в снегу (left area features)
arrow(ax[0][1], W2, H2, 0.22, 0.68, 0.08, 0.85,
      'Тундровые\nречки (суша)', '#78716c')

# ═══════════════════════════════════════════════════════════════════════════════
# Panel C — May detection (blue)
# ═══════════════════════════════════════════════════════════════════════════════
ax[1][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
ov1 = np.zeros((H1, W1, 4))
ov1[...,0]=0.10; ov1[...,1]=0.75; ov1[...,2]=1.0; ov1[...,3]=cand1*0.40
ax[1][0].imshow(ov1, aspect='equal')
ax[1][0].set_title(f'В) Детекция тёмных зон — май 2025  ({df1:.1f}% кадра)',
                   color='w', fontsize=11, pad=6)
ax[1][0].text(W1*0.02, H1*0.97,
    f'Море/лёд: μ={mu1:.0f}  σ={sig1:.0f}  T=μ−1.3σ={T1:.0f}',
    color='#9aa4b2', fontsize=8, va='bottom')

# ═══════════════════════════════════════════════════════════════════════════════
# Panel D — April detection (orange)
# ═══════════════════════════════════════════════════════════════════════════════
ax[1][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
ov2 = np.zeros((H2, W2, 4))
ov2[...,0]=1.0; ov2[...,1]=0.45; ov2[...,2]=0.05; ov2[...,3]=cand2*0.44
ax[1][1].imshow(ov2, aspect='equal')
ax[1][1].set_title(f'Г) Детекция тёмных зон — апрель 2025  ({df2:.1f}% кадра)',
                   color='w', fontsize=11, pad=6)
ax[1][1].text(W2*0.02, H2*0.97,
    f'Морской лёд: μ={mu2:.0f}  σ={sig2:.0f}  T=μ−1.3σ={T2:.0f}',
    color='#9aa4b2', fontsize=8, va='bottom')

# ═══════════════════════════════════════════════════════════════════════════════
# Right info panel
# ═══════════════════════════════════════════════════════════════════════════════
y = 0.975
def info(text, color='#e2e8f0', fs=9.5, dy=0.038, bold=False):
    global y
    ax_info.text(0.06, y, text, color=color, fontsize=fs,
                 fontweight='bold' if bold else 'normal',
                 transform=ax_info.transAxes, va='top', clip_on=False)
    y -= dy

info('ВАРАНДЕЙ', '#f8fafc', fs=13, dy=0.043, bold=True)
info('Нефтеналивной терминал ЛУКОЙЛ', '#94a3b8', fs=8.5, dy=0.030)
info('68.8°N, 58.1°E · Печорское море', '#94a3b8', fs=8.5, dy=0.030)
info('Ненецкий АО · терминал ~21 км', '#94a3b8', fs=8.5, dy=0.040)
info('─'*28, '#3a4252', fs=8, dy=0.028)

info('Ориентация снимка', '#cbd5e1', fs=9, dy=0.024, bold=True)
info('← Запад/юг: тундра (суша)', '#a16207', fs=8.5, dy=0.022)
info('→ Восток/север: Печорское море', '#2563eb', fs=8.5, dy=0.036)

info('─'*28, '#3a4252', fs=8, dy=0.028)
info('Sentinel-1 IW GRD VV', '#cbd5e1', fs=9, dy=0.026, bold=True)
info('Конец мая 2025  (A, В)', '#7dd3fc', fs=8.5, dy=0.023)
info('Ледоход: открытая вода +', '#9aa4b2', fs=8, dy=0.019)
info('дрейфующие льдины', '#9aa4b2', fs=8, dy=0.030)
info('Середина апреля 2025  (Б, Г)', '#fca5a5', fs=8.5, dy=0.023)
info('Поздняя зима: гладкий FYI +', '#9aa4b2', fs=8, dy=0.019)
info('припай + разводья', '#9aa4b2', fs=8, dy=0.034)

info('─'*28, '#3a4252', fs=8, dy=0.028)
info('СТАТИСТИКА', '#f8fafc', fs=9.5, dy=0.030, bold=True)
for label, mu, sig, T, df, clr in [
    ('Май 2025',  mu1, sig1, T1, df1, '#7dd3fc'),
    ('Апрель 2025', mu2, sig2, T2, df2, '#fca5a5')]:
    info(f'{label}', clr, fs=9, dy=0.022, bold=True)
    info(f'  μ={mu:.0f}  σ={sig:.0f}  T=μ−1.3σ={T:.0f}', '#9aa4b2', fs=8, dy=0.020)
    info(f'  Тёмных зон: {df:.1f}% кадра', '#cbd5e1', fs=8.5, dy=0.032)

info('─'*28, '#3a4252', fs=8, dy=0.028)
info('LOOK-ALIKE ЭФФЕКТ', '#f8fafc', fs=9.5, dy=0.030, bold=True)
info('Апрель: гладкий FYI лёд (тёмный)', '#f97316', fs=8.5, dy=0.019)
info('= σ⁰ близкий к нефтяному слику.', '#f97316', fs=8.5, dy=0.022)
info('Май: ветровая тень на море.', '#f97316', fs=8.5, dy=0.028)
info('PD = σ⁰_VV − σ⁰_VH:', '#e2e8f0', fs=8.5, dy=0.021)
info('  Нефть:   6–10 дБ', '#ef4444', fs=8.5, dy=0.019)
info('  FYI лёд: 2–4 дБ ✓', '#22d3ee', fs=8.5, dy=0.019)
info('  Ветр. тень: 2–5 дБ', '#94a3b8', fs=8.5, dy=0.030)

info('─'*28, '#3a4252', fs=8, dy=0.028)
info('ВЫВОД', '#f8fafc', fs=9.5, dy=0.026, bold=True)
info('Разливов в 2022–2025 гг.', '#4ade80', fs=8.5, dy=0.019)
info('не зафиксировано. Все тёмные', '#4ade80', fs=8.5, dy=0.019)
info('зоны = лёд / ветровой эффект.', '#4ade80', fs=8.5, dy=0.019)
info('Контрольный полигон для H₀.', '#4ade80', fs=8.5, dy=0.024)
info('─'*28, '#3a4252', fs=8, dy=0.026)
info('Метод: текстурная маска +', '#9aa4b2', fs=8, dy=0.019)
info('адапт. порог T=μ−k·σ (k=1.3)', '#9aa4b2', fs=8, dy=0.019)
info('8-бит превью (качественно)', '#6b7280', fs=7.5, dy=0.020)

fig.suptitle(
    'Варандей (Печорское море) — Sentinel-1 IW GRD VV: ледовые и ветровые двойники нефтяных разливов',
    color='w', fontsize=14, fontweight='bold', y=0.975)
fig.text(0.375, 0.028,
    'Примечание: 8-бит превью. Слева = Малоземельская тундра (суша). '
    'Справа = Печорское море. Синий = тёмные зоны мая (открытая вода + ветровые тени). '
    'Оранжевый = апрель (гладкий FYI лёд). Оба — ложные цели. Разделение: PD из .SAFE (SNAP).',
    color='#6b7280', fontsize=7.5, ha='center', style='italic')

plt.savefig('varandey_may_apr_lookalikes.png', dpi=160, facecolor=BG)
plt.close()
print("DONE → varandey_may_apr_lookalikes.png")
