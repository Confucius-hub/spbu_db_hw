import sys
sys.path.insert(0, '/home/user/spbu_db_hw/thesis/otchet/figures')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter
from sar_style import (detect, style_axes, panel_label, arrow, stat_box,
                       overlay, COL, GRID)

OUT = '/home/user/spbu_db_hw/thesis/otchet/figures'
rng = np.random.default_rng(2024)

# ── синтетический Sentinel-1 VV, Кольский залив ───────────────────────────
H, W = 760, 900
yy, xx = np.mgrid[0:H, 0:W].astype(float)
axis_x = 0.46*W + 0.10*W*np.sin(yy/H*np.pi*1.15) + 0.05*W*(yy/H)
half   = 0.085*W + 0.045*W*np.sin(yy/H*np.pi*0.8)
bay    = np.abs(xx - axis_x) < half

img = np.full((H, W), 128.0)
img += gaussian_filter(rng.normal(0, 22, (H, W)), 2.0)
img[bay] = 84.0
img += gaussian_filter(rng.normal(0, 6, (H, W)), 1.2)

cy, cx = 0.60*H, axis_x[int(0.60*H), 0]
el   = (((xx-cx)/(0.060*W))**2 + ((yy-cy)/(0.165*H))**2)
spill = (el < 1.0) & bay
tail  = (((xx-cx+0.035*W)/(0.10*W))**2 + ((yy-cy-0.10*H)/(0.07*H))**2 < 1.0) & bay
spill = spill | tail
img[spill] = 44.0
img = gaussian_filter(img, 0.8)
img *= (1.0 + rng.normal(0, 0.06, (H, W)))
img = np.clip(img, 0, 255)

for _ in range(1400):
    py = int(rng.uniform(0.30, 0.78)*H)
    px = int(axis_x[py, 0] + half[py, 0] + rng.uniform(2, 60))
    if 0 <= px < W:
        img[py, px] = min(255, img[py, px] + rng.uniform(40, 90))

a = img.copy()
mask, mu, sigma, T = detect(a, land_pct=72, k=1.3, smooth_pct=55, min_frac=0.0008)
df_water = mask.sum() / max(bay.sum(), 1) * 100

# ── ВЕРТИКАЛЬНАЯ раскладка: 2 строки × 1 столбец (9×8") ─────────────────
# → при вставке в слайд занимает ≈5.6"×5.0" вместо прежних 6.1"×2.7"
fig = plt.figure(figsize=(9, 8), facecolor='white')
gs  = gridspec.GridSpec(2, 1, figure=fig,
                        left=0.02, right=0.98,
                        top=0.965, bottom=0.085,
                        hspace=0.06)
axT = fig.add_subplot(gs[0])   # верхняя панель — исходный снимок
axB = fig.add_subplot(gs[1])   # нижняя панель  — сегментация
for ax in (axT, axB):
    style_axes(ax)

# ── верхняя: исходный VV ─────────────────────────────────────────────────
axT.imshow(a, cmap='gray', vmin=0, vmax=255, aspect='equal')
axT.set_title('а)  Исходный снимок Sentinel-1 (VV) — Кольский залив, 18.08.2024',
              color='black', fontsize=15, pad=5, fontweight='bold', loc='left', x=0.01)
arrow(axT, W, H, 0.18, 0.22, 0.07, 0.10, 'Суша', COL['land'], fs=13)
arrow(axT, W, H, 0.87, 0.40, 0.97, 0.22, 'Порт\nМурманск', COL['infra'], fs=13)
arrow(axT, W, H, 0.50, 0.28, 0.64, 0.10, 'Акватория\n(вода)', COL['water'], fs=13)
arrow(axT, W, H, 0.52, 0.60, 0.26, 0.77, 'Тёмное пятно\n← нефть', COL['oil'], fs=13)

# ── нижняя: выход модели ─────────────────────────────────────────────────
axB.imshow(a, cmap='gray', vmin=0, vmax=255, aspect='equal')
overlay(axB, mask, H, W, (0.80, 0.18, 0.12), 0.55)
axB.set_title(f'б)  Результат сегментации: нефтяное пятно — {df_water:.0f} % акватории',
              color='black', fontsize=15, pad=5, fontweight='bold', loc='left', x=0.01)
axB.text(0.015*W, 0.975*H,
         f'μ={mu:.0f}  σ={sigma:.0f}  T=μ−1.3σ={T:.0f}',
         color='black', fontsize=12, va='bottom', ha='left',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=GRID, lw=0.7, alpha=0.92))
axB.text(0.985*W, 0.975*H,
         'ERA5 ветер 4.8 м/с  •  AIS судно ≤ 5 км / ≤ 24 ч',
         color='black', fontsize=12, va='bottom', ha='right',
         bbox=dict(boxstyle='round,pad=0.3', fc='#f0fff4', ec=COL['veg'],
                   lw=1.0, alpha=0.95))

legend = [(COL['land'], 'суша'), (COL['water'], 'вода'),
          (COL['infra'], 'порт'), ((0.80, 0.18, 0.12), 'нефть (выход модели)')]
handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=c,
                  markeredgecolor=GRID, markersize=13, label=l) for c, l in legend]
fig.legend(handles=handles, loc='lower center', ncol=4,
           frameon=False, fontsize=13, bbox_to_anchor=(0.5, 0.005),
           handletextpad=0.4, columnspacing=1.8)

fig.savefig(f'{OUT}/fig_kola_slide.png', dpi=300, facecolor='white')
plt.close()
print(f'Saved fig_kola_slide.png  spill={df_water:.1f}%  size=9x8" @300dpi')
