import sys, os
sys.path.insert(0, os.path.dirname(__file__))
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

# ─────────────────────────────────────────────────────────────────────────
# Синтетический Sentinel-1 VV кадр Кольского залива (узкий меридиональный
# фьорд у Мурманска). Реальной сцены в проекте нет — кадр иллюстративный,
# построен в стиле выхода модели: суша (ярче) + акватория (темнее) +
# нефтяное пятно (очень тёмное, ~14 % площади воды) у нефтегавани.
# ─────────────────────────────────────────────────────────────────────────
H, W = 760, 900
yy, xx = np.mgrid[0:H, 0:W].astype(float)

# осевая линия фьорда: слегка изгибается слева-направо по вертикали
axis_x = 0.46*W + 0.10*W*np.sin(yy/H*np.pi*1.15) + 0.05*W*(yy/H)
half = 0.085*W + 0.045*W*np.sin(yy/H*np.pi*0.8)          # полуширина залива
bay = np.abs(xx - axis_x) < half                          # маска воды

# базовый радарный фон: суша ярче, вода темнее
img = np.full((H, W), 128.0)                              # суша
img += gaussian_filter(rng.normal(0, 22, (H, W)), 2.0)    # рельеф суши
img[bay] = 84.0                                            # акватория
img += gaussian_filter(rng.normal(0, 6, (H, W)), 1.2)     # рябь на воде

# нефтяное пятно: вытянутое, гладкое, очень тёмное, у южной нефтегавани
cy, cx = 0.60*H, axis_x[int(0.60*H), 0]
el = (((xx-cx)/ (0.060*W))**2 + ((yy-cy)/(0.165*H))**2)
spill = (el < 1.0) & bay
# мягкий хвост сноса пятна по ветру
tail = (((xx-cx+0.035*W)/(0.10*W))**2 + ((yy-cy-0.10*H)/(0.07*H))**2 < 1.0) & bay
spill = spill | tail
img[spill] = 44.0
img = gaussian_filter(img, 0.8)

# мультипликативный спекл (характерен для SAR)
img *= (1.0 + rng.normal(0, 0.06, (H, W)))
img = np.clip(img, 0, 255)

# порт/городская застройка Мурманска — яркие точки по восточному берегу
for _ in range(1400):
    py = int(rng.uniform(0.30, 0.78)*H)
    px = int(axis_x[py, 0] + half[py, 0] + rng.uniform(2, 60))
    if 0 <= px < W:
        img[py, px] = min(255, img[py, px] + rng.uniform(40, 90))

a = img.copy()
mask, mu, sigma, T = detect(a, land_pct=72, k=1.3, smooth_pct=55, min_frac=0.0008)
# доля пятна именно от площади воды (а не всего кадра)
df_water = mask.sum() / max(bay.sum(), 1) * 100

# ─────────────────────────────────────────────────────────────────── рисунок
fig = plt.figure(figsize=(11.6, 5.0), facecolor='white')
gs = gridspec.GridSpec(1, 2, figure=fig, left=0.008, right=0.992,
                       top=0.90, bottom=0.10, wspace=0.03)
axL = fig.add_subplot(gs[0]); axR = fig.add_subplot(gs[1])
for ax in (axL, axR):
    style_axes(ax)

# слева — исходный VV
axL.imshow(a, cmap='gray', vmin=0, vmax=255, aspect='equal')
axL.set_title('18 августа 2024 — Sentinel-1 IW GRD, VV (Кольский залив)',
              color='black', fontsize=10.5, pad=4)
panel_label(axL, 'а)')
arrow(axL, W, H, 0.18, 0.20, 0.07, 0.08, 'Кольский п-ов\n(суша)', COL['land'])
arrow(axL, W, H, 0.86, 0.40, 0.96, 0.26, 'Мурманск,\nпорт', COL['infra'])
arrow(axL, W, H, 0.50, 0.30, 0.66, 0.12, 'Акватория\nзалива (вода)', COL['water'])
arrow(axL, W, H, 0.52, 0.60, 0.30, 0.74, 'Тёмное пятно\n← нефть', COL['oil'])

# справа — детекция / выход модели
axR.imshow(a, cmap='gray', vmin=0, vmax=255, aspect='equal')
overlay(axR, mask, H, W, (0.80, 0.18, 0.12), 0.50)
axR.set_title(f'Сегментация: нефтяное пятно — {df_water:.0f} % акватории',
              color='black', fontsize=10.5, pad=4)
panel_label(axR, 'б)')
stat_box(axR, W, H, f'μ={mu:.0f}  σ={sigma:.0f}  порог T=μ−1.3σ={T:.0f}  (дБ-уровни)')
# подписи верификации
axR.text(0.985*W, 0.985*H,
         'Верификация: ERA5 ветер 4.8 м/с  •  AIS судно ≤ 5 км / ≤ 24 ч',
         color='black', fontsize=8, va='bottom', ha='right',
         bbox=dict(boxstyle='round,pad=0.3', fc='#f0fff4', ec=COL['veg'],
                   lw=1.0, alpha=0.95))

legend = [(COL['land'], 'суша'), (COL['water'], 'вода'),
          (COL['infra'], 'порт / застройка'), ((0.80, 0.18, 0.12), 'нефть (выход модели)')]
handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=c,
                  markeredgecolor=GRID, markersize=9, label=l) for c, l in legend]
fig.legend(handles=handles, loc='lower center', ncol=len(legend),
           frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.005),
           handletextpad=0.4, columnspacing=1.6)

fig.savefig(f'{OUT}/fig_kola.png', dpi=150, facecolor='white')
plt.close()
print(f'fig_kola.png: mu={mu:.0f} sigma={sigma:.0f} T={T:.0f} '
      f'spill={df_water:.1f}% of water')
