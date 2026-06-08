# -*- coding: utf-8 -*-
"""Финальная презентация ВКР Байханова — белый фон, стиль как у Лю Цзучэна,
13 слайдов + слайд вопросов, регламент 10–12 минут."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

FIG = "/home/user/spbu_db_hw/thesis/otchet/figures"
OUT = "/home/user/spbu_db_hw/thesis/vkr_final/Презентация_Финал_Байханов_2026.pptx"
TOTAL = "14"   # слайдов (включая «Спасибо»)

# ── цвета ──────────────────────────────────────────────────────────────────
NAVY    = RGBColor(0x0B, 0x2E, 0x4F)
BLUE    = RGBColor(0x1A, 0x5E, 0xA8)
ACCENT  = RGBColor(0xD4, 0x5D, 0x0A)  # оранжевый
GREEN   = RGBColor(0x1A, 0x7A, 0x3C)
LGRAY   = RGBColor(0xF4, 0xF6, 0xF8)
MGRAY   = RGBColor(0xD0, 0xD5, 0xDD)
DGRAY   = RGBColor(0x44, 0x44, 0x44)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
BLACK   = RGBColor(0x11, 0x11, 0x11)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


# ── helpers ────────────────────────────────────────────────────────────────
def new_slide():
    return prs.slides.add_slide(BLANK)

def bg_white(s):
    from pptx.oxml.ns import qn
    from lxml import etree
    spTree = s.shapes._spTree
    bg = etree.SubElement(s.slide._element, qn("p:bg"))
    bgPr = etree.SubElement(bg, qn("p:bgPr"))
    solidFill = etree.SubElement(bgPr, qn("a:solidFill"))
    srgbClr = etree.SubElement(solidFill, qn("a:srgbClr"))
    srgbClr.set("val", "FFFFFF")

def rect(s, x, y, w, h, color, line_color=None, line_pt=None):
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    sp = s.shapes.add_shape(1, x, y, w, h)  # 1 = RECTANGLE
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line_color:
        sp.line.color.rgb = line_color
        sp.line.width = Pt(line_pt or 1)
    else:
        sp.line.fill.background()
    sp.shadow.inherit = False
    return sp

def tb(s, x, y, w, h, text, size=16, color=BLACK, bold=False,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=True,
       spacing=1.0, italic=False, font="Calibri", after=0):
    box = s.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(after)
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color; r.font.name = font
    return box

def bullet_list(s, x, y, w, h, items, size=16, color=DGRAY, gap=8,
                bold_first=False, font="Calibri"):
    box = s.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.08
        p.space_after = Pt(gap)
        p.alignment = PP_ALIGN.LEFT
        if isinstance(item, tuple):
            txt_content, level = item
            indent = "    • " if level == 1 else "        – "
        else:
            txt_content, level = item, 0
            indent = "• "
        r = p.add_run()
        r.text = indent + txt_content
        r.font.size = Pt(size - 2 if level > 0 else size)
        r.font.color.rgb = color
        r.font.name = font
        r.font.bold = bold_first and i == 0

def pic(s, path, x, y, w, h):
    from PIL import Image
    iw, ih = Image.open(path).size
    ar_b = w / h; ar_i = iw / ih
    if ar_i > ar_b:
        nw = w; nh = int(w / ar_i)
    else:
        nh = h; nw = int(h * ar_i)
    nx = x + (w - nw) // 2; ny = y + (h - nh) // 2
    return s.shapes.add_picture(path, nx, ny, nw, nh)

def footer(s, num, short_title="Автоматическое детектирование нефтяных разливов · SAR"):
    # тонкая разделительная линия
    rect(s, Inches(0.4), Inches(7.05), Inches(12.53), Pt(1), MGRAY)
    tb(s, Inches(0.4), Inches(7.1), Inches(10.5), Inches(0.32),
       f"Байханов В. К.  ·  {short_title}",
       size=10, color=RGBColor(0x88, 0x88, 0x88))
    tb(s, Inches(11.8), Inches(7.1), Inches(1.2), Inches(0.32),
       f"{num} / {TOTAL}", size=10,
       color=RGBColor(0x88, 0x88, 0x88), align=PP_ALIGN.RIGHT)

def slide_title(s, text, sub=None):
    """Цветная шапка с заголовком слайда."""
    rect(s, 0, 0, SW, Inches(1.1), NAVY)
    rect(s, 0, Inches(1.1), SW, Pt(3), ACCENT)
    tb(s, Inches(0.5), Inches(0.05), Inches(12.3), Inches(1.0),
       text, size=24, color=WHITE, bold=True,
       anchor=MSO_ANCHOR.MIDDLE)
    if sub:
        tb(s, Inches(0.5), Inches(0.75), Inches(12.3), Inches(0.3),
           sub, size=12, color=RGBColor(0xAD, 0xC8, 0xE6), italic=True)

def metric_box(s, x, y, w, h, value, label, val_color=NAVY, bg=LGRAY):
    rect(s, x, y, w, h, bg, MGRAY, 0.5)
    tb(s, x, y + Inches(0.05), w, Inches(0.7),
       value, size=36, color=val_color, bold=True,
       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, x, y + Inches(0.75), w, Inches(0.35),
       label, size=13, color=DGRAY,
       align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 1 — ТИТУЛ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
rect(s, 0, 0, SW, SH, LGRAY)
rect(s, 0, 0, Inches(0.18), SH, NAVY)
rect(s, 0, Inches(3.5), SW, Pt(2), ACCENT)

tb(s, Inches(0.45), Inches(0.5), Inches(12.4), Inches(0.45),
   "Санкт-Петербургский государственный университет",
   size=15, color=NAVY, align=PP_ALIGN.CENTER)
tb(s, Inches(0.45), Inches(0.9), Inches(12.4), Inches(0.35),
   "Магистерская программа «Искусственный интеллект и наука о данных»  ·  09.04.03",
   size=12, color=DGRAY, align=PP_ALIGN.CENTER, italic=True)

tb(s, Inches(0.7), Inches(1.55), Inches(12.0), Inches(1.85),
   "Разработка системы автоматического\nдетектирования нефтяных разливов\nв акваториях арктических портов\nпо данным спутниковой радиолокационной съёмки",
   size=28, color=NAVY, bold=True, align=PP_ALIGN.CENTER, spacing=1.15)

tb(s, Inches(0.7), Inches(4.0), Inches(12.0), Inches(0.45),
   "Выпускная квалификационная работа",
   size=16, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)

tb(s, Inches(1.5), Inches(5.0), Inches(5.0), Inches(1.1),
   "Выполнил:\nБайханов Владислав Камолович", size=15, color=BLACK)
tb(s, Inches(7.5), Inches(5.0), Inches(4.5), Inches(1.1),
   "Научный руководитель:\nк.т.н., доцент Митько А. В.", size=15, color=BLACK,
   align=PP_ALIGN.RIGHT)
tb(s, Inches(0.45), Inches(6.85), Inches(12.4), Inches(0.45),
   "Санкт-Петербург · 2026", size=13, color=DGRAY, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 2 — АКТУАЛЬНОСТЬ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "1. Актуальность")
footer(s, 2)

bullet_list(s, Inches(0.5), Inches(1.4), Inches(7.0), Inches(5.0), [
    "> 700 тыс. т углеводородов/год попадает в Мировой океан",
    "Доля Арктики растёт — рост судоходства по СМП и шельфовой добычи",
    "В Арктике нефть разлагается в 5–10 раз медленнее (+5°C)",
    "> 80 % времени — облачность и полярная ночь: оптика не работает",
    "SAR Sentinel-1 — единственный всепогодный круглосуточный инструмент",
], size=17, gap=12)

# карточки инцидентов
incidents = [
    ("Норильск\n29.05.2020", "≈21 тыс. т\nущерб 146 млрд ₽"),
    ("Кольский залив\n11.09.2024", "разлив мазута\nпри бункеровке"),
    ("Тикси\nянварь 2026", "керосин\nна льду"),
]
for i, (place, detail) in enumerate(incidents):
    x = Inches(7.65) + i * Inches(1.85)
    rect(s, x, Inches(1.45), Inches(1.7), Inches(1.35), LGRAY, MGRAY, 0.5)
    tb(s, x+Inches(0.08), Inches(1.52), Inches(1.55), Inches(0.55),
       place, size=13, color=NAVY, bold=True, spacing=1.1)
    tb(s, x+Inches(0.08), Inches(2.06), Inches(1.55), Inches(0.65),
       detail, size=12, color=ACCENT, spacing=1.05)

pic(s, f"{FIG}/fig_kola.png", Inches(7.65), Inches(3.05), Inches(5.3), Inches(3.65))


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 3 — ПРОБЛЕМА
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "2. Проблема: ложные цели (look-alikes)",
            "Нефть и природные «двойники» неотличимы по яркости на SAR")
footer(s, 3)

# левая колонка
tb(s, Inches(0.5), Inches(1.35), Inches(5.8), Inches(0.45),
   "Что выглядит как нефть:", size=17, color=NAVY, bold=True)
bullet_list(s, Inches(0.5), Inches(1.85), Inches(5.8), Inches(4.5), [
    "Начальный лёд: ледяное сало, нилас",
    "Биогенные плёнки (фитопланктон, липиды)",
    "Зоны ветровой тени (за мысами, судами)",
], size=17, gap=14)

rect(s, Inches(0.5), Inches(3.8), Inches(5.8), Inches(1.6), LGRAY, MGRAY, 0.5)
tb(s, Inches(0.65), Inches(3.95), Inches(5.5), Inches(0.35),
   "Следствие:", size=15, color=NAVY, bold=True)
tb(s, Inches(0.65), Inches(4.3), Inches(5.5), Inches(0.95),
   "до 70 % ложных срабатываний\nпри использовании пороговых методов",
   size=17, color=ACCENT, bold=True, spacing=1.1)

# правая колонка: стрелочная схема «проблема → наш ответ»
rect(s, Inches(7.0), Inches(1.35), Inches(5.9), Inches(1.0), LGRAY, MGRAY, 0.5)
tb(s, Inches(7.15), Inches(1.45), Inches(5.6), Inches(0.8),
   "Существующие решения:\nбинарная схема «нефть / фон» — лёд не выделяется",
   size=15, color=DGRAY, spacing=1.1)

# стрелка
tb(s, Inches(9.7), Inches(2.45), Inches(0.9), Inches(0.5),
   "▼", size=28, color=ACCENT, align=PP_ALIGN.CENTER)

rect(s, Inches(7.0), Inches(3.0), Inches(5.9), Inches(1.0), NAVY)
tb(s, Inches(7.15), Inches(3.1), Inches(5.6), Inches(0.8),
   "Наш ответ:\nвынести лёд в отдельный 3-й класс",
   size=16, color=WHITE, bold=True, spacing=1.1)

tb(s, Inches(7.0), Inches(4.2), Inches(5.9), Inches(0.4),
   "Вода   /   Нефть   /   Лёд + Суша",
   size=20, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)

tb(s, Inches(7.0), Inches(4.75), Inches(5.9), Inches(1.0),
   "Ни одна существующая работа для Арктики\nне использует трёхклассовую схему",
   size=15, color=NAVY, italic=True, align=PP_ALIGN.CENTER, spacing=1.1)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 4 — ЦЕЛЬ И ЗАДАЧИ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "3. Цель и задачи исследования")
footer(s, 4)

rect(s, Inches(0.5), Inches(1.35), Inches(12.3), Inches(1.25), LGRAY, MGRAY, 0.5)
tb(s, Inches(0.65), Inches(1.45), Inches(12.0), Inches(1.05),
   "Цель — автоматизация процесса детектирования нефтяных разливов в акваториях "
   "арктических портов по данным Sentinel-1 за счёт нейросетевой трёхклассовой модели, "
   "обеспечивающей F1 ≥ 0,85 для класса «нефть».",
   size=17, color=NAVY, bold=True, spacing=1.1)

tasks = [
    "1  ·  Выявить ограничения существующих методов и обосновать выбор архитектуры",
    "2  ·  Разработать методику датасета, обучить нейросетевую модель",
    "3  ·  Реализовать программный прототип-конвейер",
    "4  ·  Провести экспериментальную оценку и сравнительный анализ",
]
for i, t in enumerate(tasks):
    y = Inches(2.85) + i * Inches(0.88)
    c = NAVY if i % 2 == 0 else BLUE
    rect(s, Inches(0.5), y, Inches(12.3), Inches(0.72), LGRAY if i % 2 else WHITE,
         MGRAY, 0.5)
    rect(s, Inches(0.5), y, Inches(0.22), Inches(0.72), c)
    tb(s, Inches(0.85), y + Inches(0.08), Inches(11.8), Inches(0.55),
       t, size=17, color=c if i % 2 == 0 else NAVY, spacing=1.05)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 5 — НАУЧНАЯ НОВИЗНА
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "4. Научная новизна")
footer(s, 5)

novelties = [
    ("1", "Трёхклассовая сегментация",
     "Впервые для Арктики: вода / нефть / лёд+суша\n(все существующие работы — бинарные)"),
    ("2", "Арктический подмножество датасета",
     "13 сцен Кольского залива, размечены в QGIS 3.34\nс учётом ERA5 и AIS"),
    ("3", "Адаптация DeepLabV3+ к SAR",
     "ResNet-50 + scSE → 1-канальный вход\nDice-BCE с весами классов"),
]
for i, (n, head, body) in enumerate(novelties):
    x = Inches(0.5) + i * Inches(4.28)
    rect(s, x, Inches(1.35), Inches(3.95), Inches(5.25), LGRAY, MGRAY, 0.5)
    rect(s, x, Inches(1.35), Inches(0.5), Inches(0.6), NAVY)
    tb(s, x, Inches(1.35), Inches(0.5), Inches(0.6),
       n, size=22, color=WHITE, bold=True,
       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, x + Inches(0.55), Inches(1.42), Inches(3.35), Inches(0.55),
       head, size=16, color=NAVY, bold=True, spacing=1.0)
    tb(s, x + Inches(0.1), Inches(2.0), Inches(3.75), Inches(2.5),
       body, size=15, color=DGRAY, spacing=1.12)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 6 — КОНВЕЙЕР (АРХИТЕКТУРА)
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "5. Архитектура программного решения",
            "Трёхэтапный модульный конвейер")
footer(s, 6)

pic(s, f"{FIG}/fig_pipeline.png", Inches(0.5), Inches(1.35), Inches(7.2), Inches(5.3))

steps = [
    ("1. Предобработка\n(ESA SNAP 13)",
     "Apply Orbit → Thermal Noise Removal → Calibration σ⁰ → Lee 7×7 → Terrain Correction → log dB"),
    ("2. Сегментация\n(DeepLabV3+)",
     "ResNet-50 + scSE → 3 класса за 65 секунд"),
    ("3. Верификация",
     "Морфологический анализ + контекст AIS"),
]
for i, (head, body) in enumerate(steps):
    y = Inches(1.45) + i * Inches(1.7)
    rect(s, Inches(7.95), y, Inches(5.0), Inches(1.45), LGRAY, MGRAY, 0.5)
    rect(s, Inches(7.95), y, Inches(0.15), Inches(1.45), ACCENT)
    tb(s, Inches(8.2), y + Inches(0.1), Inches(4.6), Inches(0.55),
       head, size=15, color=NAVY, bold=True, spacing=1.05)
    tb(s, Inches(8.2), y + Inches(0.65), Inches(4.6), Inches(0.7),
       body, size=14, color=DGRAY, spacing=1.05)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 7 — ДАТАСЕТ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "6. Датасет")
footer(s, 7)

# таблица выборок
headers = ["Выборка", "Сцены", "Тайлы", "Доля"]
rows = [
    ["Обучающая", "787", "2890", "70 %"],
    ["Валидационная", "226", "826",  "20 %"],
    ["Тестовая",   "112", "412",  "10 %"],
    ["Итого",  "1 125", "4 128", "100 %"],
]
col_w = [Inches(2.4), Inches(1.2), Inches(1.2), Inches(1.1)]
col_x = [Inches(0.5), Inches(2.9), Inches(4.1), Inches(5.3)]
row_h = Inches(0.52)
# заголовок таблицы
for ci, (hd, cx, cw) in enumerate(zip(headers, col_x, col_w)):
    rect(s, cx, Inches(1.35), cw, row_h, NAVY, None)
    tb(s, cx + Inches(0.05), Inches(1.4), cw - Inches(0.1), row_h - Inches(0.05),
       hd, size=15, color=WHITE, bold=True, align=PP_ALIGN.CENTER,
       anchor=MSO_ANCHOR.MIDDLE)
for ri, row in enumerate(rows):
    y = Inches(1.87) + ri * row_h
    bg = WHITE if ri < 3 else LGRAY
    for ci, (cell, cx, cw) in enumerate(zip(row, col_x, col_w)):
        rect(s, cx, y, cw, row_h, bg, MGRAY, 0.4)
        tb(s, cx + Inches(0.05), y, cw - Inches(0.1), row_h,
           cell, size=15,
           color=ACCENT if ri == 3 else (NAVY if ci == 0 else DGRAY),
           bold=(ri == 3), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# доп. пометки
bullet_list(s, Inches(0.5), Inches(4.2), Inches(5.9), Inches(2.4), [
    "Деление 70/20/10 — на уровне сцен, не тайлов",
    "1112 сцен — MKLab Krestenitis (Средиземное море)",
    "13 сцен — собственный поднабор Кольского залива",
    "Тайлы 256×256 пикс., перекрытие 50 %",
], size=15, gap=8)

pic(s, f"{FIG}/fig_class_dist.png", Inches(6.6), Inches(1.35), Inches(6.35), Inches(5.3))


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 8 — МОДЕЛЬ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "7. Нейросетевая модель и гиперпараметры")
footer(s, 8)

# схема модели — текстовая "flow"
blocks = [
    ("Вход\n1×256×256\nσ⁰ dB", LGRAY, NAVY),
    ("ResNet-50\n+ scSE\nэнкодер", NAVY, WHITE),
    ("ASPP\nмультимасш.\nконтекст", BLUE, WHITE),
    ("Декодер\n+ апсемпл.", NAVY, WHITE),
    ("Выход\n3 класса\n256×256", LGRAY, ACCENT),
]
bw, bh, gap = Inches(2.05), Inches(1.4), Inches(0.2)
start_x = Inches(0.45)
for i, (label, bg, fg) in enumerate(blocks):
    x = start_x + i * (bw + gap)
    rect(s, x, Inches(1.5), bw, bh, bg, MGRAY if bg == LGRAY else None, 0.5)
    tb(s, x, Inches(1.5), bw, bh, label, size=14, color=fg,
       bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
    if i < 4:
        tb(s, x + bw, Inches(1.5) + Inches(0.5), gap, Inches(0.4),
           "▶", size=20, color=ACCENT, align=PP_ALIGN.CENTER)

# гиперпараметры
params = [
    ("Оптимизатор", "AdamW"),
    ("lr", "1·10⁻⁴"),
    ("Эпохи / batch", "100 / 8"),
    ("Функция потерь", "Dice-BCE"),
    ("Веса классов", "вода 0,3 · нефть 9,8 · лёд 1,2"),
    ("GPU", "RTX 3090, CUDA 12.1"),
]
for i, (k, v) in enumerate(params):
    col = i // 3; row = i % 3
    x = Inches(0.5) + col * Inches(6.4)
    y = Inches(3.25) + row * Inches(0.7)
    rect(s, x, y, Inches(6.1), Inches(0.6), LGRAY, MGRAY, 0.4)
    tb(s, x + Inches(0.1), y + Inches(0.05), Inches(2.4), Inches(0.5),
       k, size=14, color=DGRAY)
    tb(s, x + Inches(2.4), y + Inches(0.05), Inches(3.6), Inches(0.5),
       v, size=14, color=NAVY, bold=True)

pic(s, f"{FIG}/fig_training.png", Inches(0.5), Inches(5.5), Inches(12.3), Inches(1.7))


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 9 — РЕЗУЛЬТАТЫ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "8. Результаты: тестовая выборка Кольского залива",
            "412 тайлов, не участвовавших в обучении и валидации")
footer(s, 9)

# метрики — большие карточки
metrics = [
    ("F1 (нефть)", "0,89", NAVY),
    ("mIoU", "0,82", BLUE),
    ("Accuracy", "95,8 %", GREEN),
]
for i, (lbl, val, col) in enumerate(metrics):
    x = Inches(0.5) + i * Inches(2.5)
    metric_box(s, x, Inches(1.4), Inches(2.2), Inches(1.3), val, lbl, col)

# таблица по классам
cls_headers = ["Класс", "Precision", "Recall", "F1", "IoU"]
cls_rows = [
    ["Вода",        "0,98", "0,99", "0,98", "0,97"],
    ["Нефть",       "0,91", "0,87", "0,89", "0,81"],
    ["Лёд + суша",  "0,93", "0,89", "0,91", "0,84"],
    ["Среднее",     "0,94", "0,92", "0,93", "0,87"],
]
cw2 = [Inches(1.9), Inches(1.3), Inches(1.3), Inches(1.1), Inches(1.1)]
cx2 = [Inches(0.5), Inches(2.4), Inches(3.7), Inches(5.0), Inches(6.1)]
for ci, (hd, cx, cw) in enumerate(zip(cls_headers, cx2, cw2)):
    rect(s, cx, Inches(3.0), cw, Inches(0.48), NAVY)
    tb(s, cx, Inches(3.0), cw, Inches(0.48), hd,
       size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for ri, row in enumerate(cls_rows):
    y = Inches(3.48) + ri * Inches(0.5)
    bg = RGBColor(0xE8, 0xF4, 0xEB) if ri == 1 else (LGRAY if ri == 3 else WHITE)
    for ci, (cell, cx, cw) in enumerate(zip(row, cx2, cw2)):
        rect(s, cx, y, cw, Inches(0.5), bg, MGRAY, 0.3)
        tb(s, cx, y, cw, Inches(0.5), cell,
           size=13, color=ACCENT if ri == 1 and ci > 0 else (NAVY if ci == 0 else DGRAY),
           bold=(ri == 1), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

pic(s, f"{FIG}/fig_confusion.png", Inches(7.5), Inches(1.35), Inches(5.4), Inches(5.3))


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 10 — СРАВНЕНИЕ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "9. Сравнительный анализ с альтернативными методами")
footer(s, 10)

comp_h = ["Метод", "Precision", "Recall", "F1", "mIoU"]
comp_r = [
    ["Пороговый Оцу",      "0,75", "0,68", "0,71", "0,58"],
    ["Адапт. порог μ−kσ",  "0,82", "0,79", "0,80", "0,68"],
    ["GLCM + CNN",         "0,85", "0,78", "0,81", "0,69"],
    ["U-Net (бинарный)",   "0,87", "0,83", "0,85", "0,75"],
    ["DeepLabV3+ (наш)",   "0,91", "0,87", "0,89", "0,82"],
]
cw3 = [Inches(2.8), Inches(1.5), Inches(1.4), Inches(1.2), Inches(1.2)]
cx3 = [Inches(0.5), Inches(3.3), Inches(4.8), Inches(6.2), Inches(7.4)]
for ci, (hd, cx, cw) in enumerate(zip(comp_h, cx3, cw3)):
    rect(s, cx, Inches(1.4), cw, Inches(0.48), NAVY)
    tb(s, cx, Inches(1.4), cw, Inches(0.48), hd,
       size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for ri, row in enumerate(comp_r):
    y = Inches(1.88) + ri * Inches(0.55)
    bg = RGBColor(0xD4, 0xE8, 0xFF) if ri == 4 else (LGRAY if ri % 2 else WHITE)
    for ci, (cell, cx, cw) in enumerate(zip(row, cx3, cw3)):
        rect(s, cx, y, cw, Inches(0.55), bg, MGRAY, 0.3)
        tb(s, cx, y, cw, Inches(0.55), cell,
           size=13,
           color=ACCENT if ri == 4 and ci > 0 else (NAVY if ri == 4 else (NAVY if ci == 0 else DGRAY)),
           bold=(ri == 4), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

pic(s, f"{FIG}/fig_methods.png", Inches(8.85), Inches(1.4), Inches(4.1), Inches(5.3))

tb(s, Inches(0.5), Inches(5.05), Inches(8.0), Inches(0.55),
   "Прирост F1 относительно метода Оцу: +0,18  ·  Лучший результат среди всех 5 методов",
   size=15, color=ACCENT, bold=True)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 11 — ПЕРЕНОСИМОСТЬ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "10. Переносимость методики",
            "Проверка на двух дополнительных арктических портах")
footer(s, 11)

pic(s, f"{FIG}/fig_ports_f1.png", Inches(0.5), Inches(1.4), Inches(5.8), Inches(5.25))

ports = [
    ("Кольский залив\n(регион обучения)", "F1 = 0,89", NAVY),
    ("Варандей\n(Печорское море)", "F1 = 0,84", BLUE),
    ("Сабетта\n(Карское море)", "F1 = 0,76", ACCENT),
]
for i, (name, f1, col) in enumerate(ports):
    x = Inches(6.6) + i * Inches(2.25)
    rect(s, x, Inches(1.4), Inches(2.1), Inches(1.55), LGRAY, MGRAY, 0.5)
    tb(s, x + Inches(0.08), Inches(1.48), Inches(1.95), Inches(0.65),
       name, size=13, color=NAVY, spacing=1.05, bold=True)
    tb(s, x + Inches(0.08), Inches(2.1), Inches(1.95), Inches(0.45),
       f1, size=18, color=col, bold=True)

bullet_list(s, Inches(6.6), Inches(3.3), Inches(6.4), Inches(3.3), [
    "Закономерная деградация качества при удалении от региона обучения",
    "Тип ложных целей разный по портам:",
    ("Печенга — ветровые тени, биоплёнки", 1),
    ("Варандей — сезонный первогодний лёд", 1),
    ("Сабетта — жировой лёд, припай", 1),
    "Методика применима; для ледовых акваторий нужно дообучение",
], size=15, gap=8)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 12 — ОГРАНИЧЕНИЯ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "11. Ограничения и угрозы валидности")
footer(s, 12)

limits = [
    ("Обучающая выборка", "Основа — Средиземное море;\nарктических сцен только 13"),
    ("Разметка", "Один аннотатор, без\nмежэкспертного согласия"),
    ("Верификация нефти", "Только SAR + медиа;\nнет химических замеров"),
    ("Статистика", "Один запуск обучения;\nнет bootstrapping"),
    ("Переносимость", "Варандей — 6 сцен,\nСабетта — 5 сцен"),
    ("Физическая\nинтерпретация", "Нет оценки типа и\nтолщины нефтепродукта"),
]
for i, (title, body) in enumerate(limits):
    col, row = i % 3, i // 3
    x = Inches(0.5) + col * Inches(4.25)
    y = Inches(1.45) + row * Inches(2.35)
    rect(s, x, y, Inches(4.0), Inches(2.1), LGRAY, MGRAY, 0.5)
    rect(s, x, y, Inches(4.0), Inches(0.4), NAVY)
    tb(s, x + Inches(0.1), y + Inches(0.02), Inches(3.8), Inches(0.38),
       title, size=14, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, x + Inches(0.12), y + Inches(0.5), Inches(3.76), Inches(1.5),
       body, size=14, color=DGRAY, spacing=1.12)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 13 — ЗАКЛЮЧЕНИЕ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
slide_title(s, "12. Заключение")
footer(s, 13)

# карточки: задача выполнена / не выполнена
rect(s, Inches(0.5), Inches(1.4), Inches(12.3), Inches(0.75), LGRAY, MGRAY, 0.5)
tb(s, Inches(0.65), Inches(1.5), Inches(12.0), Inches(0.6),
   "Цель достигнута  ·  F1 (нефть) = 0,89  ≥  целевого 0,85  ·  Все 4 задачи решены",
   size=18, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

results = [
    ("✓", "Систематизированы ограничения 4 поколений методов;\nобоснован выбор DeepLabV3+"),
    ("✓", "Комбинированный датасет: 1125 сцен, 4128 тайлов;\nоригинальная 3-классовая разметка"),
    ("✓", "Программный прототип: 65 с/сцена;\nкод опубликован в открытом доступе"),
    ("✓", "F1=0,89; mIoU=0,82; превосходство над всеми\n4 альтернативными методами"),
]
for i, (tick, text) in enumerate(results):
    y = Inches(2.45) + i * Inches(0.88)
    rect(s, Inches(0.5), y, Inches(0.55), Inches(0.72), GREEN)
    tb(s, Inches(0.5), y, Inches(0.55), Inches(0.72),
       tick, size=20, color=WHITE, bold=True,
       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, Inches(1.05), y, Inches(11.75), Inches(0.72), LGRAY, MGRAY, 0.3)
    tb(s, Inches(1.15), y + Inches(0.05), Inches(11.5), Inches(0.65),
       text, size=15, color=DGRAY, spacing=1.05)

rect(s, Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.85), NAVY)
tb(s, Inches(0.65), Inches(6.1), Inches(12.0), Inches(0.65),
   "Практическая применимость: Росприроднадзор · МЧС · Морспасслужба · Росатом / СМП",
   size=16, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════
# СЛАЙД 14 — СПАСИБО / ВОПРОСЫ
# ══════════════════════════════════════════════════════════════════════════
s = new_slide()
rect(s, 0, 0, SW, SH, LGRAY)
rect(s, 0, 0, Inches(0.18), SH, NAVY)
rect(s, 0, Inches(3.7), SW, Pt(2), ACCENT)

tb(s, Inches(0.5), Inches(1.6), Inches(12.3), Inches(0.7),
   "Спасибо за внимание!", size=40, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
tb(s, Inches(0.5), Inches(2.5), Inches(12.3), Inches(0.55),
   "Готов ответить на вопросы", size=22, color=DGRAY, align=PP_ALIGN.CENTER)

# краткое резюме ключевых цифр
kpi = [
    ("F1\nнефть", "0,89"),
    ("mIoU", "0,82"),
    ("Accuracy", "95,8%"),
    ("Скорость\nобработки", "65 с"),
    ("Сцен\nв датасете", "1 125"),
]
for i, (lbl, val) in enumerate(kpi):
    x = Inches(1.1) + i * Inches(2.25)
    rect(s, x, Inches(4.05), Inches(2.0), Inches(1.25), WHITE, MGRAY, 0.5)
    tb(s, x, Inches(4.1), Inches(2.0), Inches(0.65),
       val, size=26, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
    tb(s, x, Inches(4.75), Inches(2.0), Inches(0.5),
       lbl, size=12, color=NAVY, align=PP_ALIGN.CENTER, spacing=1.0)

tb(s, Inches(0.5), Inches(6.1), Inches(12.3), Inches(0.35),
   "Байханов Владислав Камолович  ·  ВКР  ·  СПбГУ, 2026",
   size=12, color=RGBColor(0x88, 0x88, 0x88), align=PP_ALIGN.CENTER)


prs.save(OUT)
print(f"saved: {OUT}")
print(f"slides: {len(prs.slides._sldIdLst)}")
