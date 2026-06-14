# -*- coding: utf-8 -*-
"""Render faithful PNG previews of the 11 slides (LibreOffice is unavailable)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from PIL import Image
plt.rcParams['font.family'] = 'Liberation Serif'

FIG = '/home/user/spbu_db_hw/thesis/otchet/figures'
OUT = '/home/user/spbu_db_hw/thesis/presentation/slides_preview'
os.makedirs(OUT, exist_ok=True)

NAVY='#1f4e79'; DARK='#222830'; GRAY='#555b63'; RED='#b02418'; LGRAY='#e9edf2'; GREEN='#2d6a4f'
W, H = 13.333, 7.5

def new_slide():
    fig = plt.figure(figsize=(W, H), facecolor='white', dpi=110)
    ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H)
    ax.axis('off'); ax.invert_yaxis()  # y=0 top
    return fig, ax

def header(ax, title, num):
    ax.add_patch(Rectangle((0,0), W, 1.02, color=NAVY, zorder=1))
    ax.add_patch(Rectangle((0,1.02), W, 0.05, color=RED, zorder=1))
    ax.text(0.45, 0.55, title, color='white', fontsize=21, fontweight='bold', va='center', zorder=2)
    ax.text(0.45, 7.2, 'В. К. Байханов · СПбГУ · 2026', color=GRAY, fontsize=8, va='center')
    ax.text(12.9, 7.2, str(num), color=GRAY, fontsize=9, va='center', ha='right')

def bullets(ax, x, y, items, size=13, dy=0.42, color=DARK, w=None):
    for lvl, t in items:
        mark = '•  ' if lvl==0 else '     –  '
        fs = size if lvl==0 else size-1.5
        ax.text(x, y, mark+t, fontsize=fs, color=color, va='top')
        y += dy
    return y

def place_img(ax, path, x, y, maxw, maxh, cap=None):
    im = Image.open(path); iw, ih = im.size; ar = iw/ih
    if maxw/maxh > ar: w_ = maxh*ar; h_ = maxh
    else: w_ = maxw; h_ = maxw/ar
    px = x + (maxw-w_)/2; py = y + (maxh-h_)/2
    ax.imshow(im, extent=(px, px+w_, py+h_, py), zorder=2, aspect='auto')
    if cap:
        ax.text(x+maxw/2, py+h_+0.18, cap, fontsize=8.5, color=GRAY, style='italic',
                ha='center', va='top')
    return py+h_

def card(ax, x, y, w, h, a, b, alt=False):
    ax.add_patch(Rectangle((x,y), w, h, facecolor=(LGRAY if alt else 'white'),
                 edgecolor=LGRAY, lw=1, zorder=1))
    ax.text(x+0.12, y+h/2, a, fontsize=12, color=DARK, va='center', zorder=2)
    ax.text(x+w-0.12, y+h/2, b, fontsize=12.5, color=NAVY, fontweight='bold',
            va='center', ha='right', zorder=2)

def save(fig, n):
    fig.savefig(f'{OUT}/slide_{n:02d}.png', dpi=110, facecolor='white')
    plt.close(fig); print(f'slide_{n:02d}.png')

# 1 — TITLE
fig, ax = new_slide()
ax.add_patch(Rectangle((0,0),W,0.32,color=NAVY)); ax.add_patch(Rectangle((0,H-0.32),W,0.32,color=NAVY))
ax.text(W/2, 0.95, 'Санкт-Петербургский государственный университет', fontsize=14, color=GRAY, ha='center')
ax.text(W/2, 1.9, 'Разработка системы автоматического детектирования\nнефтяных разливов в акваториях арктических портов\nпо данным спутниковых систем',
        fontsize=22, color=NAVY, fontweight='bold', ha='center', va='center')
ax.add_patch(Rectangle((0,2.95),W,0.04,color=RED))
ax.text(W/2, 3.4, 'Магистерская диссертация · Прикладная информатика (ИИ и наука о данных)',
        fontsize=13, color=DARK, style='italic', ha='center')
ax.text(W/2, 4.6, 'Выполнил: Байханов Владислав Камолович\n'
        'Научный руководитель: к.т.н., доцент Митько А. В.\n'
        'Рецензент: д.т.н., проф. Филиппова Н. А. (МАДИ)',
        fontsize=14, color=DARK, ha='center', va='center', linespacing=1.6)
ax.text(W/2, 6.5, 'Санкт-Петербург · 2026', fontsize=12, color=GRAY, ha='center')
save(fig, 1)

# 2 — ACTUALITY / NORILSK
fig, ax = new_slide(); header(ax, 'Актуальность: нефтяные риски в Арктике', 2)
bullets(ax, 0.45, 1.45, [
    (0,'Рост грузопотока СМП: 37,9 млн т (2024) → больше'),
    (1,'операций перевалки и бункеровки в портах.'),
    (0,'Кольский залив, 2024: два разлива мазута за сезон,'),
    (1,'источник не установлен своевременно.'),
    (0,'Норильск, 29.05.2020: авария ТЭЦ-3, ≈21 тыс. т'),
    (1,'дизеля; Далдыкан→Амбарная→оз. Пясино;'),
    (1,'ущерб 146–148 млрд руб.'),
    (0,'Оптика и полярная ночь не дают круглосуточный'),
    (1,'мониторинг (облачность > 80 % времени).'),
    (0,'SAR Sentinel-1 (C-диапазон) — всепогодный'),
    (1,'круглосуточный инструмент.'),
], size=13)
yb = place_img(ax, f'{FIG}/fig_norilsk.png', 6.7, 1.5, 6.4, 4.4,
        cap='Норильск-2020: на SAR доминирует сезонная динамика «лёд→вода»,\nмониторинг вёлся оптикой Sentinel-2.')
save(fig, 2)

# 3 — GOAL / NOVELTY
fig, ax = new_slide(); header(ax, 'Цель работы и научная новизна', 3)
ax.text(0.45, 1.45, 'Цель: разработать систему автоматического детектирования нефтяных\n'
        'разливов в акваториях арктических портов по данным Sentinel-1,\n'
        'устойчивую к арктическим ложным целям.', fontsize=14.5, color=DARK, va='top')
ax.add_patch(Rectangle((0.45,3.0),12.4,0.03,color=LGRAY))
ax.text(0.45, 3.2, 'Научная новизна:', fontsize=15, color=NAVY, fontweight='bold', va='top')
bullets(ax, 0.45, 3.8, [
    (0,'Трёхклассовая разметка SAR: «вода» / «нефть» / «лёд + суша» —'),
    (1,'впервые лёд выделен в отдельный класс.'),
    (0,'Адаптация DeepLabV3+ к одноканальным SAR-данным VV:'),
    (1,'энкодер ResNet-50 + блоки внимания scSE.'),
    (0,'Интегрированный конвейер с трёхуровневой верификацией:'),
    (1,'морфология + ERA5 + сопоставление с АИС судов.'),
], size=14)
save(fig, 3)

# 4 — PHYSICS / LOOK-ALIKES
fig, ax = new_slide(); header(ax, 'Физика SAR и проблема ложных целей', 4)
bullets(ax, 0.45, 1.45, [
    (0,'Эффект Марангони: плёнка гасит капиллярные волны'),
    (1,'→ σ0 падает на 10–20 дБ → тёмное пятно.'),
    (0,'До 70 % тёмных пятен — НЕ нефть (look-alikes):'),
    (1,'начальные формы льда (жировой, нилас, шуга);'),
    (1,'ветровые тени; биогенные плёнки.'),
    (0,'Тёмное пятно — необходимый, но НЕ'),
    (1,'достаточный признак нефти.'),
    (0,'Разделение — поляризационная разность'),
    (1,'PD = σ0_VV − σ0_VH и контекст (нейросеть).'),
], size=13)
# table
ax.add_patch(Rectangle((7.0,1.5),5.9,4.0,facecolor=LGRAY,edgecolor='none'))
ax.text(9.95,1.85,'Сравнение тёмных сигнатур', fontsize=14,color=NAVY,fontweight='bold',ha='center')
rows=[['Объект','σ0 VV','PD'],['Нефть','низкий','6–10 дБ'],
      ['Молодой лёд','низкий','< 4 дБ'],['Ветровая тень','низкий','2–5 дБ'],
      ['Откр. вода','средний','3–6 дБ']]
ty=2.2
for i,r in enumerate(rows):
    if i==0: ax.add_patch(Rectangle((7.15,ty-0.02),5.6,0.42,color=NAVY,zorder=1))
    for j,c in enumerate(r):
        col = 'white' if i==0 else (RED if i==1 else DARK)
        fw = 'bold' if i<=1 else 'normal'
        ax.text(7.4+j*1.9, ty+0.18, c, fontsize=12, color=col, fontweight=fw, va='center', zorder=2)
    ty+=0.62
save(fig, 4)

# 5 — PECHENGA + VARANDEY
fig, ax = new_slide(); header(ax, 'Контрольные полигоны: Печенга и Варандей', 5)
ax.text(0.45,1.25,'Разливов в 2022–2025 гг. не было → все тёмные зоны заведомо ложные цели.',
        fontsize=12, color=GRAY, style='italic', va='top')
place_img(ax, f'{FIG}/fig_pechenga.png', 0.4, 1.7, 6.2, 4.5,
          cap='Печенга: ветровые тени и биогенные плёнки.')
place_img(ax, f'{FIG}/fig_varandey.png', 6.85, 1.7, 6.2, 4.5,
          cap='Варандей: сезонный первогодний лёд имитирует нефть.')
save(fig, 5)

# 6 — SABETTA
fig, ax = new_slide(); header(ax, 'Контрольный полигон: Сабетта (тяжёлый лёд)', 6)
place_img(ax, f'{FIG}/fig_sabetta.png', 0.4, 1.35, 7.2, 5.3,
          cap='Жировой/ниласовый лёд и припай — сильнейшие двойники нефти.')
ax.text(8.0,1.55,'Полный спектр ложных целей:', fontsize=14,color=NAVY,fontweight='bold',va='top')
data=[['Печенга','ветер, биоплёнки'],['Варандей','сезонный лёд'],['Сабетта','жировой лёд, припай']]
yy=2.05
for i,(a,b) in enumerate(data):
    card(ax, 8.0, yy, 4.9, 0.6, a, b, alt=(i%2==0)); yy+=0.62
ax.text(8.0,4.3,'Вывод: бинарный порог даёт ложные\nсрабатывания на всех акваториях.\n'
        'Нужно явное выделение льда в класс\nи контекстная верификация.',
        fontsize=12.5, color=DARK, va='top', linespacing=1.4)
save(fig, 6)

# 7 — ARCHITECTURE
fig, ax = new_slide(); header(ax, 'Архитектура: трёхэтапный конвейер', 7)
place_img(ax, f'{FIG}/fig_pipeline.png', 0.5, 1.45, 12.3, 4.0)
bullets(ax, 0.6, 5.7, [
    (0,'SNAP: калибровка к σ0, фильтр Lee 7×7, Range-Doppler коррекция.'),
    (0,'PyTorch: DeepLabV3+ / ResNet-50 + scSE, 3 класса, TTA.'),
    (0,'Верификация: морфология + ERA5 (ветер 3–9 м/с) + АИС судов.'),
], size=12.5, dy=0.4)
save(fig, 7)

# 8 — DATASET & TRAINING
fig, ax = new_slide(); header(ax, 'Датасет и обучение модели', 8)
place_img(ax, f'{FIG}/fig_class_dist.png', 0.3, 1.4, 4.5, 4.5)
place_img(ax, f'{FIG}/fig_training.png', 5.0, 1.5, 8.0, 3.3)
bullets(ax, 5.0, 5.0, [
    (0,'1125 сцен (MKLab + 13 сцен Кольского залива), 4128 тайлов 256×256.'),
    (0,'Дисбаланс компенсирован Dice-BCE (w_нефть = 9,8).'),
    (0,'AdamW, lr 1e-4; лучшее val mIoU = 0,84 (эпоха 78); RTX 3090, ~7,5 ч.'),
], size=12.5, dy=0.42)
save(fig, 8)

# 9 — RESULTS
fig, ax = new_slide(); header(ax, 'Результаты сегментации (Кольский залив)', 9)
place_img(ax, f'{FIG}/fig_confusion.png', 0.4, 1.4, 6.0, 5.3)
ax.text(6.9,1.6,'Тестовая выборка (414 тайлов):', fontsize=15,color=NAVY,fontweight='bold',va='top')
cards=[('Общая точность','95,8 %'),('mIoU (3 класса)','0,82'),('F1 «нефть»','0,89'),
       ('Precision «нефть»','0,911'),('Recall «нефть»','0,875')]
yy=2.15
for i,(a,b) in enumerate(cards):
    card(ax, 6.9, yy, 5.9, 0.6, a, b, alt=(i%2==0)); yy+=0.62
ax.text(6.9,5.45,'Основная ошибка: 8,4 % «нефть» → «лёд+суша» —\nфизическая близость откликов нефти и молодого льда.',
        fontsize=12, color=RED, style='italic', va='top', linespacing=1.4)
save(fig, 9)

# 10 — TRANSFER + COMPARISON
fig, ax = new_slide(); header(ax, 'Перенос на порты и сравнение с аналогами', 10)
place_img(ax, f'{FIG}/fig_ports_f1.png', 0.35, 1.4, 6.4, 4.4,
          cap='F1: Кольский 0,89 → Варандей 0,84 → Сабетта 0,76.')
place_img(ax, f'{FIG}/fig_methods.png', 6.9, 1.4, 6.2, 4.4,
          cap='DeepLabV3+ scSE превосходит аналоги (F1 = 0,89).')
ax.text(0.45,6.5,'Рост ложных срабатываний на Сабетте (FP 1,4 %→6,2 %) на участках шуги и ниласа —\n'
        'подтверждает необходимость дообучения на арктических данных.',
        fontsize=12, color=GRAY, style='italic', va='top', linespacing=1.4)
save(fig, 10)

# 11 — CONCLUSIONS
fig, ax = new_slide(); header(ax, 'Выводы', 11)
bullets(ax, 0.5, 1.45, [
    (0,'Тёмное пятно в SAR — необходимый, но не достаточный признак нефти'),
    (1,'(Печенга, Варандей, Сабетта — все тёмные зоны ложные).'),
    (0,'Норильск-2020 показал предел C-SAR для дизеля на реках при ледоходе'),
    (1,'→ фокус на морских акваториях, выделение льда в отдельный класс.'),
    (0,'Модель DeepLabV3+ (ResNet-50 + scSE), 3 класса:'),
    (1,'точность 95,8 %, mIoU 0,82, F1 «нефть» = 0,89 (Кольский залив).'),
    (0,'Перенос на порты: F1 0,84 (Варандей), 0,76 (Сабетта)'),
    (1,'→ приоритет: расширение арктического датасета.'),
    (0,'Подход превзошёл 4 метода-аналога (0,89 против 0,71–0,86).'),
], size=13.5, dy=0.46)
ax.add_patch(Rectangle((0.5,6.5),12.3,0.04,color=RED))
ax.text(W/2,6.95,'Спасибо за внимание!', fontsize=18,color=NAVY,fontweight='bold',ha='center')
save(fig, 11)

print('ALL PREVIEWS DONE')
