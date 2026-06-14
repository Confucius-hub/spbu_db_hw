# -*- coding: utf-8 -*-
"""
Финальная презентация к защите ВКР Байханова В. К.
Шаблон смоделирован по лучшей презентации (Махамат А. К.):
белый фон, синий акцент, номера слайдов, таблицы со светло-голубой шапкой,
минимум вводных слов — максимум сути, резервные слайды (заслайды) для Q&A.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ── палитра ────────────────────────────────────────────────────────────────
NAVY      = RGBColor(0x0E, 0x24, 0x47)   # тёмный фон титула
NAVY2     = RGBColor(0x16, 0x3A, 0x6B)   # градиент титула
BLUE      = RGBColor(0x25, 0x63, 0xEB)   # акцент / заголовки
BLUE_DK   = RGBColor(0x1E, 0x40, 0xAF)
DARK      = RGBColor(0x1F, 0x29, 0x37)   # основной текст
GRAY      = RGBColor(0x6B, 0x72, 0x80)   # вторичный текст
LGRAY     = RGBColor(0x9C, 0xA3, 0xAF)
LIGHTBLUE = RGBColor(0xDB, 0xEA, 0xFE)   # шапки таблиц / карточки
CARDBG    = RGBColor(0xF3, 0xF6, 0xFC)   # фон карточек
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
OIL       = RGBColor(0xB5, 0x33, 0x1F)   # «нефть»
GREEN     = RGBColor(0x2E, 0x7D, 0x52)   # успех
TEAL      = RGBColor(0x2E, 0x7D, 0x7A)
LINE      = RGBColor(0xE2, 0xE8, 0xF0)

FIG = "/home/user/spbu_db_hw/thesis/otchet/figures/"
FONT = "Arial"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

TOTAL_MAIN = 13  # основных слайдов (1–13); после них слайд «Спасибо»


# ── низкоуровневые помощники ────────────────────────────────────────────────
def _set_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def rect(slide, l, t, w, h, color, shape=MSO_SHAPE.RECTANGLE):
    sp = slide.shapes.add_shape(shape, l, t, w, h)
    _set_fill(sp, color)
    sp.shadow.inherit = False
    return sp


def gradient_bg(slide, c1, c2):
    """Диагональный градиент во весь слайд."""
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    sp.line.fill.background()
    sp.shadow.inherit = False
    sp.fill.gradient()
    stops = sp.fill.gradient_stops
    stops[0].position = 0.0
    stops[0].color.rgb = c1
    stops[1].position = 1.0
    stops[1].color.rgb = c2
    try:
        sp.fill.gradient_angle = 45.0
    except Exception:
        pass
    return sp


def txt(slide, l, t, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        space_after=6, line=1.05, wrap=True):
    """runs: список абзацев; абзац = список (text, size, bold, color, italic)."""
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        p.space_before = Pt(0)
        p.line_spacing = line
        for (text, size, bold, color, *rest) in para:
            italic = rest[0] if rest else False
            r = p.add_run(); r.text = text
            r.font.size = Pt(size); r.font.bold = bold
            r.font.italic = italic
            r.font.name = FONT; r.font.color.rgb = color
    return tb


def bullets(slide, l, t, w, h, items, size=15, color=DARK, gap=8,
            marker="•", mcolor=BLUE, line=1.05):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.space_before = Pt(0); p.line_spacing = line
        # маркер
        rm = p.add_run(); rm.text = marker + "  "
        rm.font.size = Pt(size); rm.font.bold = True
        rm.font.name = FONT; rm.font.color.rgb = mcolor
        # текст (поддержка пар «жирная часть: остальное»)
        if isinstance(it, tuple):
            head, tail = it
            r1 = p.add_run(); r1.text = head
            r1.font.size = Pt(size); r1.font.bold = True
            r1.font.name = FONT; r1.font.color.rgb = color
            r2 = p.add_run(); r2.text = tail
            r2.font.size = Pt(size); r2.font.bold = False
            r2.font.name = FONT; r2.font.color.rgb = color
        else:
            r = p.add_run(); r.text = it
            r.font.size = Pt(size); r.font.bold = False
            r.font.name = FONT; r.font.color.rgb = color
    return tb


def _counter_pill(slide, label):
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                  SW - Inches(1.15), SH - Inches(0.55),
                                  Inches(0.85), Inches(0.34))
    _set_fill(pill, CARDBG)
    pill.line.color.rgb = LINE; pill.line.width = Pt(0.75)
    pill.shadow.inherit = False
    tf = pill.text_frame; tf.word_wrap = False
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(11); r.font.color.rgb = GRAY; r.font.name = FONT


def page_number(slide, n):
    _counter_pill(slide, f"{n} / {TOTAL_MAIN}")


def backup_num(slide, n):
    _counter_pill(slide, f"В.{n}")


def content_slide(title, n, kicker=None, counter=True):
    """Белый фон + заголовок + акцентная черта + номер."""
    slide = prs.slides.add_slide(BLANK)
    rect(slide, 0, 0, SW, SH, WHITE)
    # тонкая декоративная полоса слева сверху
    rect(slide, 0, 0, Inches(0.16), SH, BLUE)
    L = Inches(0.7)
    if kicker:
        txt(slide, L, Inches(0.34), Inches(11), Inches(0.3),
            [[(kicker.upper(), 11, True, GRAY)]])
        ty = Inches(0.62)
    else:
        ty = Inches(0.40)
    txt(slide, L, ty, Inches(12), Inches(0.8),
        [[(title, 30, True, BLUE)]])
    # подчёркивание заголовка
    rect(slide, L, ty + Inches(0.72), Inches(2.2), Pt(3), BLUE)
    if counter:
        page_number(slide, n)
    return slide


def card(slide, l, t, w, h, bg=CARDBG, border=LIGHTBLUE, accent=None):
    c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    _set_fill(c, bg)
    c.line.color.rgb = border; c.line.width = Pt(1)
    c.shadow.inherit = False
    if accent:
        rect(slide, l, t, Inches(0.09), h, accent)
    return c


def num_badge(slide, l, t, num, d=Inches(0.5), color=BLUE):
    b = slide.shapes.add_shape(MSO_SHAPE.OVAL, l, t, d, d)
    _set_fill(b, color); b.shadow.inherit = False
    tf = b.text_frame
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(num)
    r.font.size = Pt(16); r.font.bold = True
    r.font.color.rgb = WHITE; r.font.name = FONT
    return b


def add_image_fit(slide, path, l, t, max_w, max_h):
    """Вписать изображение по центру области, сохраняя пропорции."""
    from PIL import Image
    iw, ih = Image.open(path).size
    ar = iw / ih
    w = max_w; h = int(w / ar)
    if h > max_h:
        h = max_h; w = int(h * ar)
    off_l = l + (max_w - w) // 2
    off_t = t + (max_h - h) // 2
    slide.shapes.add_picture(path, off_l, off_t, width=w, height=h)


def make_table(slide, l, t, w, rows, col_w, header_size=12, body_size=12,
               row_h=Inches(0.45), first_bold=False):
    """rows[0] — шапка. col_w — доли ширины (сумма 1)."""
    ncols = len(rows[0]); nrows = len(rows)
    gtbl = slide.shapes.add_table(nrows, ncols, l, t, w, row_h * nrows).table
    gtbl.first_row = False; gtbl.horz_banding = False
    widths = [int(w * f) for f in col_w]
    for j, cw in enumerate(widths):
        gtbl.columns[j].width = cw
    for i, row in enumerate(rows):
        gtbl.rows[i].height = row_h
        for j, val in enumerate(row):
            cell = gtbl.cell(i, j)
            cell.margin_left = Inches(0.08); cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.03); cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if i == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = LIGHTBLUE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if i % 2 else CARDBG
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            r = p.add_run(); r.text = str(val)
            r.font.name = FONT
            r.font.size = Pt(header_size if i == 0 else body_size)
            r.font.bold = (i == 0) or (first_bold and j == 0)
            r.font.color.rgb = BLUE_DK if i == 0 else DARK
            # цветовая маркировка ячеек сравнения (как в современных дек)
            if i > 0:
                _vs = str(val).strip().lower()
                if _vs == "+":
                    r.font.color.rgb = GREEN; r.font.bold = True; r.font.size = Pt(body_size + 2)
                elif _vs in ("—", "-", "–"):
                    r.font.color.rgb = LGRAY; r.font.bold = True; r.font.size = Pt(body_size + 2)
                elif "частич" in _vs:
                    r.font.color.rgb = RGBColor(0xD9, 0x77, 0x06); r.font.bold = True
    return gtbl


# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 1 — ТИТУЛ (тёмный фон)
# ════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient_bg(s, NAVY, NAVY2)
# верхняя строка: вуз + дата
txt(s, Inches(0.7), Inches(0.5), Inches(8), Inches(0.6),
    [[("Санкт-Петербургский государственный университет", 13, True, WHITE)]])
pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                          SW - Inches(2.0), Inches(0.45), Inches(1.5), Inches(0.45))
_set_fill(pill, NAVY)
pill.line.color.rgb = RGBColor(0x4B, 0x6A, 0x9C); pill.line.width = Pt(1)
pill.shadow.inherit = False
p = pill.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Июнь 2026"; r.font.size = Pt(13)
r.font.color.rgb = WHITE; r.font.name = FONT
# тема (kicker)
txt(s, Inches(0.7), Inches(1.9), Inches(11.5), Inches(0.4),
    [[("ВЫПУСКНАЯ КВАЛИФИКАЦИОННАЯ РАБОТА · МАГИСТЕРСКАЯ ДИССЕРТАЦИЯ",
       12, True, RGBColor(0x8F, 0xB4, 0xF5))]])
txt(s, Inches(0.7), Inches(2.30), Inches(12.0), Inches(2.3),
    [[("Разработка системы автоматического", 28, True, WHITE)],
     [("детектирования нефтяных разливов", 28, True, WHITE)],
     [("в акваториях арктических портов", 28, True, WHITE)],
     [("по данным спутниковой радиолокационной съёмки", 28, True, WHITE)]],
    line=1.08, space_after=2)
# три колонки
cols = [
    ("Байханов\nВладислав Камолович",
     "Выпускник магистратуры,\nпрограмма «Искусственный\nинтеллект и наука о данных»", WHITE),
    ("Митько\nАрсений Валерьевич",
     "Научный руководитель,\nк.т.н., доцент", RGBColor(0xC9, 0xD6, 0xEC)),
    ("Филиппова\nНадежда Анатольевна",
     "Рецензент,\nд.т.н., профессор, МАДИ", RGBColor(0xC9, 0xD6, 0xEC)),
]
cx = [Inches(0.7), Inches(5.0), Inches(9.3)]
for (name, role, ncol), x in zip(cols, cx):
    rect(s, x, Inches(5.35), Pt(3), Inches(1.4), BLUE)
    txt(s, x + Inches(0.18), Inches(5.35), Inches(3.7), Inches(0.9),
        [[(name, 17, True, ncol)]], line=1.05, space_after=0)
    txt(s, x + Inches(0.18), Inches(6.25), Inches(3.7), Inches(1.0),
        [[(role, 12, False, RGBColor(0x9F, 0xB2, 0xD0))]], line=1.05, space_after=0)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 2 — АКТУАЛЬНОСТЬ И ПРОБЛЕМА
# Верхняя часть: 4 факта в 2 колонки; снизу — снимок Кольского на всю ширину
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Актуальность и проблема", 2)

# 4 факта в виде карточек 2×2
facts = [
    ("> 700 тыс. т/год", "углеводородов в Мировой океан\nежегодно; доля Арктики растёт", BLUE),
    ("В 5–10 раз медленнее", "разлагается нефть в холодных\nводах → долгосрочный ущерб", TEAL),
    ("> 80 % времени", "облачность и полярная ночь:\nоптические спутники бесполезны", OIL),
    ("Sentinel-1 SAR", "всепогодный круглосуточный\nмониторинг — единственный выход", GREEN),
]
cw_f = Inches(2.95); gap_f = Inches(0.18)
row_h = Inches(1.32)
positions = [
    (Inches(0.7),          Inches(1.55)),
    (Inches(0.7) + cw_f + gap_f, Inches(1.55)),
    (Inches(0.7),          Inches(1.55) + row_h + Inches(0.12)),
    (Inches(0.7) + cw_f + gap_f, Inches(1.55) + row_h + Inches(0.12)),
]
for (big, small, acc), (fx, fy) in zip(facts, positions):
    card(s, fx, fy, cw_f, row_h, bg=CARDBG, border=LIGHTBLUE, accent=acc)
    txt(s, fx + Inches(0.25), fy + Inches(0.12), cw_f - Inches(0.3), Inches(0.55),
        [[(big, 16, True, acc)]], space_after=0)
    txt(s, fx + Inches(0.25), fy + Inches(0.65), cw_f - Inches(0.3), Inches(0.65),
        [[(small, 12, False, DARK)]], line=1.1, space_after=0)

# красная плашка справа — проблема
card(s, Inches(6.75), Inches(1.55), Inches(6.1), Inches(2.76),
     bg=RGBColor(0xFD, 0xF0, 0xEE), border=RGBColor(0xF0, 0xC8, 0xC0), accent=OIL)
txt(s, Inches(7.0), Inches(1.75), Inches(5.6), Inches(0.6),
    [[("Главная проблема: ложные цели", 17, True, OIL)]], space_after=6)
txt(s, Inches(7.0), Inches(2.42), Inches(5.6), Inches(1.7),
    [[("Лёд, биоплёнки и штиль дают тёмные пятна "
       "— неотличимые от нефти на SAR-снимке. "
       "У классических методов до 70 % ложных срабатываний.\n"
       "→ Нужна трёхклассовая модель: вода / нефть / лёд+суша.",
       13.5, False, DARK)]], line=1.15, space_after=0)

# ── Снимок Кольского залива — ПОЛНАЯ ШИРИНА внизу ──────────────────────
txt(s, Inches(0.7), Inches(4.46), Inches(11.5), Inches(0.32),
    [[("Кольский залив, разлив мазута 11.09.2024 — иллюстрация работы модели (схема: слева сцена, справа сегментация)",
       11, True, GRAY)]])
add_image_fit(s, FIG + "fig_kola.png",
              Inches(0.7), Inches(4.82),
              Inches(11.95), Inches(2.35))

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 3 — ЦЕЛЬ И ЗАДАЧИ
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Цель и задачи работы", 3)
card(s, Inches(0.7), Inches(1.6), Inches(11.95), Inches(1.55),
     bg=CARDBG, border=LIGHTBLUE, accent=BLUE)
txt(s, Inches(1.0), Inches(1.75), Inches(11.4), Inches(1.3),
    [[("Цель: ", 16, True, BLUE),
      ("автоматизация детектирования нефтяных разливов в акваториях "
       "арктических портов по данным Sentinel-1 за счёт трёхклассовой "
       "нейросетевой модели семантической сегментации, обеспечивающей "
       "F1-меру для класса «нефть» не ниже 0,85.", 16, False, DARK)]],
    line=1.1, space_after=0)
txt(s, Inches(0.7), Inches(3.45), Inches(8), Inches(0.4),
    [[("Задачи:", 16, True, BLUE)]])
tasks = [
    "Выявить ограничения существующих методов и обосновать выбор архитектуры",
    "Разработать методику формирования датасета и обучить модель",
    "Реализовать программный прототип — модульный конвейер обработки",
    "Провести экспериментальную оценку и сравнительный анализ",
]
ty = Inches(3.95)
for i, t in enumerate(tasks, 1):
    num_badge(s, Inches(0.7), ty, i, d=Inches(0.5))
    txt(s, Inches(1.4), ty + Inches(0.04), Inches(11), Inches(0.5),
        [[(t, 15, False, DARK)]], anchor=MSO_ANCHOR.MIDDLE)
    ty += Inches(0.72)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 4 — СУЩЕСТВУЮЩИЕ МЕТОДЫ (таблица)
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Существующие методы и их ограничения", 4)
rows = [
    ["Метод / работа", "Тип", "Многоклассо-\nвость", "Учёт ложных\nцелей льда", "Арктич.\nданные"],
    ["Метод Оцу (2024)", "порог", "—", "—", "—"],
    ["U-Net, Krestenitis (2019)", "DL, бинарн.", "—", "—", "—"],
    ["GLCM + CNN (2025)", "текстуры", "—", "частично", "—"],
    ["DeepLabV3+ scSE (наст. работа)", "DL, 3 класса", "+", "+", "+"],
]
make_table(s, Inches(0.7), Inches(1.75), Inches(11.95), rows,
           col_w=[0.34, 0.16, 0.17, 0.18, 0.15],
           header_size=12, body_size=13, row_h=Inches(0.62))
txt(s, Inches(0.7), Inches(5.45), Inches(11.2), Inches(0.65),
    [[("Вывод: ", 14, True, BLUE),
      ("во всех аналогах — бинарная схема, нет отдельного класса льда → "
       "до 70 % ложных тревог в арктических акваториях.",
       14, False, DARK)]], line=1.05)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 5 — КОНВЕЙЕР ОБРАБОТКИ SAR-ДАННЫХ
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Конвейер обработки SAR-данных", 5)
add_image_fit(s, FIG + "fig_pipeline.png", Inches(0.4), Inches(1.5),
              Inches(12.55), Inches(5.8))

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 6 — ДАТАСЕТ И ОБУЧЕНИЕ
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Предобработка и датасет", 6)

# ── ЛЕВО: предобработка — 6 шагов SNAP ───────────────────────────────────
txt(s, Inches(0.7), Inches(1.5), Inches(5.9), Inches(0.4),
    [[("Предобработка снимка — 6 шагов (ESA SNAP)", 16, True, BLUE)]])
_pre = [
    ("Apply Orbit File", "уточнение орбиты спутника"),
    ("Thermal Noise Removal", "удаление шума сенсора"),
    ("Калибровка → σ⁰", "перевод в физическую величину"),
    ("Фильтр Ли 7×7", "подавление зернистости (спекл)"),
    ("Range-Doppler", "геопривязка к местности"),
    ("Перевод в дБ", "логарифмическая шкала яркости"),
]
_y = Inches(2.12)
for _i, (_h, _b) in enumerate(_pre, 1):
    num_badge(s, Inches(0.7), _y, _i, d=Inches(0.46), color=TEAL)
    txt(s, Inches(1.32), _y - Inches(0.02), Inches(5.3), Inches(0.55),
        [[(_h + " — ", 13.5, True, DARK), (_b, 13.5, False, GRAY)]],
        anchor=MSO_ANCHOR.MIDDLE, line=1.05)
    _y += Inches(0.74)

# ── ПРАВО: датасет + обучение ────────────────────────────────────────────
txt(s, Inches(6.9), Inches(1.5), Inches(5.8), Inches(0.4),
    [[("Датасет и обучение", 16, True, BLUE)]])
card(s, Inches(6.9), Inches(2.05), Inches(5.75), Inches(1.45),
     bg=CARDBG, border=LIGHTBLUE, accent=BLUE)
txt(s, Inches(7.15), Inches(2.18), Inches(5.4), Inches(1.25),
    [[("1125 снимков → 4128 фрагментов 256×256", 14, True, DARK)],
     [("1112 — открытый набор (переразмечен) +", 13, False, DARK)],
     [("13 — собственные снимки Кольского залива.", 13, False, DARK)],
     [("Деление 70 / 20 / 10 на уровне снимков.", 12, False, GRAY)]],
    line=1.1, space_after=1)
card(s, Inches(6.9), Inches(3.65), Inches(5.75), Inches(1.0),
     bg=RGBColor(0xFD, 0xF0, 0xEE), border=RGBColor(0xF0, 0xC8, 0xC0), accent=OIL)
txt(s, Inches(7.15), Inches(3.78), Inches(5.4), Inches(0.8),
    [[("Дисбаланс классов: ", 13.5, True, OIL),
      ("нефть < 2,4 % пикселей.", 13, False, DARK)],
     [("Решение: взвешенная Dice-BCE, вес «нефти» = 9,8.", 13, False, DARK)]],
    line=1.1, space_after=2)
txt(s, Inches(6.9), Inches(4.88), Inches(5.8), Inches(0.4),
    [[("Сходимость: лучшее mIoU = 0,84 на 78-й эпохе", 12.5, True, DARK)]])
add_image_fit(s, FIG + "fig_training.png", Inches(6.9), Inches(5.25),
              Inches(5.75), Inches(1.5))

# ── низ: модель (архитектура одной строкой) ──────────────────────────────
card(s, Inches(0.7), Inches(6.98), Inches(11.4), Inches(0.42),
     bg=CARDBG, border=LIGHTBLUE, accent=BLUE)
txt(s, Inches(0.95), Inches(7.0), Inches(11.2), Inches(0.38),
    [[("Модель: ", 11, True, BLUE),
      ("DeepLabV3+ (энкодер ResNet-50) + scSE-внимание · сегментация на 3 класса: вода / нефть / лёд+суша",
       11, False, DARK)]],
    anchor=MSO_ANCHOR.MIDDLE)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 8 — РЕЗУЛЬТАТЫ
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Результаты на тестовой выборке", 7)
metrics = [("F1 = 0,89", "класс «нефть»", BLUE),
           ("mIoU = 0,82", "средняя по классам", TEAL),
           ("95,8 %", "общая точность", GREEN)]
y = Inches(1.8)
for big, small, acc in metrics:
    card(s, Inches(0.7), y, Inches(5.3), Inches(1.15), bg=CARDBG,
         border=LIGHTBLUE, accent=acc)
    txt(s, Inches(1.05), y + Inches(0.12), Inches(4.9), Inches(0.6),
        [[(big, 26, True, acc)]], space_after=0)
    txt(s, Inches(1.05), y + Inches(0.72), Inches(4.9), Inches(0.4),
        [[(small, 13, False, GRAY)]], space_after=0)
    y += Inches(1.3)
card(s, Inches(0.7), Inches(5.75), Inches(5.3), Inches(1.05),
     bg=RGBColor(0xEC, 0xF7, 0xF0), border=RGBColor(0xC2, 0xE5, 0xD2),
     accent=GREEN)
txt(s, Inches(1.0), Inches(5.92), Inches(4.8), Inches(0.8),
    [[("Целевой критерий F1 ≥ 0,85 выполнен ✓", 15, True, GREEN)]],
    line=1.05)
# матрица ошибок справа
add_image_fit(s, FIG + "fig_confusion.png", Inches(6.4), Inches(1.7),
              Inches(6.3), Inches(5.1))

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 9 — СРАВНЕНИЕ С АНАЛОГАМИ
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Сравнение с методами-аналогами", 8)
add_image_fit(s, FIG + "fig_methods.png", Inches(0.6), Inches(1.7),
              Inches(8.0), Inches(5.3))
bullets(s, Inches(8.9), Inches(2.2), Inches(3.9), Inches(3.5),
        [("+0,18 к F1", " по сравнению с пороговым методом Оцу"),
         ("Превосходство", " над всеми 4 альтернативными методами по всем метрикам"),
         ("Прирост", " за счёт scSE-внимания и трёхклассовой схемы")],
        size=15, gap=14)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 10 — ПЕРЕНОСИМОСТЬ
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Переносимость на другие акватории", 9)
add_image_fit(s, FIG + "fig_ports_f1.png", Inches(0.6), Inches(1.7),
              Inches(8.0), Inches(5.3))
bullets(s, Inches(8.9), Inches(2.1), Inches(3.9), Inches(4.0),
        [("Кольский залив", " — F1 = 0,89 (обучение)"),
         ("Варандей", " — F1 = 0,84 (перенос)"),
         ("Сабетта", " — F1 = 0,76 (перенос)")],
        size=16, gap=14)
card(s, Inches(8.9), Inches(4.6), Inches(3.85), Inches(2.0),
     bg=CARDBG, border=LIGHTBLUE, accent=BLUE)
txt(s, Inches(9.15), Inches(4.78), Inches(3.45), Inches(1.7),
    [[("Вывод", 15, True, BLUE)],
     [("Методика принципиально применима; для тяжёлых ледовых акваторий "
       "требуется целевое дообучение.", 13, False, DARK)]],
    line=1.1, space_after=4)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙДЫ 9–11 — ЛОЖНЫЕ ЦЕЛИ: по одному порту на слайд (крупный снимок)
# ════════════════════════════════════════════════════════════════════════════
_ports = [
    (10, "Порт Печенга",      "ветровые тени и биогенные плёнки",              TEAL, FIG + "fig_pechenga.png"),
    (11, "Терминал Варандей", "первогодний дрейфующий лёд",                    BLUE, FIG + "fig_varandey.png"),
    (12, "Порт Сабетта",      "жировой и ниласовый лёд, припай — наиболее сложная акватория", OIL, FIG + "fig_sabetta.png"),
]
for _pn, _pname, _pkicker, _pacc, _pfig in _ports:
    s = content_slide(_pname, _pn, kicker=_pkicker)
    add_image_fit(s, _pfig, Inches(0.4), Inches(1.45), Inches(12.55), Inches(5.9))

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 13 — ЗАКЛЮЧЕНИЕ
# ════════════════════════════════════════════════════════════════════════════
s = content_slide("Заключение", 13)
card(s, Inches(0.7), Inches(1.6), Inches(11.95), Inches(0.95),
     bg=RGBColor(0xEC, 0xF7, 0xF0), border=RGBColor(0xC2, 0xE5, 0xD2),
     accent=GREEN)
txt(s, Inches(1.0), Inches(1.78), Inches(11.4), Inches(0.6),
    [[("Цель достигнута: ", 17, True, GREEN),
      ("F1 = 0,89 при целевом критерии ≥ 0,85. Все четыре задачи решены.",
       17, False, DARK)]], line=1.05)
done = [
    "Систематизированы ограничения методов, обоснован выбор архитектуры",
    "Создан комбинированный датасет с оригинальной трёхклассовой разметкой",
    "Реализован программный прототип-конвейер обработки SAR-сцен",
    "Экспериментально подтверждено превосходство над пороговыми методами",
]
y = Inches(2.85)
for d in done:
    txt(s, Inches(0.7), y, Inches(0.5), Inches(0.4),
        [[("✓", 17, True, GREEN)]])
    txt(s, Inches(1.2), y + Inches(0.02), Inches(11.3), Inches(0.5),
        [[(d, 15, False, DARK)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.62)
card(s, Inches(0.7), Inches(5.5), Inches(11.95), Inches(1.3),
     bg=CARDBG, border=LIGHTBLUE, accent=BLUE)
txt(s, Inches(1.0), Inches(5.68), Inches(11.4), Inches(1.0),
    [[("Практическая значимость", 15, True, BLUE)],
     [("Применимость в системах экологического мониторинга арктических "
       "портов — в интересах Росприроднадзора, МЧС, «Морспасслужбы» и "
       "мониторинга Северного морского пути.", 14, False, DARK)]],
    line=1.1, space_after=4)

# ════════════════════════════════════════════════════════════════════════════
# ПОСЛЕДНИЙ СЛАЙД — СПАСИБО ЗА ВНИМАНИЕ (без счётчика)
# ════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
gradient_bg(s, NAVY, NAVY2)
txt(s, Inches(0.9), Inches(2.7), Inches(11.5), Inches(1.2),
    [[("Спасибо за внимание!", 46, True, WHITE)]])
txt(s, Inches(0.9), Inches(3.9), Inches(11.5), Inches(0.6),
    [[("Готов ответить на ваши вопросы", 20, False,
       RGBColor(0x9F, 0xB2, 0xD0))]])
rect(s, Inches(0.9), Inches(5.0), Pt(3), Inches(1.1), BLUE)
txt(s, Inches(1.1), Inches(5.0), Inches(11), Inches(1.2),
    [[("Байханов Владислав Камолович", 16, True, WHITE)],
     [("Санкт-Петербургский государственный университет · 2026", 13, False,
       RGBColor(0x9F, 0xB2, 0xD0))]], line=1.3, space_after=4)

# ── сохранение ───────────────────────────────────────────────────────────────
out = "/home/user/spbu_db_hw/thesis/vkr_final/Презентация_Финал_Байханов_2026.pptx"
prs.save(out)
print("saved:", out, "| slides:", len(prs.slides._sldIdLst))
