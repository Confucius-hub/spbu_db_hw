#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_pptx_v2.py — 10-slide VKR defence presentation (2026).
Чистый, не перегруженный макет. Без заметок в слайдах — речь отдельным файлом.
Поток: титул → цель/задачи → нефть → данные+метод → кейсы (с источниками) →
модель → результаты → новизна/сравнение/выводы.  Белый фон, плавные fade-переходы.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image
import os

FIGS  = '/home/user/spbu_db_hw/thesis/otchet/figures'
OUT   = '/home/user/spbu_db_hw/thesis/presentation/Презентация_ВКР_2026.pptx'
SPEECH_OUT = '/home/user/spbu_db_hw/thesis/presentation/Речь_к_защите_2026.docx'

# ── Палитра ──────────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x1E, 0x3A, 0x5F)
NAVY2  = RGBColor(0x2C, 0x52, 0x82)
RED    = RGBColor(0xC5, 0x30, 0x30)
RED2   = RGBColor(0x92, 0x40, 0x0E)
GREEN  = RGBColor(0x27, 0x67, 0x49)
LBLUE  = RGBColor(0xEB, 0xF4, 0xFF)
LGRAY  = RGBColor(0xF8, 0xFA, 0xFC)
LGRAY2 = RGBColor(0xF0, 0xF4, 0xF8)
LAMBER = RGBColor(0xFF, 0xFB, 0xEB)
LRED   = RGBColor(0xFF, 0xF5, 0xF5)
LGREEN = RGBColor(0xF0, 0xFF, 0xF4)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GRAY   = RGBColor(0x4A, 0x55, 0x68)
ORANGE = RGBColor(0xD9, 0x77, 0x06)

FONT  = 'Liberation Serif'
TOTAL = 10

prs = Presentation()
prs.slide_width  = Inches(10)
prs.slide_height = Inches(5.625)
BLANK = prs.slide_layouts[6]


def sl():
    return prs.slides.add_slide(BLANK)


def fade(slide, speed='med'):
    sld = slide._element
    for ex in sld.findall(qn('p:transition')):
        sld.remove(ex)
    tr = etree.SubElement(sld, qn('p:transition'))
    tr.set('spd', speed)
    etree.SubElement(tr, qn('p:fade'))


def R(s, x, y, w, h, fill, line_col=None, line_w=None):
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


def PIC(s, fname, x, y, max_w, max_h, center=True):
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
    R(s, 0, 0, 10, 0.62, NAVY)
    R(s, 0, 0.62, 10, 0.035, RED)
    T(s, 0.12, 0.09, 1.55, 0.46, label, sz=7, col=WHITE, bold=True, wrap=False)
    R(s, 1.72, 0.11, 0.02, 0.4, WHITE)
    T(s, 1.77, 0.09, 8.1, 0.46, title, sz=13.5, col=WHITE, bold=True, wrap=False)
    T(s, 9.0, 5.32, 0.95, 0.26, f'{pg} / {TOTAL}', sz=7, col=GRAY,
      align=PP_ALIGN.RIGHT, wrap=False)


def SRC(s, text):
    T(s, 0.12, 5.33, 8.6, 0.24, 'Источник: ' + text, sz=7, col=GRAY,
      italic=True, wrap=False)


def TITLECARD(s, x, y, w, h, header, hdr_col, bg, lines, body_sz=9.5):
    R(s, x, y, w, h, bg)
    R(s, x, y, w, 0.32, hdr_col)
    T(s, x + 0.1, y + 0.04, w - 0.16, 0.26, header, sz=9, col=WHITE, bold=True)
    tb, tf = T(s, x + 0.12, y + 0.42, w - 0.22, h - 0.5, sz=body_sz, col=GRAY)
    tf.word_wrap = True
    first = True
    for item in lines:
        if isinstance(item, tuple):
            lbl, val = item
        else:
            lbl, val = None, item
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph(); p.space_before = Pt(5)
        p.alignment = PP_ALIGN.LEFT
        if lbl:
            r = p.add_run(); r.text = lbl + '  '
            r.font.name = FONT; r.font.size = Pt(body_sz)
            r.font.bold = True; r.font.color.rgb = hdr_col
        r2 = p.add_run(); r2.text = val
        r2.font.name = FONT; r2.font.size = Pt(body_sz); r2.font.color.rgb = GRAY


