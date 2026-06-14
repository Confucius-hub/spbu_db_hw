import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
from sar_style import load_rgb, style_axes, panel_label, COL, GRID

BASE = '/home/user/spbu_db_hw/thesis/sar_norilsk_2020'
OUT  = '/home/user/spbu_db_hw/thesis/otchet/figures'

a1 = load_rgb(f'{BASE}/sentinel1_norilsk_03jun2020_falsecolor.webp')
a2 = load_rgb(f'{BASE}/sentinel1_norilsk_15jun2020_falsecolor.webp')
H1,W1 = a1.shape[:2]; H2,W2 = a2.shape[:2]

def arrow(ax, W, H, fx, fy, tx, ty, txt, col, fs=8.5):
    ax.add_patch(FancyArrowPatch((tx*W,ty*H),(fx*W,fy*H), arrowstyle='-|>',
        mutation_scale=12, color=col, lw=1.5, shrinkA=0, shrinkB=2))
    ax.text(tx*W, ty*H, txt, color='black', fontsize=fs, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=col, lw=1.3, alpha=0.95))

fig = plt.figure(figsize=(13, 6.2), facecolor='white')
gs = gridspec.GridSpec(1,2, figure=fig, left=0.012, right=0.988,
                       top=0.92, bottom=0.10, wspace=0.03)
axA = fig.add_subplot(gs[0,0]); axB = fig.add_subplot(gs[0,1])
for ax_ in (axA,axB): style_axes(ax_)

# ── а) 3 June 2020 ──
axA.imshow(a1, aspect='equal')
axA.set_title('3 июня 2020 (+5 сут. после аварии)', color='black', fontsize=10.5, pad=4)
panel_label(axA, 'а)')
arrow(axA, W1,H1, 0.17,0.62, 0.07,0.46, 'оз. Пясино\n(вода)', COL['water'])
arrow(axA, W1,H1, 0.36,0.60, 0.30,0.40, 'дельта р. Амбарной\n(вход стока)', COL['oil'])
arrow(axA, W1,H1, 0.40,0.24, 0.52,0.10, 'р. Норильская', COL['sky'])
arrow(axA, W1,H1, 0.75,0.66, 0.89,0.45, 'плато Путорана\n(рельеф)', COL['land'])
arrow(axA, W1,H1, 0.10,0.22, 0.06,0.08, 'тундра', COL['veg'])

# ── б) 15 June 2020 ──
axB.imshow(a2, aspect='equal')
axB.set_title('15 июня 2020 (+17 сут. после аварии)', color='black', fontsize=10.5, pad=4)
panel_label(axB, 'б)')
arrow(axB, W2,H2, 0.17,0.64, 0.07,0.48, 'оз. Пясино', COL['water'])
arrow(axB, W2,H2, 0.37,0.60, 0.30,0.40, 'дельта р. Амбарной', COL['oil'])
arrow(axB, W2,H2, 0.75,0.66, 0.89,0.46, 'плато Путорана', COL['land'])

fig.suptitle('Бассейн оз. Пясино (Sentinel-1 IW GRD, RGB-композит R=VV, G=VH, B=VV/VH; 10 м/пикс)',
             color='black', fontsize=10.5, y=0.985)

# legend
handles = [Line2D([0],[0], marker='o', color='w', markerfacecolor=c,
                  markeredgecolor=GRID, markersize=9, label=l) for c,l in
           [(COL['water'],'вода (низкий сигнал)'),(COL['veg'],'тундра/растительность'),
            (COL['land'],'рельеф (VV > VH)'),(COL['oil'],'дельта Амбарной — путь стока')]]
fig.legend(handles=handles, loc='lower center', ncol=4, frameon=False, fontsize=8.5,
           bbox_to_anchor=(0.5, 0.005), handletextpad=0.4, columnspacing=1.6)
fig.savefig(f'{OUT}/fig_norilsk.png', dpi=150, facecolor='white')
plt.close()
print('fig_norilsk.png DONE')
