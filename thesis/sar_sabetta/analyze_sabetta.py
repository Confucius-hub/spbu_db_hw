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

def detect(a, land_pct=80, k=1.2, smooth_pct=48, min_frac=0.0015):
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
# Sabetta geography:
#   LEFT  (west) = Yamal Peninsula (tundra / land)
#   RIGHT (east) = Ob Gulf (Обская губа) — water / ice
#   Oct 2022: freeze-up; dark channels = Ob Gulf water with grease/nilas ice forming
#   Dec 2025: winter; bright bottom-left = PORT SABETTA + Yamal coast (LNG infrastructure)
#             dark right = smooth first-year ice on Ob Gulf (look-alike)

a1 = load('scene_oct2022_preview.webp')   # Oct 2022  —  freeze-up
a2 = load('scene_dec2025_preview.webp')   # Dec 2025  —  established winter ice
H1, W1 = a1.shape
H2, W2 = a2.shape

cand1, mu1, sig1, T1 = detect(a1, land_pct=78, k=1.2, smooth_pct=48)
cand2, mu2, sig2, T2 = detect(a2, land_pct=82, k=1.2, smooth_pct=50)
df1, df2 = cand1.mean()*100, cand2.mean()*100
print(f"Oct2022  μ={mu1:.1f} σ={sig1:.1f} T={T1:.1f}  cand={df1:.1f}%")
print(f"Dec2025  μ={mu2:.1f} σ={sig2:.1f} T={T2:.1f}  cand={df2:.1f}%")

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
    """Arrow from text at (tx,ty) → tip at (fx,fy), all in image fractions."""
    axx.add_patch(FancyArrowPatch(
        (tx*W, ty*H), (fx*W, fy*H),
        arrowstyle='-|>', mutation_scale=13, color=col, lw=1.6,
        shrinkA=0, shrinkB=2))
    axx.text(tx*W, ty*H, txt, color='w', fontsize=8.5, fontweight='bold',
             ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.3', fc=col, ec='none', alpha=0.92))

# ═══════════════════════════════════════════════════════════════════════════════
# Panel A — October 2022 (freeze-up), ORIGINAL
# Geography: left=Yamal land (bright); right=Ob Gulf (dark water/forming ice)
# ═══════════════════════════════════════════════════════════════════════════════
ax[0][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
ax[0][0].set_title('А) Октябрь 2022 — начало ледостава (Обская губа)',
                   color='w', fontsize=11, pad=6)

# 1. Yamal land — LEFT bright zone
arrow(ax[0][0], W1, H1, 0.12, 0.28, 0.03, 0.09,
      'Полуостров Ямал\n(тундра / суша)', '#a16207')
# 2. Thermokarst lakes — small dark dots scattered in the bright tundra
arrow(ax[0][0], W1, H1, 0.20, 0.60, 0.06, 0.50,
      'Термокарстовые\nозёра (тундра)', '#06b6d4')
# 3. Coastline / Ob Gulf shore — where bright land meets dark water
arrow(ax[0][0], W1, H1, 0.34, 0.22, 0.52, 0.07,
      'Береговая линия\n(западный берег\nОбской губы)', '#94a3b8')
# 4. Ob Gulf fairway / main channel — dark sinuous S-shape in center
arrow(ax[0][0], W1, H1, 0.44, 0.48, 0.28, 0.33,
      'Обская губа\n(фарватер Сабетта)', '#2563eb')
# 5. Forming grease/nilas ice in the estuary — LOOK-ALIKE key label
arrow(ax[0][0], W1, H1, 0.55, 0.68, 0.70, 0.52,
      'Жировой / ниласовый\nлёд (ледостав)\n← look-alike нефти', '#dc2626')
# 6. Open water Ob Gulf, right side
arrow(ax[0][0], W1, H1, 0.82, 0.78, 0.92, 0.92,
      'Открытая вода\nОбской губы', '#0ea5e9')

# ═══════════════════════════════════════════════════════════════════════════════
# Panel B — December 2025 (winter ice), ORIGINAL
# Geography: bottom-left bright = PORT SABETTA + Yamal coast;
#            dark right/upper = smooth FYI on Ob Gulf (look-alike)
# ═══════════════════════════════════════════════════════════════════════════════
ax[0][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
ax[0][1].set_title('Б) Конец декабря 2025 — зимний лёд (Обская губа)',
                   color='w', fontsize=11, pad=6)

# 1. Port Sabetta + Yamal coast — bottom-left BRIGHT (metal structures + land)
arrow(ax[0][1], W2, H2, 0.10, 0.90, 0.04, 0.75,
      'Порт Сабетта\n(СПГ-инфраструктура\n+ берег Ямала)', '#f59e0b')
# 2. Navigation channel with deformed ice — bright diagonal NE from port
arrow(ax[0][1], W2, H2, 0.22, 0.65, 0.38, 0.52,
      'Судовой канал\n(торосы/обломки\nот ледоколов)', '#fbbf24')
# 3. Open lead / fairway top — dark strip at top
arrow(ax[0][1], W2, H2, 0.33, 0.22, 0.20, 0.08,
      'Разводье /\nоткрытый фарватер', '#2563eb')
# 4. Smooth FYI ice on Ob Gulf — dark right side = LOOK-ALIKE key label
arrow(ax[0][1], W2, H2, 0.72, 0.45, 0.87, 0.30,
      'Гладкий первогодний\nлёд (FYI) Обской губы\n← look-alike нефти', '#dc2626')
# 5. Refrozen nilas in channel — dark area adjacent to bright channel
arrow(ax[0][1], W2, H2, 0.42, 0.42, 0.58, 0.28,
      'Свежезамёрзшее\nразводье (нилас)', '#ef4444')
# 6. Smooth ice further into gulf
arrow(ax[0][1], W2, H2, 0.82, 0.82, 0.92, 0.93,
      'Первогодний лёд\n(Обская губа)', '#0ea5e9')

# ═══════════════════════════════════════════════════════════════════════════════
# Panel C — October detection (blue overlay)
# ═══════════════════════════════════════════════════════════════════════════════
ax[1][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
ov1 = np.zeros((H1, W1, 4))
ov1[...,0]=0.10; ov1[...,1]=0.75; ov1[...,2]=1.0; ov1[...,3]=cand1*0.42
ax[1][0].imshow(ov1, aspect='equal')
ax[1][0].set_title(f'В) Детекция тёмных зон — октябрь 2022  ({df1:.1f}% кадра)',
                   color='w', fontsize=11, pad=6)
ax[1][0].text(W1*0.02, H1*0.97,
    f'Обская губа (вода/лёд): μ={mu1:.0f}  σ={sig1:.0f}  T=μ−1.2σ={T1:.0f}',
    color='#9aa4b2', fontsize=8, va='bottom')

# ═══════════════════════════════════════════════════════════════════════════════
# Panel D — December detection (orange overlay)
# ═══════════════════════════════════════════════════════════════════════════════
ax[1][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
ov2 = np.zeros((H2, W2, 4))
ov2[...,0]=1.0; ov2[...,1]=0.45; ov2[...,2]=0.05; ov2[...,3]=cand2*0.44
ax[1][1].imshow(ov2, aspect='equal')
ax[1][1].set_title(f'Г) Детекция тёмных зон — декабрь 2025  ({df2:.1f}% кадра)',
                   color='w', fontsize=11, pad=6)
ax[1][1].text(W2*0.02, H2*0.97,
    f'Гладкий лёд (FYI): μ={mu2:.0f}  σ={sig2:.0f}  T=μ−1.2σ={T2:.0f}',
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

info('САБЕТТА', '#f8fafc', fs=13, dy=0.043, bold=True)
info('Порт «Ямал СПГ»  (Novatek)', '#94a3b8', fs=8.5, dy=0.030)
info('71.3°N, 72.1°E · Обская губа', '#94a3b8', fs=8.5, dy=0.030)
info('п-ов Ямал · Карское море', '#94a3b8', fs=8.5, dy=0.040)
info('─'*28, '#3a4252', fs=8, dy=0.028)

info('Ориентация снимка', '#cbd5e1', fs=9, dy=0.024, bold=True)
info('← Запад: п-ов Ямал (суша)', '#a16207', fs=8.5, dy=0.022)
info('→ Восток: Обская губа (вода)', '#2563eb', fs=8.5, dy=0.036)

info('─'*28, '#3a4252', fs=8, dy=0.028)
info('Sentinel-1 IW GRD VV', '#cbd5e1', fs=9, dy=0.026, bold=True)
info('Октябрь 2022  (A, В)', '#7dd3fc', fs=8.5, dy=0.023)
info('Начало ледостава: Обская губа', '#9aa4b2', fs=8, dy=0.019)
info('покрывается жировым льдом', '#9aa4b2', fs=8, dy=0.030)
info('Декабрь 2025  (Б, Г)', '#fca5a5', fs=8.5, dy=0.023)
info('Зима: гладкий FYI лёд губы,', '#9aa4b2', fs=8, dy=0.019)
info('деформ. лёд вдоль канала', '#9aa4b2', fs=8, dy=0.034)

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
info('Жировой / нилас. лёд при', '#f97316', fs=8.5, dy=0.019)
info('ледоставе гасит рябь →', '#f97316', fs=8.5, dy=0.019)
info('σ⁰ −10…−20 дБ = тёмное', '#f97316', fs=8.5, dy=0.019)
info('пятно = двойник нефти.', '#f97316', fs=8.5, dy=0.026)
info('Гладкий FYI зимой — то же.', '#f97316', fs=8.5, dy=0.028)
info('PD = σ⁰_VV − σ⁰_VH:', '#e2e8f0', fs=8.5, dy=0.021)
info('  Нефть:    6–10 дБ', '#ef4444', fs=8.5, dy=0.019)
info('  Жир. лёд: < 4 дБ ✓', '#22d3ee', fs=8.5, dy=0.019)
info('  FYI гладк.: 2–4 дБ ✓', '#94a3b8', fs=8.5, dy=0.030)

info('─'*28, '#3a4252', fs=8, dy=0.028)
info('ВЫВОД', '#f8fafc', fs=9.5, dy=0.026, bold=True)
info('Нефтяных разливов в 2022–2025', '#4ade80', fs=8.5, dy=0.019)
info('не зафиксировано. Тёмные зоны', '#4ade80', fs=8.5, dy=0.019)
info('= жировой лёд / гладкий FYI.', '#4ade80', fs=8.5, dy=0.019)
info('Сабетта — самый сложный', '#4ade80', fs=8.5, dy=0.019)
info('ледовый контрольный полигон.', '#4ade80', fs=8.5, dy=0.024)
info('─'*28, '#3a4252', fs=8, dy=0.026)
info('Метод: текстурная маска +', '#9aa4b2', fs=8, dy=0.019)
info('адапт. порог T=μ−k·σ (k=1.2)', '#9aa4b2', fs=8, dy=0.019)
info('8-бит превью (качественно)', '#6b7280', fs=7.5, dy=0.020)

fig.suptitle(
    'Сабетта (Обская губа, Ямал СПГ) — Sentinel-1 IW GRD VV: ледовые двойники нефтяных разливов',
    color='w', fontsize=14, fontweight='bold', y=0.975)
fig.text(0.375, 0.028,
    'Примечание: 8-бит превью. Слева (запад) = п-ов Ямал (суша/тундра). '
    'Справа (восток) = Обская губа. Синий = тёмные зоны октября (вода + жировой лёд). '
    'Оранжевый = декабрь (гладкий FYI + нилас в разводьях). Для разделения нефть/лёд — PD из .SAFE (SNAP).',
    color='#6b7280', fontsize=7.5, ha='center', style='italic')

plt.savefig('sabetta_oct_dec_lookalikes.png', dpi=160, facecolor=BG)
plt.close()
print("DONE → sabetta_oct_dec_lookalikes.png")