# Речь докладчика — пойдёт ТОЛЬКО в отдельный .docx (в слайды не вставляется)
SPEECH = {}


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 1 — ТИТУЛЬНЫЙ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
R(s, 0, 0, 10, 1.3, NAVY)
R(s, 0, 1.3, 10, 0.055, RED)

T(s, 0.35, 0.12, 9.3, 1.12,
  'Разработка системы автоматического детектирования\n'
  'нефтяных разливов в акваториях арктических портов\n'
  'по данным спутниковых радиолокационных систем',
  sz=16.5, col=WHITE, bold=True, align=PP_ALIGN.LEFT, sp_after=3)

R(s, 0.3, 1.62, 4.6, 2.55, LGRAY)
R(s, 0.3, 1.62, 4.6, 0.3, NAVY2)
T(s, 0.42, 1.66, 4.35, 0.26, 'САНКТ-ПЕТЕРБУРГСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ',
  sz=6.5, col=WHITE, bold=True)
T(s, 0.42, 2.04, 4.35, 0.28, 'Кафедра информатики', sz=9.5, col=NAVY2)
T(s, 0.42, 2.38, 4.35, 0.28, 'Направление: Прикладная информатика', sz=9.5, col=GRAY)
T(s, 0.42, 2.72, 4.35, 0.28, 'Профиль: Искусственный интеллект и наука о данных',
  sz=9.5, col=GRAY)
T(s, 0.42, 3.2, 4.35, 0.3, 'Магистерская диссертация · 2026',
  sz=10.5, col=NAVY, bold=True)

R(s, 5.1, 1.62, 4.6, 2.55, LBLUE)
R(s, 5.1, 1.62, 4.6, 0.3, NAVY)
T(s, 5.22, 1.66, 4.35, 0.26, 'СВЕДЕНИЯ ОБ АВТОРЕ', sz=6.5, col=WHITE, bold=True)
T(s, 5.22, 2.04, 4.35, 0.26, 'Подготовил:', sz=8.5, col=GRAY)
T(s, 5.22, 2.3, 4.35, 0.3, 'Байханов Владислав Камолович', sz=11.5, col=NAVY, bold=True)
T(s, 5.22, 2.62, 4.35, 0.26, 'студент группы 24.М81-мм', sz=9, col=GRAY)
T(s, 5.22, 3.0, 4.35, 0.26, 'Научный руководитель:', sz=8.5, col=GRAY)
T(s, 5.22, 3.24, 4.35, 0.35, 'к.т.н., доцент Митько А. В.', sz=10, col=NAVY)

T(s, 9.0, 5.32, 0.95, 0.26, f'1 / {TOTAL}', sz=7, col=GRAY,
  align=PP_ALIGN.RIGHT, wrap=False)

SPEECH[1] = ('Здравствуйте, уважаемые члены комиссии! Тема моей работы — разработка '
             'системы автоматического детектирования нефтяных разливов в акваториях '
             'арктических портов по данным спутниковой радиолокации. Научный '
             'руководитель — кандидат технических наук, доцент Митько Арсений Валерьевич.')
