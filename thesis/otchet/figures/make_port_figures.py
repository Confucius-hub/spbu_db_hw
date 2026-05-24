import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
from sar_style import (load, detect, style_axes, panel_label, arrow, stat_box,
                       overlay, COL, GRID)

BASE = '/home/user/spbu_db_hw/thesis'
OUT  = '/home/user/spbu_db_hw/thesis/otchet/figures'

def four_panel(name, srcA, srcB, titleA, titleB, annsA, annsB,
               paramsA, paramsB, legend, ovA=(0.12,0.45,0.85), ovB=(0.80,0.30,0.10)):
    a1 = load(srcA); a2 = load(srcB)
    H1,W1 = a1.shape; H2,W2 = a2.shape
    c1,mu1,s1,T1 = detect(a1, **paramsA)
    c2,mu2,s2,T2 = detect(a2, **paramsB)
    df1,df2 = c1.mean()*100, c2.mean()*100

    fig = plt.figure(figsize=(13, 10.4), facecolor='white')
    gs = gridspec.GridSpec(2,2, figure=fig, left=0.012, right=0.988,
                           top=0.965, bottom=0.072, wspace=0.03, hspace=0.07)
    ax = [[fig.add_subplot(gs[r,c]) for c in range(2)] for r in range(2)]
    for row in ax:
        for a_ in row: style_axes(a_)

    # A — original A
    ax[0][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
    ax[0][0].set_title(titleA, color='black', fontsize=10.5, pad=4)
    panel_label(ax[0][0], 'а)')
    for (fx,fy,tx,ty,t,c) in annsA: arrow(ax[0][0],W1,H1,fx,fy,tx,ty,t,c)

    # B — original B
    ax[0][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
    ax[0][1].set_title(titleB, color='black', fontsize=10.5, pad=4)
    panel_label(ax[0][1], 'б)')
    for (fx,fy,tx,ty,t,c) in annsB: arrow(ax[0][1],W2,H2,fx,fy,tx,ty,t,c)

    # C — detection A
    ax[1][0].imshow(a1, cmap='gray', vmin=0, vmax=255, aspect='equal')
    overlay(ax[1][0], c1, H1, W1, ovA, 0.42)
    ax[1][0].set_title(f'Детекция тёмных зон — {df1:.1f}% кадра',
                       color='black', fontsize=10.5, pad=4)
    panel_label(ax[1][0], 'в)')
    stat_box(ax[1][0], W1, H1, f'μ={mu1:.0f}  σ={s1:.0f}  T=μ−{paramsA.get("k",1.3)}σ={T1:.0f}')

    # D — detection B
    ax[1][1].imshow(a2, cmap='gray', vmin=0, vmax=255, aspect='equal')
    overlay(ax[1][1], c2, H2, W2, ovB, 0.44)
    ax[1][1].set_title(f'Детекция тёмных зон — {df2:.1f}% кадра',
                       color='black', fontsize=10.5, pad=4)
    panel_label(ax[1][1], 'г)')
    stat_box(ax[1][1], W2, H2, f'μ={mu2:.0f}  σ={s2:.0f}  T=μ−{paramsB.get("k",1.3)}σ={T2:.0f}')

    # legend strip
    handles = [Line2D([0],[0], marker='o', color='w', markerfacecolor=c,
                      markeredgecolor=GRID, markersize=9, label=l) for c,l in legend]
    fig.legend(handles=handles, loc='lower center', ncol=len(legend),
               frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.006),
               handletextpad=0.4, columnspacing=1.4)
    fig.savefig(f'{OUT}/{name}', dpi=150, facecolor='white')
    plt.close()
    print(f'{name}: A μ={mu1:.0f} σ={s1:.0f} T={T1:.0f} {df1:.1f}% | B μ={mu2:.0f} σ={s2:.0f} T={T2:.0f} {df2:.1f}%')
    return dict(mu1=mu1,s1=s1,T1=T1,df1=df1,mu2=mu2,s2=s2,T2=T2,df2=df2)

# ════════════════════════════════ ПЕЧЕНГА ════════════════════════════════
# wind-shadow + biogenic look-alikes; winter (Feb 2026) + summer (Aug 2025)
pech = four_panel(
    'fig_pechenga.png',
    f'{BASE}/sar_pechenga/pechenga_feb2026_winter_VV.webp',
    f'{BASE}/sar_pechenga/pechenga_aug2025_summer_VV.webp',
    'Февраль 2026 — зима (Sentinel-1, VV)',
    'Август 2025 — лето (Sentinel-1, VV)',
    annsA=[
        (0.30,0.12, 0.16,0.05, 'Сопки\n(суша)', COL['land']),
        (0.55,0.40, 0.70,0.22, 'Акватория\nзалива (вода)', COL['water']),
        (0.45,0.62, 0.30,0.78, 'Ветровая тень\n← look-alike', COL['oil']),
        (0.10,0.80, 0.05,0.92, 'Берег', COL['coast']),
    ],
    annsB=[
        (0.78,0.18, 0.90,0.06, 'Полуостров\n(суша)', COL['land']),
        (0.40,0.30, 0.22,0.16, 'Береговая линия', COL['coast']),
        (0.45,0.65, 0.62,0.80, 'Биогенная плёнка /\nштилевая зона\n← look-alike', COL['oil']),
        (0.20,0.55, 0.07,0.42, 'Открытая\nвода', COL['water']),
    ],
    paramsA=dict(land_pct=78, k=1.3, smooth_pct=50),
    paramsB=dict(land_pct=80, k=1.3, smooth_pct=48),
    legend=[(COL['land'],'суша'),(COL['water'],'вода'),(COL['coast'],'берег'),
            (COL['oil'],'тёмная зона (look-alike)')],
    ovA=(0.12,0.45,0.85), ovB=(0.80,0.30,0.10))

# ════════════════════════════════ ВАРАНДЕЙ ═══════════════════════════════
# left=tundra(land), right=Pechora Sea; May 2025 breakup + Apr 2025 winter
vara = four_panel(
    'fig_varandey.png',
    f'{BASE}/sar_varandey/scene_may2025_preview.webp',
    f'{BASE}/sar_varandey/scene_apr2025_preview.webp',
    'Конец мая 2025 — весенний ледоход',
    'Середина апреля 2025 — поздняя зима',
    annsA=[
        (0.10,0.42, 0.05,0.25, 'Тундра\n(суша)', COL['land']),
        (0.30,0.52, 0.18,0.70, 'Берег. линия', COL['coast']),
        (0.72,0.18, 0.86,0.06, 'Печорское море\n(откр. вода)', COL['water']),
        (0.44,0.32, 0.57,0.15, 'Кромка льда', COL['ice']),
        (0.52,0.58, 0.66,0.74, 'Дрейфующий лёд', COL['iceL']),
        (0.82,0.52, 0.93,0.66, 'Ветровая тень\n← look-alike', COL['oil']),
    ],
    annsB=[
        (0.12,0.35, 0.05,0.18, 'Тундра\n(суша,\nснег)', COL['land']),
        (0.37,0.50, 0.22,0.66, 'Берег. линия', COL['coast']),
        (0.50,0.38, 0.62,0.20, 'Припай\n(fast ice)', COL['iceL']),
        (0.72,0.28, 0.87,0.13, 'Гладкий лёд (FYI)\n← look-alike', COL['oil']),
        (0.60,0.52, 0.78,0.64, 'Разводье', COL['water']),
    ],
    paramsA=dict(land_pct=82, k=1.3, smooth_pct=45),
    paramsB=dict(land_pct=80, k=1.3, smooth_pct=42),
    legend=[(COL['land'],'суша'),(COL['water'],'вода/разводье'),(COL['ice'],'лёд'),
            (COL['oil'],'тёмная зона (look-alike)')],
    ovA=(0.12,0.45,0.85), ovB=(0.80,0.30,0.10))

# ════════════════════════════════ САБЕТТА ════════════════════════════════
# left=Yamal land/port, right=Ob Gulf; Oct 2022 freeze-up + Dec 2025 winter
sab = four_panel(
    'fig_sabetta.png',
    f'{BASE}/sar_sabetta/scene_oct2022_preview.webp',
    f'{BASE}/sar_sabetta/scene_dec2025_preview.webp',
    'Октябрь 2022 — начало ледостава',
    'Конец декабря 2025 — зимний лёд',
    annsA=[
        (0.12,0.28, 0.04,0.10, 'П-ов Ямал\n(тундра)', COL['land']),
        (0.20,0.60, 0.06,0.50, 'Термокарст.\nозёра', COL['ice']),
        (0.34,0.22, 0.50,0.07, 'Берег. линия', COL['coast']),
        (0.44,0.48, 0.28,0.34, 'Обская губа\n(фарватер)', COL['water']),
        (0.55,0.68, 0.70,0.52, 'Жировой/нилас.\nлёд ← look-alike', COL['oil']),
        (0.82,0.78, 0.93,0.92, 'Откр. вода', COL['water']),
    ],
    annsB=[
        (0.10,0.90, 0.05,0.74, 'Порт Сабетта\n(СПГ + берег)', COL['infra']),
        (0.22,0.65, 0.38,0.52, 'Судовой канал\n(торосы)', COL['iceL']),
        (0.33,0.22, 0.20,0.08, 'Разводье', COL['water']),
        (0.72,0.45, 0.87,0.30, 'Гладкий лёд (FYI)\n← look-alike', COL['oil']),
        (0.42,0.42, 0.58,0.28, 'Нилас', COL['ice']),
    ],
    paramsA=dict(land_pct=78, k=1.2, smooth_pct=48),
    paramsB=dict(land_pct=82, k=1.2, smooth_pct=50),
    legend=[(COL['land'],'суша/порт'),(COL['water'],'вода'),(COL['ice'],'лёд'),
            (COL['oil'],'тёмная зона (look-alike)')],
    ovA=(0.12,0.45,0.85), ovB=(0.80,0.30,0.10))

print("\nALL PORT FIGURES DONE")
