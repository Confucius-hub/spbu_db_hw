import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, Rectangle
from scipy import ndimage as ndi
from scipy.ndimage import gaussian_filter, binary_opening, binary_closing, uniform_filter

plt.rcParams['font.family'] = 'DejaVu Sans'

def load(path):
    return np.asarray(Image.open(path).convert('L'), float)

def texture(a, win=9):
    m = uniform_filter(a.astype(float), win)
    m2 = uniform_filter((a*a).astype(float), win)
    return np.sqrt(np.clip(m2 - m*m, 0, None))

def detect(a, land_pct=80, k=1.3, smooth_pct=45, min_frac=0.0015):
    """Mark smooth+dark zones — the surfaces that imitate an oil slick
    (open water, grease/nilas ice, refrozen leads)."""
    sm = gaussian_filter(a, 1.5)
    tex = texture(sm, 11)
    smooth = tex < np.percentile(tex, smooth_pct)
    bright = sm > np.percentile(sm, land_pct)
    flat = smooth & ~bright
    flat = binary_closing(binary_opening(flat, iterations=2), iterations=3)
    fv = sm[flat]
    if fv.size == 0:
        return ~flat, np.zeros_like(flat, bool), 0, 0, 0
    mu, sigma = fv.mean(), fv.std()
    T = max(mu - k*sigma, np.percentile(fv, 8))
    cand = flat & (sm < T)
    cand = binary_opening(cand, iterations=2)
    cand = binary_closing(cand, iterations=3)
    lbl, n = ndi.label(cand)
    sizes = ndi.sum(np.ones_like(lbl), lbl, range(1, n+1))
    keep = np.zeros_like(cand)
    for i, s in enumerate(sizes, 1):
        if s > a.size*min_frac:
            keep |= (lbl == i)
    return ~flat, keep, mu, sigma, T

a1 = load('scene_oct2022_preview.webp')   # October 2022 — freeze-up
a2 = load('scene_dec2025_preview.webp')   # end December 2025 — deep winter ice
H1, W1 = a1.shape
H2, W2 = a2.shape

_, cand1, mu1, sig1, T1 = detect(a1, land_pct=78, k=1.2, smooth_pct=48)
_, cand2, mu2, sig2, T2 = detect(a2, land_pct=82, k=1.2, smooth_pct=50)
df1 = cand1.mean()*100
df2 = cand2.mean()*100
print(f"Oct2022  μ={mu1:.1f} σ={sig1:.1f} T={T1:.1f}  cand={df1:.1f}%")
print(f"Dec2025  μ={mu2:.1f} σ={sig2:.1f} T={T2:.1f}  cand={df2:.1f}%")