print('Slide 1 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 2 — ЦЕЛЬ И ЗАДАЧИ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'ЦЕЛЬ И ЗАДАЧИ', 'Цель и задачи исследования', 2)

R(s, 0.4, 0.95, 9.2, 0.95, LBLUE)
R(s, 0.4, 0.95, 0.12, 0.95, NAVY)
T(s, 0.65, 1.02, 9.0, 0.26, 'ЦЕЛЬ РАБОТЫ', sz=9, col=NAVY, bold=True)
T(s, 0.65, 1.28, 8.85, 0.6,
  'Создать и проверить систему, которая по снимкам Sentinel-1 автоматически находит '
  'нефтяные разливы в арктических портах и устойчива к ложным целям (лёд, штиль, биоплёнки).',
  sz=10.5, col=GRAY)

T(s, 0.4, 2.12, 9.2, 0.3, 'ЗАДАЧИ', sz=9, col=NAVY2, bold=True)
tasks = [
    'Изучить физику радиолокации нефти и систематизировать ложные цели',
    'Реализовать конвейер предобработки снимков Sentinel-1 в ESA SNAP',
    'Собрать трёхклассовый датасет: вода / нефть / лёд + суша',
    'Адаптировать и обучить нейросеть DeepLabV3+ под радарные данные',
    'Проверить перенос модели на новые порты и сравнить с аналогами',
]
ty, th = 2.45, 0.55
for i, t in enumerate(tasks):
    yy = ty + i * (th + 0.04)
    R(s, 0.4, yy, 9.2, th, LGRAY if i % 2 == 0 else LGRAY2)
    R(s, 0.4, yy, 0.55, th, NAVY if i % 2 == 0 else NAVY2)
    T(s, 0.4, yy + 0.12, 0.55, 0.32, str(i + 1), sz=16, col=WHITE, bold=True,
      align=PP_ALIGN.CENTER)
    T(s, 1.1, yy + 0.13, 8.4, 0.34, t, sz=10.5, col=GRAY)

SPEECH[2] = ('Цель работы — создать и проверить систему, которая по радарным снимкам '
             'Sentinel-1 автоматически находит нефтяные разливы и при этом не путает их '
             'с похожими тёмными пятнами. Для достижения цели я поставил пять задач: '
             'изучить физику радиолокации нефти и систематизировать ложные цели; '
             'реализовать конвейер предобработки снимков; собрать трёхклассовый датасет; '
             'адаптировать и обучить нейросеть DeepLabV3+; и проверить перенос модели на '
             'новые порты со сравнением с аналогами.')
print('Slide 2 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 3 — АКТУАЛЬНОСТЬ: НЕФТЬ В АРКТИКЕ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'АКТУАЛЬНОСТЬ', 'Нефтяные разливы в Арктике — масштаб проблемы', 3)

stats = [
    ('700+', 'тыс. тонн нефти в год\nпопадает в Мировой океан', NAVY),
    ('5–10×', 'медленнее разлагается\nнефть в воде < 5 °C', NAVY2),
    ('> 80 %', 'времени — облака и ночь:\nоптика в Арктике не видит', RED2),
]
sw = 3.07
for i, (big, txt, c) in enumerate(stats):
    xx = 0.4 + i * (sw + 0.13)
    R(s, xx, 0.95, sw, 1.55, LGRAY)
    R(s, xx, 0.95, sw, 0.06, c)
    T(s, xx, 1.12, sw, 0.6, big, sz=30, col=c, bold=True, align=PP_ALIGN.CENTER)
    T(s, xx + 0.1, 1.78, sw - 0.2, 0.65, txt, sz=9.5, col=GRAY,
      align=PP_ALIGN.CENTER)

T(s, 0.4, 2.72, 9.2, 0.3, 'ДВА ПОКАЗАТЕЛЬНЫХ СЛУЧАЯ В РОССИЙСКОЙ АРКТИКЕ',
  sz=9, col=NAVY2, bold=True)

R(s, 0.4, 3.06, 4.55, 2.05, LAMBER)
R(s, 0.4, 3.06, 4.55, 0.34, RED2)
T(s, 0.52, 3.1, 4.3, 0.28, 'Кольский залив — август 2024', sz=9.5, col=WHITE, bold=True)
T(s, 0.52, 3.5, 4.3, 1.55,
  'При бункеровке судна в порту Мурманска\n'
  'произошла утечка топлива. Тёмное пятно\n'
  'зафиксировано Sentinel-1 и заняло\n'
  'около 14 % акватории залива.',
  sz=9.5, col=GRAY)

R(s, 5.05, 3.06, 4.55, 2.05, LRED)
R(s, 5.05, 3.06, 4.55, 0.34, RED)
T(s, 5.17, 3.1, 4.3, 0.28, 'Норильск — май 2020', sz=9.5, col=WHITE, bold=True)
T(s, 5.17, 3.5, 4.3, 1.55,
  'Авария на ТЭЦ-3 НТЭК: в реки и почву\n'
  'вылилось ≈ 21 000 тонн дизтоплива.\n'
  'Крупнейший разлив в истории Арктики,\n'
  'штраф — 146 млрд рублей.',
  sz=9.5, col=GRAY)

SRC(s, 'ITOPF (2023); Росприроднадзор; данные Sentinel-1, ESA Copernicus')

SPEECH[3] = ('Почему эта тема актуальна. Ежегодно в Мировой океан попадает более '
             '700 тысяч тонн нефти, а в холодной арктической воде она разлагается в '
             '5–10 раз медленнее, поэтому ущерб особенно велик. При этом оптические '
             'спутники здесь почти бесполезны: больше 80 процентов времени мешают облака '
             'и полярная ночь. Два показательных случая в российской Арктике — разлив в '
             'Кольском заливе в августе 2024 года и крупнейшая авария в Норильске '
             'в 2020-м, когда вылилось около 21 тысячи тонн дизтоплива со штрафом '
             '146 миллиардов рублей.')
print('Slide 3 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 4 — ДАННЫЕ И МЕТОД (объединяет «Почему SAR» + датасет)
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'ДАННЫЕ И МЕТОД', 'Радиолокация Sentinel-1 и трёхклассовый датасет', 4)

# Верхняя полоса: почему радар + ложные цели
R(s, 0.4, 0.9, 9.2, 0.92, LBLUE)
R(s, 0.4, 0.9, 0.12, 0.92, NAVY)
tb, tf = T(s, 0.65, 0.95, 8.9, 0.84, sz=9.5, col=GRAY)
tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run(); r.text = 'Почему радар (SAR):  '
r.font.name = FONT; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = NAVY
r = p.add_run()
r.text = ('работает круглосуточно и сквозь облака; нефть гасит рябь (эффект Марангони) '
          '→ на снимке тёмное пятно.')
r.font.name = FONT; r.font.size = Pt(9.5); r.font.color.rgb = GRAY
p = tf.add_paragraph(); p.space_before = Pt(3)
r = p.add_run(); r.text = 'Ложные цели:  '
r.font.name = FONT; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = RED2
r = p.add_run()
r.text = ('лёд, штиль и биоплёнки дают такие же пятна (до 70 % тёмных пятен — лёд), '
          'поэтому лёд выделен в отдельный класс.')
r.font.name = FONT; r.font.size = Pt(9.5); r.font.color.rgb = GRAY

# Слева — параметры Sentinel-1
cx, cy = 0.4, 1.95
R(s, cx, cy, 4.55, 3.18, LGRAY)
R(s, cx, cy, 4.55, 0.32, NAVY)
T(s, cx + 0.1, cy + 0.04, 4.35, 0.26, 'Sentinel-1 IW GRD — параметры данных',
  sz=9, col=WHITE, bold=True)
specs = [
    ('Спутник', 'Sentinel-1, ESA Copernicus'),
    ('Диапазон · поляр.', 'C-band 5.4 ГГц · VV + VH'),
    ('Разрешение', '10 м / пиксель'),
    ('Объём', '1 125 сцен · 4 128 тайлов'),
    ('Размер тайла', '256 × 256 пикселей'),
    ('Классы', 'вода · нефть · лёд + суша'),
    ('Районы · период', '4 акватории · 2022–2025'),
]
rh = 0.37
for j, (k, v) in enumerate(specs):
    yy = cy + 0.42 + j * rh
    R(s, cx + 0.12, yy, 4.3, rh - 0.06, LGRAY2 if j % 2 == 0 else WHITE)
    T(s, cx + 0.22, yy + 0.04, 1.95, 0.3, k, sz=8.5, col=NAVY2, bold=True)
    T(s, cx + 2.2, yy + 0.04, 2.2, 0.3, v, sz=8.5, col=GRAY)

# Справа — распределение классов
R(s, 5.05, 1.95, 4.55, 3.18, LGRAY)
R(s, 5.05, 1.95, 4.55, 0.32, NAVY2)
T(s, 5.15, 1.99, 4.35, 0.26, 'Распределение классов в датасете', sz=9,
  col=WHITE, bold=True)
PIC(s, 'fig_class_dist.png', 5.12, 2.32, 4.4, 2.72)

SRC(s, 'Copernicus Open Access Hub (ESA); базовый датасет MKLab (Krestenitis et al., 2019)')

SPEECH[4] = ('Решение — радиолокация. Радар Sentinel-1 работает круглосуточно и сквозь '
             'облака, а данные бесплатны. Физика простая: нефть гасит мелкую рябь на воде '
             '— это эффект Марангони — и на снимке появляется тёмное пятно. Главная '
             'сложность в том, что такие же тёмные пятна дают молодой лёд, зоны штиля и '
             'биоплёнки — это ложные цели; до 70 процентов тёмных пятен в Арктике это лёд, '
             'а не нефть. Поэтому я собрал датасет из 1125 сцен с разрешением 10 метров и '
             'разметил его на три класса — вода, нефть и лёд с сушей, впервые выделив лёд '
             'в отдельный класс. Источник данных — Copernicus, ESA.')
print('Slide 4 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 5 — КЕЙС 1: КОЛЬСКИЙ ЗАЛИВ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'КЕЙС 1', 'Кольский залив — базовый порт исследования', 5)

R(s, 0.4, 0.95, 4.55, 4.15, LAMBER)
R(s, 0.4, 0.95, 4.55, 0.34, RED2)
T(s, 0.52, 0.99, 4.3, 0.28, 'Реальный инцидент — 11 августа 2024', sz=9.5,
  col=WHITE, bold=True)
T(s, 0.52, 1.42, 4.3, 3.5,
  'При бункеровке судна в порту Мурманска\n'
  'допущена утечка топлива.\n\n'
  'Тёмное пятно зафиксировано Sentinel-1\n'
  'через 7 суток (18 августа): около 14 %\n'
  'акватории залива.\n\n'
  'Кольский залив — главный нефтеналивной\n'
  'узел Западной Арктики (≈ 30–40 млн т/год,\n'
  'регулярные бункеровки).',
  sz=10, col=GRAY)

TITLECARD(s, 5.05, 0.95, 4.55, 4.15, 'Двойная верификация находки', GREEN, LGREEN,
          [
              ('Метео (ERA5):', 'ветер 4.8 м/с — в рабочем диапазоне '
               '3–9 м/с (не штиль и не шторм)'),
              ('Суда (AIS):', 'зафиксированы суда ≤ 5 км и ≤ 24 ч '
               'от аномалии в момент съёмки'),
              ('Метод детектирования:', 'адаптивный порог по VV-каналу '
               'T = μ − 1.3·σ; подтверждён нейросетью'),
              ('Вывод:', 'аномалия классифицирована как нефтяной разлив, '
               'а не ложная цель'),
          ], body_sz=10)

SRC(s, 'Sentinel-1 (ESA); метеореанализ ERA5 (ECMWF); судовой трафик AIS')

SPEECH[5] = ('Первый и основной кейс — Кольский залив, главный нефтяной узел западной '
             'Арктики. В августе 2024 года при бункеровке судна произошла утечка '
             'топлива. Sentinel-1 зафиксировал тёмное пятно, занявшее около 14 процентов '
             'акватории. Чтобы убедиться, что это именно нефть, а не двойник, я применил '
             'двойную проверку: метеоданные ERA5 показали рабочий ветер 4.8 метра в '
             'секунду, а данные судового трафика AIS подтвердили суда в зоне в момент '
             'съёмки.')
print('Slide 5 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 6 — КЕЙС 2: ВАРАНДЕЙ + ПЕЧЕНГА
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'КЕЙС 2', 'Новые порты: Варандей и Печенга (снимки Sentinel-1)', 6)

R(s, 0.3, 0.95, 4.7, 4.05, LGRAY)
R(s, 0.3, 0.95, 4.7, 0.3, NAVY2)
T(s, 0.4, 0.99, 4.5, 0.26, 'Варандей — нефтеналивной терминал НАО', sz=8.5,
  col=WHITE, bold=True)
PIC(s, 'fig_varandey.png', 0.34, 1.3, 4.62, 3.5)

R(s, 5.05, 0.95, 4.7, 4.05, LGRAY)
R(s, 5.05, 0.95, 4.7, 0.3, NAVY)
T(s, 5.15, 0.99, 4.5, 0.26, 'Печенга — порт Мурманской области', sz=8.5,
  col=WHITE, bold=True)
PIC(s, 'fig_pechenga.png', 5.09, 1.3, 4.62, 3.5)

T(s, 0.3, 5.05, 9.4, 0.26,
  'Тёмные аномалии в VV-канале выделяются автоматически; стрелки — зоны разливов и '
  'ложные цели (лёд, тень).', sz=8, col=GRAY, italic=True, wrap=False)
SRC(s, 'Sentinel-1 IW GRD, ESA Copernicus (2025)')

SPEECH[6] = ('Далее я проверил метод на новых портах — слева нефтеналивной терминал '
             'Варандей, справа порт Печенга. На обоих снимках видны тёмные аномалии, '
             'которые система выделяет автоматически. Все снимки — Sentinel-1, ESA.')
print('Slide 6 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 7 — КЕЙС 3: САБЕТТА + НОРИЛЬСК
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'КЕЙС 3', 'Сабетта и мотивирующий случай Норильск-2020', 7)

R(s, 0.3, 0.95, 4.7, 3.75, LGRAY)
R(s, 0.3, 0.95, 4.7, 0.3, NAVY)
T(s, 0.4, 0.99, 4.5, 0.26, 'Сабетта — ворота арктического СПГ (Обская губа)',
  sz=8.5, col=WHITE, bold=True)
PIC(s, 'fig_sabetta.png', 0.34, 1.3, 4.62, 3.25)

R(s, 5.05, 0.95, 4.7, 3.75, LGRAY)
R(s, 5.05, 0.95, 4.7, 0.3, RED2)
T(s, 5.15, 0.99, 4.5, 0.26, 'Норильск — 3 и 15 июня 2020 (после аварии НТЭК)',
  sz=8.5, col=WHITE, bold=True)
PIC(s, 'fig_norilsk.png', 5.09, 1.3, 4.62, 3.25)

R(s, 0.3, 4.78, 9.45, 0.46, LRED)
T(s, 0.42, 4.8, 9.25, 0.42,
  'Важно: разлив в Норильске был на суше и реках — его отслеживали по оптике '
  'Sentinel-2; радар здесь показывает ледовую обстановку, а не плёнку нефти.',
  sz=8.5, col=RED, italic=True)
SRC(s, 'Sentinel-1 / Sentinel-2, ESA Copernicus; Росприроднадзор (2020)')

SPEECH[7] = ('Третий блок — Сабетта, ворота арктического СПГ, и мотивирующий случай '
             'Норильска. Здесь важно быть честным перед комиссией: разлив в Норильске '
             'произошёл на суше и в реках, поэтому его отслеживали по оптике Sentinel-2, '
             'а радар показывает ледовую обстановку, а не саму плёнку нефти. Этот случай '
             'как раз объясняет, зачем нужен надёжный всепогодный мониторинг.')
print('Slide 7 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 8 — МОДЕЛЬ DeepLabV3+
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'МОДЕЛЬ', 'Нейросеть DeepLabV3+, адаптированная под SAR', 8)

cw, ch = 3.05, 3.05
cards8 = [
    (NAVY, 'Энкодер ResNet-50',
     'Предобучен на ImageNet\n\n'
     '•  вход перестроен под 1 канал\n   (VV, дБ)\n'
     '•  дилатированные свёртки\n'
     '•  выходной страйд 16'),
    (NAVY2, 'ASPP — контекст',
     'Atrous Spatial Pyramid Pooling\n\n'
     '•  ветви r = 6, 12, 18\n'
     '•  глобальный pooling\n'
     '•  объекты разного масштаба:\n   от пикселя до пятна'),
    (GREEN, 'Декодер + внимание scSE',
     '3 класса на выходе\n\n'
     '•  scSE подавляет спекл-шум\n'
     '•  усиливает нефтяные пятна\n'
     '•  потери Dice-BCE\n'
     '•  веса классов 0.3 / 9.8 / 1.2'),
]
for i, (hc, htxt, body) in enumerate(cards8):
    xx = 0.4 + i * (cw + 0.18)
    R(s, xx, 0.95, cw, ch, LGRAY)
    R(s, xx, 0.95, cw, 0.34, hc)
    T(s, xx + 0.1, 0.99, cw - 0.18, 0.28, htxt, sz=9.5, col=WHITE, bold=True)
    T(s, xx + 0.14, 1.42, cw - 0.24, ch - 0.5, body, sz=9.5, col=GRAY)

R(s, 0.4, 4.2, 9.2, 0.9, LBLUE)
R(s, 0.4, 4.2, 0.12, 0.9, NAVY)
T(s, 0.62, 4.26, 9.0, 0.26, 'Обучение', sz=9, col=NAVY, bold=True)
T(s, 0.62, 4.52, 9.0, 0.5,
  'Оптимизатор AdamW  ·  78 эпох (CosineAnnealing)  ·  батч 16, GPU A100  ·  '
  'аугментация + TTA ×4  ·  41.2 млн параметров',
  sz=10, col=GRAY)

SPEECH[8] = ('Для автоматического распознавания я адаптировал нейросеть DeepLabV3+. '
             'Энкодер ResNet-50 перестроен под одноканальные радарные данные, блок ASPP '
             'улавливает объекты разного масштаба, а блоки внимания scSE подавляют шум и '
             'усиливают нефтяные пятна. Поскольку нефти на снимках очень мало, обучение '
             'шло с балансировкой классов и комбинированной функцией потерь Dice-BCE.')
print('Slide 8 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 9 — РЕЗУЛЬТАТЫ МОДЕЛИ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'РЕЗУЛЬТАТЫ', 'Результаты модели: метрики и перенос на новые порты', 9)

R(s, 0.3, 0.95, 5.35, 4.15, LGRAY)
R(s, 0.3, 0.95, 5.35, 0.3, NAVY)
T(s, 0.4, 0.99, 5.15, 0.26, 'Кривые обучения (78 эпох): потери и mIoU', sz=8.5,
  col=WHITE, bold=True)
PIC(s, 'fig_training.png', 0.34, 1.32, 5.27, 3.65)

metrics = [
    ('95.8 %', 'Точность (accuracy)', NAVY),
    ('0.82', 'mIoU (3 класса)', NAVY2),
    ('0.89', 'F1 по нефти (Кольский)', GREEN),
]
for j, (v, k, c) in enumerate(metrics):
    yy = 0.95 + j * 0.92
    R(s, 5.75, yy, 3.85, 0.84, LGRAY)
    R(s, 5.75, yy, 0.12, 0.84, c)
    T(s, 5.95, yy + 0.06, 1.6, 0.7, v, sz=24, col=c, bold=True,
      anchor=MSO_ANCHOR.MIDDLE)
    T(s, 7.5, yy + 0.06, 2.05, 0.7, k, sz=9.5, col=GRAY,
      anchor=MSO_ANCHOR.MIDDLE)

R(s, 5.75, 3.72, 3.85, 1.38, LBLUE)
R(s, 5.75, 3.72, 3.85, 0.3, NAVY2)
T(s, 5.85, 3.76, 3.65, 0.26, 'Перенос без дообучения (zero-shot)', sz=8.5,
  col=WHITE, bold=True)
T(s, 5.9, 4.08, 3.6, 1.0,
  'Кольский:   F1 = 0.89   (FP 1.4 %)\n'
  'Варандей:  F1 = 0.84   (FP 1.4 %)\n'
  'Сабетта:    F1 = 0.76   (FP 6.2 %)',
  sz=10, col=NAVY)

SPEECH[9] = ('Главные результаты. На Кольском заливе модель достигла точности 95.8 '
             'процента, mIoU 0.82 и F1 по нефти 0.89. Кривые обучения слева показывают '
             'устойчивую сходимость без переобучения. При переносе на другие порты без '
             'дообучения качество ожидаемо снижается: Варандей — 0.84, Сабетта — 0.76. '
             'Я количественно оценил эту деградацию — это один из ключевых результатов '
             'работы.')
print('Slide 9 done')


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 10 — НОВИЗНА, СРАВНЕНИЕ И ВЫВОДЫ
# ═══════════════════════════════════════════════════════════════════════════════
s = sl()
R(s, 0, 0, 10, 5.625, WHITE)
HDR(s, 'ИТОГИ', 'Научная новизна, сравнение и выводы', 10)

# Слева — 3 пункта новизны
T(s, 0.4, 0.88, 5.0, 0.28, 'НАУЧНАЯ НОВИЗНА', sz=9, col=NAVY, bold=True)
novelties = [
    (NAVY, '1', 'Трёхклассовый датасет для Арктики',
     'Впервые лёд выделен в отдельный класс — до 70 % тёмных пятен это лёд, а не нефть.'),
    (NAVY2, '2', 'DeepLabV3+ под одноканальный SAR',
     'Вход и блоки внимания scSE адаптированы под радар вместо RGB-снимков.'),
    (GREEN, '3', 'Оценка переноса между портами',
     'Впервые измерена деградация качества при переходе на новые акватории России.'),
]
nh = 1.08
for i, (nc, num, title, body) in enumerate(novelties):
    yy = 1.2 + i * (nh + 0.08)
    R(s, 0.4, yy, 5.0, nh, LGRAY if i % 2 == 0 else LGRAY2)
    R(s, 0.4, yy, 0.5, nh, nc)
    T(s, 0.4, yy + nh / 2 - 0.22, 0.5, 0.44, num, sz=20, col=WHITE, bold=True,
      align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    T(s, 1.05, yy + 0.1, 4.25, 0.3, title, sz=10, col=nc, bold=True)
    T(s, 1.05, yy + 0.42, 4.25, nh - 0.46, body, sz=9, col=GRAY)

# Справа — сравнение с аналогами
R(s, 5.55, 0.88, 4.05, 3.62, LGRAY)
R(s, 5.55, 0.88, 4.05, 0.3, GREEN)
T(s, 5.65, 0.92, 3.85, 0.26, 'Сравнение по F1 с аналогами', sz=8.5,
  col=WHITE, bold=True)
PIC(s, 'fig_methods.png', 5.6, 1.24, 3.95, 3.2)

# Нижняя полоса — выводы и значимость
R(s, 0.4, 4.6, 9.2, 0.62, LGREEN)
R(s, 0.4, 4.6, 0.12, 0.62, GREEN)
tb, tf = T(s, 0.62, 4.63, 9.0, 0.58, sz=9, col=GRAY)
tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run(); r.text = 'Выводы:  '
r.font.name = FONT; r.font.size = Pt(9); r.font.bold = True; r.font.color.rgb = GREEN
r = p.add_run()
r.text = ('реализован полный конвейер (SNAP → DeepLabV3+ → ERA5/AIS); собран первый '
          'трёхклассовый датасет Арктики; F1 = 0.89 — выше всех аналогов.')
r.font.name = FONT; r.font.size = Pt(9); r.font.color.rgb = GRAY
p = tf.add_paragraph(); p.space_before = Pt(2)
r = p.add_run(); r.text = 'Значимость:  '
r.font.name = FONT; r.font.size = Pt(9); r.font.bold = True; r.font.color.rgb = GREEN
r = p.add_run()
r.text = 'система готова к всепогодному мониторингу четырёх арктических акваторий России.'
r.font.name = FONT; r.font.size = Pt(9); r.font.color.rgb = GRAY

SRC(s, 'Сравнение: Otsu; U-Net; GLCM+CNN; адаптивный порог (по данным литературы)')

SPEECH[10] = ('Научная новизна состоит в трёх вещах: первый трёхклассовый датасет для '
              'российской Арктики с отдельным классом льда; адаптация DeepLabV3+ под '
              'одноканальный радар; и первая количественная оценка переноса модели между '
              'портами. По метрике F1 мой метод превосходит все аналоги из литературы. '
              'В итоге создан полный рабочий конвейер — от обработки снимка до проверки по '
              'метео и судовым данным — готовый к мониторингу четырёх арктических '
              'акваторий России. Спасибо за внимание, готов ответить на вопросы.')
print('Slide 10 done')


# ─── Только переходы (без заметок в слайдах) ──────────────────────────────────
for slide in prs.slides:
    fade(slide)

prs.save(OUT)
print(f'\nSaved → {OUT}')


# ─── Отдельный файл с речью (.docx) ───────────────────────────────────────────
def build_speech_docx():
    from docx import Document
    from docx.shared import Pt as DPt, Cm, RGBColor as DRGB
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn as dqn

    titles = {
        1: 'Слайд 1 — Титульный',
        2: 'Слайд 2 — Цель и задачи',
        3: 'Слайд 3 — Актуальность',
        4: 'Слайд 4 — Данные и метод',
        5: 'Слайд 5 — Кейс 1: Кольский залив',
        6: 'Слайд 6 — Кейс 2: Варандей и Печенга',
        7: 'Слайд 7 — Кейс 3: Сабетта и Норильск',
        8: 'Слайд 8 — Модель DeepLabV3+',
        9: 'Слайд 9 — Результаты модели',
        10: 'Слайд 10 — Новизна, сравнение и выводы',
    }
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.5); sec.right_margin = Cm(1.5)
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = DPt(13)
    style.element.rPr.rFonts.set(dqn('w:eastAsia'), 'Times New Roman')

    h = doc.add_paragraph(); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run('Речь к защите магистерской диссертации')
    r.font.name = 'Times New Roman'; r.font.size = DPt(15); r.font.bold = True
    sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run('Детектирование нефтяных разливов в арктических портах по данным '
                    'Sentinel-1  ·  ≈ 6 минут')
    r.font.name = 'Times New Roman'; r.font.size = DPt(11); r.font.italic = True
    doc.add_paragraph()

    for i in range(1, TOTAL + 1):
        ph = doc.add_paragraph()
        ph.paragraph_format.space_before = DPt(8)
        ph.paragraph_format.space_after = DPt(2)
        r = ph.add_run(titles[i])
        r.font.name = 'Times New Roman'; r.font.size = DPt(12); r.font.bold = True
        r.font.color.rgb = DRGB(0x1E, 0x3A, 0x5F)
        pb = doc.add_paragraph()
        pb.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pb.paragraph_format.line_spacing = 1.3
        pb.paragraph_format.space_after = DPt(4)
        r = pb.add_run(SPEECH[i])
        r.font.name = 'Times New Roman'; r.font.size = DPt(13)

    doc.save(SPEECH_OUT)
    print(f'Saved → {SPEECH_OUT}')


build_speech_docx()
