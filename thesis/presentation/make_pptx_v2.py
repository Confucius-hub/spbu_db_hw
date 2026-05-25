#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_pptx_v2.py — 12-slide VKR defence presentation (2026).
Style: exact colour palette + layout from user's A-grade previous deck.
White background · navy header bar · section labels · Liberation Serif.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import os

FIGS  = '/home/user/spbu_db_hw/thesis/otchet/figures'
OUT   = '/home/user/spbu_db_hw/thesis/presentation/Презентация_ВКР_2026.pptx'

# ── Colour palette (from user's A-grade presentation) ────────────────────────
NAVY   = RGBColor(0x1E, 0x3A, 0x5F)   # primary navy  #1E3A5F
NAVY2  = RGBColor(0x2C, 0x52, 0x82)   # secondary navy
RED    = RGBColor(0xC5, 0x30, 0x30)   # red accent
RED2   = RGBColor(0x92, 0x40, 0x0E)   # dark amber/brown
GREEN  = RGBColor(0x27, 0x67, 0x49)   # green
LBLUE  = RGBColor(0xEB, 0xF4, 0xFF)   # light blue card bg
LGRAY  = RGBColor(0xF8, 0xFA, 0xFC)   # light gray card bg
LGRAY2 = RGBColor(0xF0, 0xF4, 0xF8)   # slightly darker gray
LAMBER = RGBColor(0xFF, 0xFB, 0xEB)   # light amber
LRED   = RGBColor(0xFF, 0xF5, 0xF5)   # light red bg
LGREEN = RGBColor(0xF0, 0xFF, 0xF4)   # light green bg
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GRAY   = RGBColor(0x4A, 0x55, 0x68)
ORANGE = RGBColor(0xD9, 0x77, 0x06)

FONT  = 'Liberation Serif'
TOTAL = 12

# ── Presentation setup ───────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(10)
prs.slide_height = Inches(5.625)
SW, SH = prs.slide_width, prs.slide_height
BLANK  = prs.slide_layouts[6]   # completely blank layout


def sl():
    return prs.slides.add_slide(BLANK)


def R(s, x, y, w, h, fill, line_col=None, line_w=None):
    """Rectangle (inches).  line_col=None → no border."""
    sp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                            Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid()
    sp.fill.fore_color.rgb = fill
    if line_col is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line_col
        sp.line.width = Pt(line_w or 0.75)
    sp.shadow.inherit = False
    return sp


