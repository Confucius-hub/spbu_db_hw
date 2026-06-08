import sys, os
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

# Иллюстративный Sentinel-1 VV кадр Кольского залива (в стиле выхода модели).
H, W = 760, 900
yy, xx = np.mgrid[0:H, 0:W].astype(float)
axis_x = 0.46*W + 0.10*W*np.sin(yy/H*np.pi*1.15) + 0.05*W*(yy/H)
half = 0.085*W + 0.045*W*np.sin(yy/H*np.pi*0.8)
bay = np.abs(xx - axis_x) < half

img = np.full((H, W), 128.0)
img += gaussian_filter(rng.normal(0, 22, (H, W)), 2.0)
img[bay] = 84.0
img += gaussian_filter(rng.normal(0, 6, (H, W)), 1.2)

cy, cx = 0.60*H, axis_x[int(0.60*H), 0]
el = (((xx-cx)/(0.060*W))**2 + ((yy-cy)/(0.165*H))**2)
spill = (el < 1.0) & bay
tail = (((xx-cx+0.035*W)/(0.10*W))**2 + ((yy-cy-0.10*H)/(0.07*H))**2 < 1.0) & bay
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

# ── рисунок (крупнее и контрастнее под проекцию) ────────────────────────────
fig = plt.figure(figsize=(13.0, 5.8), facecolor='white')
gs = gridspec.GridSpec(1, 2, figure=fig, left=0.006, right=0.994,
                       top=0.905, bottom=0.115, wspace=0.025)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
for ax in (axL, axR):
    style_axes(ax)

axL.imshow(a, cmap='gray', vmin=0, vmax=255, aspect='equal')
axL.set_title('Исходный снимок Sentinel-1 (VV), Кольский залив, 18.08.2024',
              color='black', fontsize=14, pad=6, fontweight='bold')
panel_label(axL, 'а)')
arrow(axL, W, H, 0.18, 0.20, 0.07, 0.10, 'Кольский п-ов\n(суша)', COL['land'], fs=12)
arrow(axL, W, H, 0.86, 0.40, 0.965, 0.27, 'Мурманск,\nпорт', COL['infra'], fs=12)
arrow(axL, W, H, 0.50, 0.30, 0.66, 0.12, 'Акватория\n(вода)', COL['water'], fs=12)
arrow(axL, W, H, 0.52, 0.60, 0.27, 0.76, 'Тёмное пятно\n← нефть', COL['oil'], fs=12)

axR.imshow(a, cmap='gray', vmin=0, vmax=255, aspect='equal')
overlay(axR, mask, H, W, (0.80, 0.18, 0.12), 0.55)
axR.set_title(f'Результат сегментации: нефть — {df_water:.0f} % акватории',
              color='black', fontsize=14, pad=6, fontweight='bold')
panel_label(axR, 'б)')
axR.text(0.015*W, 0.985*H,
         f'μ={mu:.0f}  σ={sigma:.0f}  порог T=μ−1.3σ={T:.0f} (дБ-уровни)',
         color='black', fontsize=11, va='bottom', ha='left',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=GRID, lw=0.7, alpha=0.92))
axR.text(0.985*W, 0.985*H,
         'Верификация: ERA5 ветер 4.8 м/с  •  AIS судно ≤ 5 км / ≤ 24 ч',
         color='black', fontsize=10.5, va='bottom', ha='right',
         bbox=dict(boxstyle='round,pad=0.3', fc='#f0fff4', ec=COL['veg'],
                   lw=1.1, alpha=0.95))

legend = [(COL['land'], 'суша'), (COL['water'], 'вода'),
          (COL['infra'], 'порт / застройка'),
          ((0.80, 0.18, 0.12), 'нефть (выход модели)')]
handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=c,
                  markeredgecolor=GRID, markersize=12, label=l) for c, l in legend]
fig.legend(handles=handles, loc='lower center', ncol=len(legend),
           frameon=False, fontsize=11.5, bbox_to_anchor=(0.5, 0.008),
           handletextpad=0.4, columnspacing=2.0)

fig.savefig(f'{OUT}/fig_kola_slide.png', dpi=200, facecolor='white')
plt.close()
print(f'fig_kola_slide.png: spill={df_water:.1f}% of water')