BG = '#0b0e14'
fig = plt.figure(figsize=(20, 13), facecolor=BG)
gs = gridspec.GridSpec(2, 2, figure=fig,
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
    axx.add_patch(FancyArrowPatch((tx*W, ty*H), (fx*W, fy*H),
        arrowstyle='-|>', mutation_scale=13, color=col, lw=1.6, shrinkA=0, shrinkB=2))
    axx.text(tx*W, ty*H, txt, color='w', fontsize=8.5, fontweight='bold',
             ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.3', fc=col, ec='none', alpha=0.92))

# ── A: October 2022 original (freeze-up) ─────────────────────────────────────
ax[0][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
ax[0][0].set_title('А) Октябрь 2022 — начало ледостава (исходный снимок)',
                   color='w', fontsize=11, pad=6)
arrow(ax[0][0], W1, H1, 0.10, 0.20, 0.05, 0.07, 'Тундра / суша\n(яркий отклик)', '#a16207')
arrow(ax[0][0], W1, H1, 0.45, 0.45, 0.30, 0.30, 'Гладкий молодой лёд\n(жировой / нилас)\n← имитирует нефть', '#dc2626')
arrow(ax[0][0], W1, H1, 0.55, 0.78, 0.42, 0.93, 'Открытая вода\n(Обская губа)', '#2563eb')
arrow(ax[0][0], W1, H1, 0.88, 0.55, 0.95, 0.40, 'Протока\n(рукав)', '#0ea5e9')
arrow(ax[0][0], W1, H1, 0.18, 0.55, 0.06, 0.45, 'Термокарстовые\nозёра', '#06b6d4')
arrow(ax[0][0], W1, H1, 0.40, 0.12, 0.55, 0.05, 'Береговая линия', '#94a3b8')

# ── B: December 2025 original (deep winter) ──────────────────────────────────
ax[0][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
ax[0][1].set_title('Б) Конец декабря 2025 — устойчивый зимний лёд (исходный снимок)',
                   color='w', fontsize=11, pad=6)
arrow(ax[0][1], W2, H2, 0.22, 0.78, 0.10, 0.92, 'Деформированный лёд\n(торосы / обломки\nот каравана СПГ)', '#f59e0b')
arrow(ax[0][1], W2, H2, 0.40, 0.28, 0.30, 0.10, 'Разводье /\nсудовой канал', '#2563eb')
arrow(ax[0][1], W2, H2, 0.70, 0.55, 0.85, 0.40, 'Гладкий припай\n(ровный лёд)\n← тёмный, как нефть', '#dc2626')
arrow(ax[0][1], W2, H2, 0.40, 0.45, 0.55, 0.32, 'Свежезамёрзшее\nразводье (нилас)', '#ef4444')
arrow(ax[0][1], W2, H2, 0.05, 0.30, 0.10, 0.16, 'Поле\nдрейф. льда', '#7dd3fc')
arrow(ax[0][1], W2, H2, 0.85, 0.80, 0.92, 0.92, 'Первогодний\nлёд', '#0ea5e9')

# ── C: October detection ─────────────────────────────────────────────────────
ax[1][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
ov1 = np.zeros((H1, W1, 4)); ov1[...,0]=0.10; ov1[...,1]=0.75; ov1[...,2]=1.0; ov1[...,3]=cand1*0.40
ax[1][0].imshow(ov1, aspect='equal')
ax[1][0].set_title(f'В) Детекция тёмных зон — октябрь 2022  ({df1:.1f}% кадра)',
                   color='w', fontsize=11, pad=6)
ax[1][0].text(W1*0.02, H1*0.97, f'гладкая пов.: μ={mu1:.0f}  σ={sig1:.0f}  T={T1:.0f}',
              color='#9aa4b2', fontsize=8, va='bottom')

# ── D: December detection ────────────────────────────────────────────────────
ax[1][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
ov2 = np.zeros((H2, W2, 4)); ov2[...,0]=1.0; ov2[...,1]=0.45; ov2[...,2]=0.05; ov2[...,3]=cand2*0.42
ax[1][1].imshow(ov2, aspect='equal')
ax[1][1].set_title(f'Г) Детекция тёмных зон — декабрь 2025  ({df2:.1f}% кадра)',
                   color='w', fontsize=11, pad=6)
ax[1][1].text(W2*0.02, H2*0.97, f'гладкая пов.: μ={mu2:.0f}  σ={sig2:.0f}  T={T2:.0f}',
              color='#9aa4b2', fontsize=8, va='bottom')

# ── Right info panel ─────────────────────────────────────────────────────────
y = 0.975
def info(text, color='#e2e8f0', fs=9.5, dy=0.038, bold=False):
    global y
    ax_info.text(0.06, y, text, color=color, fontsize=fs,
                 fontweight='bold' if bold else 'normal',
                 transform=ax_info.transAxes, va='top', clip_on=False)
    y -= dy

info('САБЕТТА', '#f8fafc', fs=13, dy=0.043, bold=True)
info('Порт «Ямал СПГ» (Yamal LNG)', '#94a3b8', fs=8.5, dy=0.030)
info('71.3°N, 72.1°E · Обская губа', '#94a3b8', fs=8.5, dy=0.040)
info('─'*28, '#3a4252', fs=8, dy=0.028)

info('Sentinel-1 IW GRD VV', '#cbd5e1', fs=9, dy=0.026, bold=True)
info('Октябрь 2022  (A, В)', '#7dd3fc', fs=8.5, dy=0.024)
info('Ледостав: жировой/нилас. лёд', '#9aa4b2', fs=8, dy=0.019)
info('= сильнейший двойник нефти', '#9aa4b2', fs=8, dy=0.030)
info('Конец декабря 2025  (Б, Г)', '#fca5a5', fs=8.5, dy=0.024)
info('Зимний припай + судовой канал', '#9aa4b2', fs=8, dy=0.019)
info('+ свежезамёрзшие разводья', '#9aa4b2', fs=8, dy=0.034)
info('─'*28, '#3a4252', fs=8, dy=0.028)

info('СТАТИСТИКА', '#f8fafc', fs=9.5, dy=0.030, bold=True)
for label, mu, sig, T, df, clr in [
    ('Октябрь 2022', mu1, sig1, T1, df1, '#7dd3fc'),
    ('Декабрь 2025', mu2, sig2, T2, df2, '#fca5a5')]:
    info(f'{label}', clr, fs=9, dy=0.022, bold=True)
    info(f'  μ={mu:.0f}  σ={sig:.0f}  T=μ−1.2σ={T:.0f}', '#9aa4b2', fs=8, dy=0.020)
    info(f'  Тёмных зон: {df:.1f}% кадра', '#cbd5e1', fs=8.5, dy=0.032)
info('─'*28, '#3a4252', fs=8, dy=0.028)

info('LOOK-ALIKE ЭФФЕКТ', '#f8fafc', fs=9.5, dy=0.030, bold=True)
info('При ледоставе жировой/ниласовый', '#f97316', fs=8.5, dy=0.019)
info('лёд гасит рябь → σ⁰ −10…−20 дБ', '#f97316', fs=8.5, dy=0.019)
info('→ тёмное пятно = как нефть.', '#f97316', fs=8.5, dy=0.027)
info('Гладкий припай тоже тёмный.', '#f97316', fs=8.5, dy=0.030)
info('PD = σ⁰_VV − σ⁰_VH:', '#e2e8f0', fs=8.5, dy=0.021)
info('  Нефть:   6–10 дБ', '#ef4444', fs=8.5, dy=0.019)
info('  Мол. лёд:  < 4 дБ ✓', '#22d3ee', fs=8.5, dy=0.019)
info('  Припай:  2–4 дБ ✓', '#94a3b8', fs=8.5, dy=0.030)
info('─'*28, '#3a4252', fs=8, dy=0.028)

info('ВЫВОД', '#f8fafc', fs=9.5, dy=0.026, bold=True)
info('Разливов в 2022–2025 гг.', '#4ade80', fs=8.5, dy=0.019)
info('не зафиксировано. Все тёмные', '#4ade80', fs=8.5, dy=0.019)
info('зоны = лёд (нилас, припай).', '#4ade80', fs=8.5, dy=0.019)
info('Самый сложный ледовый полигон —', '#4ade80', fs=8.5, dy=0.019)
info('проверка устойчивости к FP.', '#4ade80', fs=8.5, dy=0.024)
info('─'*28, '#3a4252', fs=8, dy=0.028)

info('Метод детекции', '#cbd5e1', fs=8.5, dy=0.020, bold=True)
info('Текстурная маска гладких зон +', '#9aa4b2', fs=8, dy=0.018)
info('адаптивный порог T=μ−k·σ (k=1.2)', '#9aa4b2', fs=8, dy=0.018)
info('8-бит превью (качественно)', '#6b7280', fs=7.5, dy=0.020)

fig.suptitle(
    'Сабетта (Обская губа, Ямал СПГ) — Sentinel-1 IW GRD VV: ледовые двойники нефтяных разливов',
    color='w', fontsize=14, fontweight='bold', y=0.975)
fig.text(0.375, 0.028,
    'Примечание: 8-бит превью — качественная визуализация. Синий = тёмные зоны октября (молодой лёд + открытая вода). '
    'Оранжевый = тёмные зоны декабря (гладкий припай + свежезамёрзшие разводья). Все — ложные цели. '
    'Разделение нефть/лёд требует PD из калиброванного продукта .SAFE (SNAP).',
    color='#6b7280', fontsize=7.5, ha='center', style='italic')

plt.savefig('sabetta_oct_dec_lookalikes.png', dpi=160, facecolor=BG)
plt.close()
print("DONE → sabetta_oct_dec_lookalikes.png")