def T(s, x, y, w, h, text='', sz=10, col=GRAY, bold=False, italic=False,
      align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, sp_after=0, wrap=True):
    """Text box – splits on \\n into separate paragraphs."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    for i, line in enumerate(text.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if sp_after:
            p.space_after = Pt(sp_after)
        r = p.add_run()
        r.text = line
        r.font.name = FONT
        r.font.size = Pt(sz)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = col
    return tb, tf


def add_run(tf, text, sz=10, col=GRAY, bold=False, italic=False):
    """Append a run to the last paragraph of tf."""
    p = tf.paragraphs[-1]
    r = p.add_run()
    r.text = text
    r.font.name = FONT; r.font.size = Pt(sz)
    r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = col


def new_para(tf, sz=10, col=GRAY, bold=False, align=PP_ALIGN.LEFT,
             before=0, after=0):
    """Add blank paragraph and return it (caller adds runs)."""
    p = tf.add_paragraph()
    p.alignment = align
    if before: p.space_before = Pt(before)
    if after:  p.space_after  = Pt(after)
    return p


def para_run(tf, text, sz=10, col=GRAY, bold=False, italic=False,
             align=PP_ALIGN.LEFT, before=2, after=0):
    """Add a new paragraph with a single run."""
    p = new_para(tf, sz, col, bold, align, before, after)
    r = p.add_run()
    r.text = text
    r.font.name = FONT; r.font.size = Pt(sz)
    r.font.bold = bold; r.font.italic = italic; r.font.color.rgb = col
    return p


def PIC(s, fname, x, y, max_w, max_h, center=True):
    """Embed image, preserving aspect ratio within max_w×max_h box."""
    path = os.path.join(FIGS, fname)
    iw, ih = Image.open(path).size
    ar = iw / ih
    bx = max_w / max_h
    if ar > bx:
        w = max_w; h = max_w / ar
    else:
        h = max_h; w = max_h * ar
    ox = (max_w - w) / 2 if center else 0
    oy = (max_h - h) / 2 if center else 0
    s.shapes.add_picture(path, Inches(x + ox), Inches(y + oy),
                         Inches(w), Inches(h))


def HDR(s, label, title, pg):
    """Standard content-slide header."""
    R(s, 0, 0, 10, 0.62, NAVY)                          # navy bar
    R(s, 0, 0.62, 10, 0.035, RED)                        # red accent line
    T(s, 0.12, 0.09, 1.55, 0.46, label, sz=7, col=WHITE, bold=True, wrap=False)
    R(s, 1.72, 0.11, 0.02, 0.4, WHITE)                  # white vertical separator
    T(s, 1.77, 0.09, 8.1, 0.46, title, sz=13.5, col=WHITE, bold=True, wrap=False)
    T(s, 9.0, 5.3, 0.95, 0.28, f'{pg} / {TOTAL}', sz=7, col=GRAY,
      align=PP_ALIGN.RIGHT, wrap=False)


def CARD(s, x, y, w, h, hdr_text, hdr_col=NAVY, bg=LGRAY, hdr_sz=8.5):
    """Coloured-header card.  Returns (cx, cy) = top-left of body area."""
    R(s, x, y, w, h, bg)
    R(s, x, y, w, 0.3, hdr_col)
    T(s, x + 0.08, y + 0.04, w - 0.12, 0.26, hdr_text,
      sz=hdr_sz, col=WHITE, bold=True)
    return x, y + 0.3


def STAT(s, x, y, w, h, big, lines, hdr_col=NAVY, bg=LBLUE):
    """Stat card: big number in header, description lines in body."""
    R(s, x, y, w, 0.7, hdr_col)
    T(s, x + 0.05, y + 0.04, w - 0.1, 0.62, big, sz=20,
      col=WHITE, bold=True, align=PP_ALIGN.CENTER)
    R(s, x, y + 0.7, w, h - 0.7, bg)
    tb, tf = T(s, x + 0.07, y + 0.72, w - 0.12, h - 0.76, sz=7.5, col=GRAY)
    tf.word_wrap = True
    for i, ln in enumerate(lines):
        if i == 0:
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            r = tf.paragraphs[0].add_run()
            r.text = ln; r.font.name = FONT
            r.font.size = Pt(7.5); r.font.color.rgb = GRAY
        else:
            para_run(tf, ln, sz=7.5, col=GRAY, align=PP_ALIGN.CENTER, before=1)


def NUM_CARD(s, x, y, w, h, num, num_col, title, body, bg=LBLUE):
    """Numbered card (like novelty items)."""
    R(s, x, y, w, h, bg)
    R(s, x, y, 0.4, h, num_col)
    T(s, x + 0.04, y + h / 2 - 0.22, 0.34, 0.44, str(num), sz=18,
      col=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    T(s, x + 0.45, y + 0.06, w - 0.52, 0.28, title,
      sz=9, col=num_col, bold=True)
    T(s, x + 0.45, y + 0.32, w - 0.52, h - 0.38, body,
      sz=8, col=GRAY)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 1 — TITLE
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
R(s, 0, 0, 10, 1.3, NAVY)
R(s, 0, 1.3, 10, 0.055, RED)          # red accent under header

T(s, 0.35, 0.08, 9.3, 1.18,
  'Разработка системы автоматического детектирования\n'
  'нефтяных разливов в акваториях арктических портов\n'
  'по данным спутниковых радиолокационных систем',
  sz=16.5, col=WHITE, bold=True, align=PP_ALIGN.LEFT, sp_after=3)

# Left info block
R(s, 0.3, 1.52, 4.6, 2.65, LGRAY)
R(s, 0.3, 1.52, 4.6, 0.3, NAVY2)
T(s, 0.42, 1.56, 4.35, 0.26, 'САНКТ-ПЕТЕРБУРГСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ',
  sz=6.5, col=WHITE, bold=True)
T(s, 0.42, 1.88, 4.35, 0.28, 'Кафедра информатики', sz=9, col=NAVY2)
T(s, 0.42, 2.18, 4.35, 0.28, 'Направление: Прикладная информатика', sz=9, col=GRAY)
T(s, 0.42, 2.48, 4.35, 0.28, 'Профиль: Искусственный интеллект и наука о данных',
  sz=9, col=GRAY)
T(s, 0.42, 2.88, 4.35, 0.3, 'Магистерская диссертация · 2026',
  sz=10, col=NAVY, bold=True)

# Right author block
R(s, 5.1, 1.52, 4.6, 2.65, LBLUE)
R(s, 5.1, 1.52, 4.6, 0.3, NAVY)
T(s, 5.22, 1.56, 4.35, 0.26, 'СВЕДЕНИЯ ОБ АВТОРЕ',
  sz=6.5, col=WHITE, bold=True)
T(s, 5.22, 1.88, 4.35, 0.26, 'Подготовил:', sz=8, col=GRAY)
T(s, 5.22, 2.12, 4.35, 0.3, 'Байханов Владислав Камолович',
  sz=11, col=NAVY, bold=True)
T(s, 5.22, 2.42, 4.35, 0.26, 'студент группы 24.М81-мм', sz=8.5, col=GRAY)
T(s, 5.22, 2.76, 4.35, 0.26, 'Научный руководитель:', sz=8, col=GRAY)
T(s, 5.22, 2.98, 4.35, 0.35, 'к.т.н., доцент Митько А. В.', sz=9.5, col=NAVY)

T(s, 9.0, 5.3, 0.95, 0.28, f'1 / {TOTAL}', sz=7, col=GRAY,
  align=PP_ALIGN.RIGHT, wrap=False)
print('Slide 1 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 2 — АКТУАЛЬНОСТЬ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'АКТУАЛЬНОСТЬ', 'Проблематика · Обоснование выбора SAR', 2)

# Top stat cards
STAT(s, 0.08, 0.72, 2.9, 1.52, '700+',
     ['тыс. т нефти в год', 'попадает в Мировой', 'океан (ITOPF, 2023)'])
STAT(s, 3.25, 0.72, 3.05, 1.52, '5–10×',
     ['медленнее разложение', 'нефти в арктических', 'водах (<5 °C)'])
STAT(s, 6.62, 0.72, 3.3, 1.52, '>80%',
     ['облачность — оптика', 'не работает круглый', 'год в Арктике'])

# Left: Why SAR
cx, cy = CARD(s, 0.08, 2.38, 4.6, 2.95, 'Почему SAR (радиолокация)?', NAVY, LGRAY)
tb, tf = T(s, cx + 0.1, cy + 0.05, 4.35, 2.55, sz=8.5, col=GRAY)
tf.word_wrap = True
items_sar = [
    ('Работает 24/7:', 'полярная ночь не препятствие'),
    ('Сквозь облака:', 'C-диапазон (5.405 ГГц) не поглощается'),
    ('Эффект Марангони:', 'нефть гасит капиллярные волны → σ⁰ ↓ 10–20 дБ → тёмное пятно'),
    ('Sentinel-1:', 'бесплатный архив ESA, 10 м/пкс, повтор ~6 сут'),
    ('Поляризации VV+VH:', 'разность PD различает нефть (6–10 дБ) и лёд (<4 дБ)'),
]
first = True
for lbl, val in items_sar:
    if first:
        tf.paragraphs[0].alignment = PP_ALIGN.LEFT
        r = tf.paragraphs[0].add_run()
        r.text = f'▶ {lbl} '; r.font.name = FONT
        r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = NAVY2
        r2 = tf.paragraphs[0].add_run()
        r2.text = val; r2.font.name = FONT
        r2.font.size = Pt(8.5); r2.font.color.rgb = GRAY
        first = False
    else:
        p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(3)
        r = p.add_run(); r.text = f'▶ {lbl} '
        r.font.name = FONT; r.font.size = Pt(8.5)
        r.font.bold = True; r.font.color.rgb = NAVY2
        r2 = p.add_run(); r2.text = val
        r2.font.name = FONT; r2.font.size = Pt(8.5); r2.font.color.rgb = GRAY

# Right: Arctic ports risk
cx, cy = CARD(s, 4.92, 2.38, 5.0, 2.95, 'Арктические порты — зона риска', RED2, LGRAY)
tb, tf = T(s, cx + 0.1, cy + 0.05, 4.75, 2.55, sz=8.5, col=GRAY)
tf.word_wrap = True
ports_info = [
    ('Кольский залив:', '~30–40 млн т/год, регулярные бункеровки, разлив авг 2024'),
    ('Варандей:', 'морской нефтеналивной терминал Ненецкого АО, ~2 млн т/год'),
    ('Сабетта:', 'ворота арктического СПГ (НоваТЭК), Обская губа'),
    ('Печенга:', 'военно-морской и рыбный порт, Мурманская обл.'),
    ('Норильск-2020:', '≈21 000 т дизтоплива ТЭЦ-3 НТЭК, штраф 146 млрд руб.'),
]
first = True
for lbl, val in ports_info:
    if first:
        tf.paragraphs[0].alignment = PP_ALIGN.LEFT
        r = tf.paragraphs[0].add_run()
        r.text = f'● {lbl} '; r.font.name = FONT
        r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = RED2
        r2 = tf.paragraphs[0].add_run()
        r2.text = val; r2.font.name = FONT
        r2.font.size = Pt(8.5); r2.font.color.rgb = GRAY
        first = False
    else:
        p = tf.add_paragraph(); p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(3)
        r = p.add_run(); r.text = f'● {lbl} '
        r.font.name = FONT; r.font.size = Pt(8.5)
        r.font.bold = True; r.font.color.rgb = RED2
        r2 = p.add_run(); r2.text = val
        r2.font.name = FONT; r2.font.size = Pt(8.5); r2.font.color.rgb = GRAY

print('Slide 2 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 3 — ЦЕЛЬ И ЗАДАЧИ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'ЦЕЛЬ И ЗАДАЧИ', 'Цель и задачи исследования', 3)

# Goal box
R(s, 0.12, 0.73, 9.76, 0.75, LBLUE)
R(s, 0.12, 0.73, 9.76, 0.3, NAVY)
T(s, 0.22, 0.76, 9.55, 0.26, 'ЦЕЛЬ', sz=8.5, col=WHITE, bold=True)
T(s, 0.22, 1.0, 9.55, 0.44,
  'Разработать и верифицировать систему автоматического детектирования нефтяных разливов '
  'в акваториях арктических портов по данным Sentinel-1, устойчивую к арктическим ложным целям.',
  sz=9.5, col=NAVY, bold=False)

# Six numbered task cards (2 columns × 3 rows)
tasks = [
    (NAVY,  'Физика SAR и look-alikes',
     'Изучить эффект Марангони; систематизировать ложные цели\n'
     '(лёд, штиль, биоплёнки) для арктических акваторий'),
    (NAVY2, 'Конвейер предобработки ESA SNAP',
     'Реализовать 8-шаговый конвейер: орбиты → термошум →\n'
     'калибровка σ⁰ → фильтр Ли 7×7 → геокоррекция'),
    (NAVY,  'Трёхклассовый датасет',
     'Сформировать аннотированный датасет: вода / нефть / лёд+суша\n'
     '(1 125 сцен, 4 128 тайлов 256×256) на базе MKLab + Кольский залив'),
    (NAVY2, 'Адаптация DeepLabV3+',
     'Модифицировать архитектуру под 1-канальный SAR-вход;\n'
     'добавить блоки внимания scSE; настроить Dice-BCE'),
    (GREEN, 'Обучение и перенос модели',
     'Обучить на Кольском заливе (78 эпох);\n'
     'проверить перенос на Варандей, Сабетту, Печенгу'),
    (GREEN, 'Сравнительный анализ',
     'Сопоставить с 4 аналогами из литературы\n'
     '(Отцу, U-Net, GLCM+CNN, адаптивный порог) по F1-score'),
]

col_w, row_h = 4.72, 1.0
yy = 1.58
for i, (nc, title, body) in enumerate(tasks):
    col = i % 2
    row = i // 2
    xx = 0.12 + col * (col_w + 0.44)
    yy_i = yy + row * (row_h + 0.06)
    R(s, xx, yy_i, col_w, row_h, LGRAY)
    R(s, xx, yy_i, 0.36, row_h, nc)
    T(s, xx + 0.06, yy_i + row_h / 2 - 0.14, 0.26, 0.28,
      str(i + 1), sz=14, col=WHITE, bold=True, align=PP_ALIGN.CENTER)
    T(s, xx + 0.43, yy_i + 0.06, col_w - 0.5, 0.26, title, sz=9, col=nc, bold=True)
    T(s, xx + 0.43, yy_i + 0.3, col_w - 0.5, row_h - 0.34, body, sz=7.8, col=GRAY)

print('Slide 3 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 4 — ДАННЫЕ И ДАТАСЕТ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'ДАННЫЕ', 'Исходные данные и аннотированный датасет', 4)

# Left: Sentinel-1 specs table
cx, cy = CARD(s, 0.12, 0.72, 4.52, 4.55, 'Sentinel-1 IW GRD — технические параметры',
              NAVY, LGRAY)
specs = [
    ('Спутник',       'Sentinel-1A/B (ESA Copernicus)'),
    ('Режим',         'IW GRD (Interferometric Wide Swath)'),
    ('Диапазон',      'C-band, 5.405 ГГц'),
    ('Поляризация',   'VV + VH (VV — основной для нефти)'),
    ('Разрешение',    '10 м / пксель'),
    ('Полоса охвата', '250 км'),
    ('Тайлы',         '256 × 256 пкс, 50 % перекрытие'),
    ('Сцен (обуч.)',  '1 125 (MKLab + Кольский залив)'),
    ('Тайлов всего',  '4 128'),
    ('Период',        '2022–2025 (4 акватории)'),
]
row_h_s = 0.37
for j, (k, v) in enumerate(specs):
    yy = cy + 0.04 + j * row_h_s
    bg = LGRAY2 if j % 2 == 0 else LGRAY
    R(s, cx + 0.04, yy, 4.4, row_h_s - 0.02, bg)
    T(s, cx + 0.1, yy + 0.04, 1.65, 0.28, k, sz=8, col=NAVY2, bold=True)
    T(s, cx + 1.82, yy + 0.04, 2.6, 0.28, v, sz=8, col=GRAY)

# Right: class distribution figure
R(s, 4.82, 0.72, 5.06, 4.55, LGRAY)
R(s, 4.82, 0.72, 5.06, 0.3, NAVY2)
T(s, 4.92, 0.76, 4.86, 0.26, 'Распределение классов в датасете', sz=8.5, col=WHITE, bold=True)
PIC(s, 'fig_class_dist.png', 4.86, 1.04, 4.98, 4.05)

print('Slide 4 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 5 — КОНВЕЙЕР ОБРАБОТКИ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'МЕТОДОЛОГИЯ', 'Трёхэтапный конвейер обработки SAR-данных', 5)

PIC(s, 'fig_pipeline.png', 0.1, 0.72, 9.8, 3.95)

# Caption / annotation below
R(s, 0.12, 4.75, 9.76, 0.62, LAMBER)
T(s, 0.22, 4.8, 9.55, 0.55,
  'Этап 1 — ESA SNAP (8 шагов: орбиты → термошум → σ⁰ → фильтр Ли 7×7 → геокоррекция WGS-84)  '
  '│  Этап 2 — DeepLabV3+ PyTorch (3 класса, Dice-BCE, TTA)  '
  '│  Этап 3 — верификация ERA5 + AIS',
  sz=8, col=GRAY, italic=True)

print('Slide 5 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 6 — АРХИТЕКТУРА DeepLabV3+
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'АРХИТЕКТУРА', 'DeepLabV3+ с блоками внимания scSE — адаптация для SAR', 6)

cw, ch = 3.06, 2.9
cards6 = [
    (NAVY,  'Энкодер ResNet-50 (модифицирован)',
     'Предобучен на ImageNet → трансфер весов\n\n'
     '▶ Входной слой: conv1 1-канальный (VV σ⁰ дБ)\n'
     '▶ 5 уровней, 64–2048 карт признаков\n'
     '▶ Дилатированные свёртки в слоях 3–4\n'
     '▶ Выходной страйд: 16 (высокое разрешение)'),
    (NAVY2, 'ASPP — многомасштабный контекст',
     'Atrous Spatial Pyramid Pooling\n\n'
     '▶ Ветви с r = 6, 12, 18 (dilated conv)\n'
     '▶ Глобальный average pooling\n'
     '▶ Конкатенация → понижение до 256 каналов\n'
     '▶ Захват объектов от пикселя до 18× рецептивного поля'),
    (GREEN, 'Декодер + scSE-внимание',
     'Конкатенация со skip-connections (Этап 1)\n\n'
     '▶ scSE = Spatial + Channel Squeeze & Excitation\n'
     '▶ Подавляет спекл, усиливает нефтяные пятна\n'
     '▶ 3 класса: вода · нефть · лёд+суша\n'
     '▶ Веса: w = 0.3 · 9.8 · 1.2 (компенсация дисбаланса)'),
]
for i, (hc, htxt, body) in enumerate(cards6):
    xx = 0.12 + i * (cw + 0.2)
    cx, cy = CARD(s, xx, 0.72, cw, ch, htxt, hc, LGRAY)
    T(s, cx + 0.1, cy + 0.05, cw - 0.18, ch - 0.42, body, sz=8, col=GRAY)

# Key params row
R(s, 0.12, 3.72, 9.76, 1.6, LBLUE)
R(s, 0.12, 3.72, 9.76, 0.3, NAVY)
T(s, 0.22, 3.75, 9.55, 0.26,
  'Ключевые гиперпараметры обучения', sz=8.5, col=WHITE, bold=True)
params = [
    ('Оптимизатор', 'AdamW\nβ₁=0.9, β₂=0.999'),
    ('LR-расписание', 'CosineAnnealing\nT_max=78 эпох'),
    ('Функция потерь', 'Dice-BCE (50/50)\nклассовые веса'),
    ('Батч / GPU', '16 / NVIDIA A100\nbf16 mixed prec.'),
    ('Аугментация', 'flip, rot, масштаб\nTTA × 4 поворота'),
    ('Early stopping', 'patience = 12\nbest epoch = 78'),
]
pw = 9.76 / len(params)
for j, (k, v) in enumerate(params):
    xx = 0.12 + j * pw
    R(s, xx + 0.03, 4.04, pw - 0.06, 1.22, WHITE)
    T(s, xx + 0.08, 4.08, pw - 0.14, 0.28, k, sz=8, col=NAVY2, bold=True)
    T(s, xx + 0.08, 4.34, pw - 0.14, 0.88, v, sz=7.8, col=GRAY)

print('Slide 6 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 7 — НАУЧНАЯ НОВИЗНА
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'НАУЧНАЯ НОВИЗНА', 'Научная новизна работы — отличия от существующих исследований', 7)

T(s, 0.12, 0.72, 9.76, 0.34,
  'Новизна состоит в адаптации и интеграции апробированных методов для специфики '
  'российских арктических акваторий — ни один из трёх компонентов ранее не применялся совместно.',
  sz=8.5, col=GRAY)

novelties = [
    (NAVY, '1',
     'Трёхклассовый датасет для арктической акватории',
     'Все открытые датасеты (SOS Dataset, OSCD, MKLab) используют бинарную схему «нефть / фон».\n'
     'Введён отдельный класс «лёд + суша» — критично для Арктики: до 70 % тёмных пятен в SAR '
     'вызваны начальными формами льда (жировой, нилас, шуга), а не нефтью.'),
    (NAVY2, '2',
     'DeepLabV3+ адаптирован для одноканальных SAR-данных + scSE-блоки внимания',
     'Стандартная реализация (Bianchi 2020; Shao 2022) работает с RGB-снимками.\n'
     'Входной слой перестроен под 1-канальный VV σ⁰ (дБ). Блоки scSE подавляют спекл-шум '
     'и усиливают различимость нефть / биогенные плёнки (ключевая look-alike).'),
    (GREEN, '3',
     'Первая количественная оценка переноса модели на новые арктические порты России',
     'Модель, обученная на Кольском заливе, впервые проверена на Варандее, Сабетте и Печенге.\n'
     'Выявлена закономерность деградации: F1 = 0.89 (Кольский) → 0.84 (Варандей) → 0.76 (Сабетта). '
     'Количественно оценён рост ложных тревог (FP 1.4 % → 6.2 %).'),
]

nh = 1.28
for i, (nc, num, title, body) in enumerate(novelties):
    yy = 1.14 + i * (nh + 0.08)
    R(s, 0.12, yy, 9.76, nh, LGRAY2 if i % 2 == 0 else LGRAY)
    R(s, 0.12, yy, 0.42, nh, nc)
    T(s, 0.17, yy + nh / 2 - 0.18, 0.34, 0.36, num,
      sz=17, col=WHITE, bold=True, align=PP_ALIGN.CENTER)
    T(s, 0.62, yy + 0.06, 9.18, 0.26, title, sz=9.5, col=nc, bold=True)
    T(s, 0.62, yy + 0.3, 9.18, nh - 0.34, body, sz=8, col=GRAY)

print('Slide 7 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 8 — КОЛЬСКИЙ ЗАЛИВ (базовый кейс)
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'КЕЙС 1', 'Кольский залив — базовый порт исследования', 8)

# Left: context + incident
cx, cy = CARD(s, 0.12, 0.72, 5.1, 2.55, 'Объект и данные', NAVY, LGRAY)
ctx_items = [
    ('Акватория:', 'Кольский залив, Мурманская обл., 68.5–69.5°N'),
    ('Снимки:', '11 сцен Sentinel-1, 01.07–30.08.2024'),
    ('Метод детектирования:', 'Адаптивный порог T = μ − 1.3·σ (VV-канал)'),
    ('Клас. дисбаланс:', '~78 % вода, 19 % лёд+суша, 2.4 % нефть'),
    ('Верификация 1:', 'Метео-контроль ERA5 — ветер 3–9 м/с (оптимум)'),
    ('Верификация 2:', 'AIS-трафик — суда ≤5 км / ≤24 ч от аномалии'),
]
tb, tf = T(s, cx + 0.1, cy + 0.05, 4.85, 2.2, sz=8.5, col=GRAY)
tf.word_wrap = True
first = True
for lbl, val in ctx_items:
    if first:
        tf.paragraphs[0].alignment = PP_ALIGN.LEFT
        r = tf.paragraphs[0].add_run()
        r.text = f'{lbl} '; r.font.name = FONT
        r.font.size = Pt(8.5); r.font.bold = True; r.font.color.rgb = NAVY2
        r2 = tf.paragraphs[0].add_run()
        r2.text = val; r2.font.name = FONT
        r2.font.size = Pt(8.5); r2.font.color.rgb = GRAY
        first = False
    else:
        p = tf.add_paragraph(); p.space_before = Pt(3)
        r = p.add_run(); r.text = f'{lbl} '
        r.font.name = FONT; r.font.size = Pt(8.5)
        r.font.bold = True; r.font.color.rgb = NAVY2
        r2 = p.add_run(); r2.text = val
        r2.font.name = FONT; r2.font.size = Pt(8.5); r2.font.color.rgb = GRAY

# Incident highlight box
R(s, 0.12, 3.38, 5.1, 1.9, LAMBER)
R(s, 0.12, 3.38, 5.1, 0.3, RED2)
T(s, 0.22, 3.41, 4.9, 0.26, 'Реальный инцидент — 11 августа 2024 г.',
  sz=8.5, col=WHITE, bold=True)
T(s, 0.22, 3.72, 4.9, 1.5,
  'При бункеровке судна в порту Мурманска допущена утечка топлива.\n'
  'Тёмное пятно зафиксировано Sentinel-1 через 7 суток (18 авг.):\n'
  '1 296 пкс → 13.7 % акватории залива.\n'
  'AIS-данные подтвердили суда в зоне в момент съёмки.\n'
  'Ветер ERA5: 4.8 м/с — в пределах рабочего диапазона 3–9 м/с.',
  sz=8, col=GRAY)

# Right: results cards
cx2, cy2 = CARD(s, 5.38, 0.72, 4.5, 2.55,
                'Результаты модели (Кольский залив)', GREEN, LGREEN)
results = [
    ('F1-score (нефть)', '0.89', GREEN),
    ('mIoU (3 класса)', '0.82', NAVY),
    ('Точность (Accuracy)', '95.8 %', NAVY2),
    ('FP (ложные тревоги)', '1.4 %', ORANGE),
    ('Best epoch', '78 / 78', GRAY),
    ('Параметров модели', '41.2 М', GRAY),
]
rh = 0.37
for j, (k, v, c) in enumerate(results):
    yy2 = cy2 + 0.06 + j * rh
    bg2 = LGRAY2 if j % 2 == 0 else LGRAY
    R(s, cx2 + 0.06, yy2, 4.35, rh - 0.04, bg2)
    T(s, cx2 + 0.14, yy2 + 0.05, 2.9, 0.26, k, sz=8.5, col=GRAY)
    T(s, cx2 + 3.1, yy2 + 0.04, 1.3, 0.28, v, sz=10, col=c, bold=True,
      align=PP_ALIGN.RIGHT)

# Right bottom: transfer note
R(s, 5.38, 3.38, 4.5, 1.9, LBLUE)
R(s, 5.38, 3.38, 4.5, 0.3, NAVY2)
T(s, 5.48, 3.41, 4.3, 0.26, 'Перенос на новые порты',
  sz=8.5, col=WHITE, bold=True)
T(s, 5.48, 3.72, 4.3, 1.5,
  'Модель протестирована на трёх новых акваториях\n'
  'без дообучения (zero-shot transfer):\n\n'
  '  Варандей:  F1 = 0.84  (FP = 1.4 %)\n'
  '  Сабетта:   F1 = 0.76  (FP = 6.2 %)\n'
  '  Печенга:   тестовая сцена 2025 г.',
  sz=8.5, col=NAVY)

print('Slide 8 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 9 — ВАРАНДЕЙ + ПЕЧЕНГА
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'НОВЫЕ ПОРТЫ', 'SAR-снимки Sentinel-1: Варандей и Печенга', 9)

# Varandey — left half
R(s, 0.1, 0.72, 4.8, 4.55, LGRAY)
R(s, 0.1, 0.72, 4.8, 0.3, NAVY2)
T(s, 0.2, 0.75, 4.6, 0.26,
  'Рис. 3.4. Варандей — май 2025 / апрель 2025', sz=8, col=WHITE, bold=True)
PIC(s, 'fig_varandey.png', 0.14, 1.04, 4.72, 3.96)

# Pechenga — right half
R(s, 5.1, 0.72, 4.8, 4.55, LGRAY)
R(s, 5.1, 0.72, 4.8, 0.3, NAVY)
T(s, 5.2, 0.75, 4.6, 0.26,
  'Рис. 3.3. Печенга — февраль 2026 / август 2025', sz=8, col=WHITE, bold=True)
PIC(s, 'fig_pechenga.png', 5.14, 1.04, 4.72, 3.96)

# Bottom annotation strip
R(s, 0.1, 5.28, 9.8, 0.28, LGRAY2)
T(s, 0.18, 5.3, 9.65, 0.24,
  'Тёмные аномалии в VV-канале детектируются адаптивным порогом T = μ − k·σ (k = 1.2–1.3). '
  'Стрелки указывают на предполагаемые зоны разливов и look-alike объекты (лёд, тень).',
  sz=7, col=GRAY, italic=True)

print('Slide 9 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 10 — САБЕТТА + НОРИЛЬСК
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'НОВЫЕ ПОРТЫ', 'SAR-снимки: Сабетта и мотивирующий кейс Норильск-2020', 10)

# Sabetta — left half
R(s, 0.1, 0.72, 4.8, 4.55, LGRAY)
R(s, 0.1, 0.72, 4.8, 0.3, NAVY)
T(s, 0.2, 0.75, 4.6, 0.26,
  'Рис. 3.5. Сабетта — октябрь 2022 / декабрь 2025', sz=8, col=WHITE, bold=True)
PIC(s, 'fig_sabetta.png', 0.14, 1.04, 4.72, 3.96)

# Norilsk — right half
R(s, 5.1, 0.72, 4.8, 4.55, LGRAY)
R(s, 5.1, 0.72, 4.8, 0.3, RED2)
T(s, 5.2, 0.75, 4.6, 0.26,
  'Рис. 3.6. Норильск — 3 июня и 15 июня 2020 (после аварии НТЭК)', sz=8, col=WHITE, bold=True)
PIC(s, 'fig_norilsk.png', 5.14, 1.04, 4.72, 3.96)

# Norilsk annotation
R(s, 5.1, 5.0, 4.8, 0.27, LRED)
T(s, 5.18, 5.02, 4.65, 0.24,
  '29 мая 2020: ~21 000 т дизтоплива ТЭЦ-3 НТЭК. '
  'SAR фиксирует динамику ледохода, не плёнку — основной мониторинг вёлся Sentinel-2.',
  sz=6.8, col=RED, italic=True)

print('Slide 10 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 11 — РЕЗУЛЬТАТЫ ОБУЧЕНИЯ + ДЕГРАДАЦИЯ ПРИ ПЕРЕНОСЕ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'РЕЗУЛЬТАТЫ', 'Обучение DeepLabV3+ · Деградация F1 при переносе модели', 11)

# Training curves — left panel
R(s, 0.1, 0.72, 5.75, 4.55, LGRAY)
R(s, 0.1, 0.72, 5.75, 0.3, NAVY)
T(s, 0.2, 0.75, 5.55, 0.26, 'Кривые обучения (78 эпох) · Loss Dice-BCE · mIoU',
  sz=8, col=WHITE, bold=True)
PIC(s, 'fig_training.png', 0.14, 1.04, 5.67, 4.05)

# Ports F1 — right panel
R(s, 6.05, 0.72, 3.83, 4.55, LGRAY)
R(s, 6.05, 0.72, 3.83, 0.3, GREEN)
T(s, 6.15, 0.75, 3.63, 0.26,
  'F1 по портам · Деградация при переносе', sz=8, col=WHITE, bold=True)
PIC(s, 'fig_ports_f1.png', 6.09, 1.04, 3.75, 2.85)

# Key metrics cards below right
metrics = [
    ('mIoU = 0.82', 'тест. выборка', NAVY),
    ('F1_нефть = 0.89', 'Кольский', GREEN),
    ('Точность = 95.8%', 'accuracy', NAVY2),
]
mw = 3.83 / 3
for j, (v, k, c) in enumerate(metrics):
    xx = 6.05 + j * mw
    R(s, xx + 0.03, 3.96, mw - 0.06, 1.25, c)
    T(s, xx + 0.06, 4.02, mw - 0.1, 0.5, v, sz=9, col=WHITE, bold=True,
      align=PP_ALIGN.CENTER)
    T(s, xx + 0.06, 4.5, mw - 0.1, 0.65, k, sz=7.5, col=WHITE,
      align=PP_ALIGN.CENTER)

print('Slide 11 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 12 — СРАВНЕНИЕ С АНАЛОГАМИ + ВЫВОДЫ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'ИТОГИ', 'Сравнение с методами-аналогами · Выводы · Значимость', 12)

# Methods comparison figure — left panel
R(s, 0.1, 0.72, 5.6, 3.95, LGRAY)
R(s, 0.1, 0.72, 5.6, 0.3, NAVY)
T(s, 0.2, 0.75, 5.4, 0.26, 'Сравнение по F1-score с методами из литературы',
  sz=8, col=WHITE, bold=True)
PIC(s, 'fig_methods.png', 0.14, 1.04, 5.52, 3.45)

# Conclusions — right panel
cx, cy = CARD(s, 5.88, 0.72, 4.0, 3.95, 'Выводы', NAVY, LGRAY)
conclusions = [
    'Трёхэтапный конвейер ESA SNAP → DeepLabV3+ → ERA5/AIS успешно детектирует нефтяные разливы в Арктике',
    'Трёхклассовый датасет (1125 сцен) — первый для российских арктических акваторий',
    'F1=0.89 превосходит все аналоги: Отцу (0.71), U-Net (0.80), GLCM+CNN (0.81)',
    'Перенос модели: F1 0.89 → 0.84 → 0.76 — выявлена закономерность деградации',
]
tb, tf = T(s, cx + 0.1, cy + 0.05, 3.75, 2.52, sz=8, col=GRAY)
tf.word_wrap = True
first = True
for ci, c in enumerate(conclusions):
    if first:
        tf.paragraphs[0].alignment = PP_ALIGN.LEFT
        r = tf.paragraphs[0].add_run()
        r.text = f'•  {c}'
        r.font.name = FONT; r.font.size = Pt(7.8)
        r.font.bold = False; r.font.color.rgb = NAVY
        first = False
    else:
        p = tf.add_paragraph()
        p.space_before = Pt(4)
        r = p.add_run(); r.text = f'•  {c}'
        r.font.name = FONT; r.font.size = Pt(7.8)
        r.font.color.rgb = NAVY

# Practical significance (всё выполнено — без планов на будущее)
R(s, 5.88, 4.76, 4.0, 0.52, LGREEN)
R(s, 5.88, 4.76, 4.0, 0.24, GREEN)
T(s, 5.98, 4.78, 3.82, 0.22, 'Практическая значимость', sz=7.5, col=WHITE, bold=True)
T(s, 5.98, 5.0, 3.82, 0.25,
  'Система готова к мониторингу 4 арктических акваторий России; реализован полный конвейер',
  sz=7.5, col=GREEN)

# Bottom full-width conclusion highlight
R(s, 0.1, 4.76, 5.6, 0.52, LAMBER)
T(s, 0.2, 4.8, 5.4, 0.46,
  'Система обеспечивает автоматическое всепогодное обнаружение нефтяных разливов '
  'в арктических акваториях России со значимым превосходством над базовыми методами.',
  sz=8, col=GRAY, bold=False, italic=True)

print('Slide 12 done')


# ─── Save ────────────────────────────────────────────────────────────────────
prs.save(OUT)
print(f'\nSaved → {OUT}')
