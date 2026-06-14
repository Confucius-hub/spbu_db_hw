import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from scipy import ndimage as ndi
from scipy.ndimage import gaussian_filter, binary_opening, binary_closing

plt.rcParams['font.family'] = 'DejaVu Sans'

def load(name):
    return np.asarray(Image.open(name).convert('L'), float)

def low_mask(a, pct, min_area_frac=0.0006):
    sm = gaussian_filter(a, sigma=2.0)
    thr = np.percentile(sm, pct)
    m = sm < thr
    m = binary_opening(m, iterations=2)
    m = binary_closing(m, iterations=2)
    lbl, n = ndi.label(m)
    sizes = ndi.sum(np.ones_like(lbl), lbl, range(1, n+1))
    keep = np.zeros_like(m)
    for i, s in enumerate(sizes, start=1):
        if s >= a.size*min_area_frac:
            keep |= (lbl == i)
    return keep, thr

def panel(name, title, sub, out, annots, pct):
    a = load(name); H, W = a.shape
    mask, thr = low_mask(a, pct)
    df = mask.mean()*100
    fig, ax = plt.subplots(1, 2, figsize=(17, 17*H/W/2*1.04))
    fig.patch.set_facecolor('#0b0e14')
    # left original
    ax[0].imshow(a, cmap='gray', vmin=0, vmax=255, aspect='equal')
    ax[0].set_title('а) Исходный снимок Sentinel-1 (VV, превью)', color='w', fontsize=12, pad=8)
    ax[0].add_patch(Rectangle((W*0.04, H*0.93), W*0.18, H*0.012, color='w'))
    ax[0].text(W*0.04, H*0.905, 'масштаб условный', color='w', fontsize=8)
    # right annotated
    ax[1].imshow(a, cmap='gray', vmin=0, vmax=255, aspect='equal')
    ov = np.zeros((H, W, 4)); ov[...,0]=0.10; ov[...,1]=0.75; ov[...,2]=1.0; ov[...,3]=mask*0.33
    ax[1].imshow(ov, aspect='equal')
    ax[1].set_title(f'б) Зоны низкого обратного рассеяния (< P{pct}) — {df:.1f}% кадра', color='w', fontsize=12, pad=8)
    for axx in ax:
        axx.set_xticks([]); axx.set_yticks([])
        for s in axx.spines.values(): s.set_color('#3a4252')
    for (fx, fy, txt, col, tx, ty) in annots:
        ax[1].add_patch(FancyArrowPatch((tx*W, ty*H), (fx*W, fy*H), arrowstyle='-|>',
                        mutation_scale=14, color=col, lw=1.8, shrinkA=0, shrinkB=2))
        ax[1].text(tx*W, ty*H, txt, color='w', fontsize=9, fontweight='bold', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', fc=col, ec='none', alpha=0.92))
    fig.suptitle(title, color='w', fontsize=14.5, fontweight='bold', y=0.995)
    fig.text(0.5, 0.962, sub, color='#9aa4b2', fontsize=10, ha='center')
    fig.text(0.5, 0.012,
        'Примечание: анализ по 8-битному превью (скриншот) — КАЧЕСТВЕННОЕ распределение яркости. Тёмные зоны = гладкие поверхности '
        '(вода/реки/тени рельефа) и НЕ отделяют нефть от воды/льда. Для этого нужны калиброванные σ⁰(дБ) VV/VH и PD из продукта .SAFE (SNAP).',
        color='#6b7280', fontsize=8, ha='center', style='italic')
    plt.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.055, wspace=0.03)
    plt.savefig(out, dpi=160, facecolor=fig.get_facecolor()); plt.close()
    print(out, f'dark={df:.1f}% thr={thr:.0f}')

panel('scene1_norilsk_pyasino_preview.webp',
    'Сцена 1. Норильск — оз. Пясино и плато Путорана (Sentinel-1 IW GRD, VV)',
    'обзорный кадр · бассейн Карского моря',
    'scene1_annotated.png',
    annots=[
        (0.47, 0.40, 'НОРИЛЬСК\nгород + промзона\n(яркий отклик)', '#dc2626', 0.30, 0.18),
        (0.40, 0.86, 'Оз. Пясино', '#2563eb', 0.20, 0.95),
        (0.55, 0.22, 'Речной канал', '#0ea5e9', 0.66, 0.10),
        (0.80, 0.66, 'Плато Путорана\n(рельеф: тёмные тени\nв долинах)', '#a16207', 0.92, 0.40),
        (0.83, 0.28, 'Озеро в\nпредгорьях', '#2563eb', 0.95, 0.16),
        (0.14, 0.50, 'Термокарстовые\nозёра', '#0ea5e9', 0.07, 0.30),
    ], pct=22)

panel('scene2_meander_river_preview.webp',
    'Сцена 2. Меандрирующее русло (р. Пясина/Амбарная) в тундре (Sentinel-1 IW GRD, VV)',
    'нижнее течение · сильная меандрация',
    'scene2_annotated.png',
    annots=[
        (0.50, 0.30, 'Слияние\nрукавов', '#dc2626', 0.72, 0.12),
        (0.42, 0.50, 'Главное русло\n(меандры)', '#2563eb', 0.75, 0.30),
        (0.22, 0.68, 'Дендритовая сеть\nпритоков', '#0ea5e9', 0.08, 0.55),
        (0.33, 0.82, 'Старицы /\nbraided-комплекс', '#0ea5e9', 0.12, 0.95),
        (0.92, 0.42, 'Широкий\nводоём', '#2563eb', 0.95, 0.22),
        (0.68, 0.58, 'Тундровая\nравнина', '#16a34a', 0.85, 0.72),
    ], pct=25)
print('DONE')
