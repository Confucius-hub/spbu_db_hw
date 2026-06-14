# -*- coding: utf-8 -*-
"""Builds the defense presentation (.pptx), light-academic style, 11 slides."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image
import os

FIG = '/home/user/spbu_db_hw/thesis/otchet/figures'
OUT = '/home/user/spbu_db_hw/thesis/presentation/Презентация_арктические_порты.pptx'

# palette
NAVY = RGBColor(0x1f,0x4e,0x79)
DARK = RGBColor(0x22,0x28,0x30)
GRAY = RGBColor(0x55,0x5b,0x63)
RED  = RGBColor(0xb0,0x24,0x18)
GREEN= RGBColor(0x2d,0x6a,0x4f)
LGRAY= RGBColor(0xe9,0xed,0xf2)
WHITE= RGBColor(0xff,0xff,0xff)
FONT = 'Times New Roman'

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
blank = prs.slide_layouts[6]

def slide():
    return prs.slides.add_slide(blank)

def rect(s, x, y, w, h, color, line=None):
    from pptx.enum.shapes import MSO_SHAPE
    sp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(0.75)
    sp.shadow.inherit = False
    return sp

def txt(s, x, y, w, h, text, size=18, color=DARK, bold=False, italic=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=FONT, sp_after=4):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    lines = text.split('\n')
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(sp_after)
        r = p.add_run(); r.text = ln
        f = r.font; f.size=Pt(size); f.bold=bold; f.italic=italic
        f.name=font; f.color.rgb=color
    return tb

def bullets(s, x, y, w, h, items, size=17, color=DARK, gap=6):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame; tf.word_wrap=True
    for i,(lvl,t) in enumerate(items):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.level = lvl; p.space_after = Pt(gap); p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = ('•  ' if lvl==0 else '–  ')+t
        f = r.font; f.size=Pt(size if lvl==0 else size-2); f.name=FONT
        f.color.rgb = color; f.bold = (lvl==0 and t.endswith(':'))
    return tb

def header(s, title, num):
    rect(s, 0, 0, SW, Inches(1.02), NAVY)
    rect(s, 0, Inches(1.02), SW, Pt(3), RED)
    txt(s, Inches(0.45), Inches(0.12), Inches(11.8), Inches(0.8), title,
        size=26, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    # footer
    txt(s, Inches(0.45), Inches(7.05), Inches(8), Inches(0.4),
        'В. К. Байханов · СПбГУ · 2026', size=10, color=GRAY)
    txt(s, Inches(12.4), Inches(7.05), Inches(0.7), Inches(0.4), str(num),
        size=11, color=GRAY, align=PP_ALIGN.RIGHT)

def pic_fit(s, path, x, y, max_w, max_h, align_center=True):
    iw, ih = Image.open(path).size
    ar = iw/ih; box_ar = max_w/max_h
    if ar > box_ar:
        w = max_w; h = int(max_w/ar)
    else:
        h = max_h; w = int(max_h*ar)
    px = x + (max_w-w)//2 if align_center else x
    py = y + (max_h-h)//2 if align_center else y
    s.shapes.add_picture(path, px, py, width=w, height=h)
    return px, py, w, h

def caption(s, x, y, w, text):
    txt(s, x, y, w, Inches(0.35), text, size=11, color=GRAY, italic=True,
        align=PP_ALIGN.CENTER)

# ════════════════════════ SLIDE 1 — TITLE ════════════════════════
s = slide()
rect(s, 0, 0, SW, SH, WHITE)
rect(s, 0, 0, SW, Inches(0.32), NAVY)
rect(s, 0, SH-Inches(0.32), SW, Inches(0.32), NAVY)
rect(s, 0, Inches(2.55), SW, Pt(2.5), RED)
txt(s, Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.5),
    'Санкт-Петербургский государственный университет', size=16, color=GRAY,
    align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(1.25), Inches(11.7), Inches(1.3),
    'Разработка системы автоматического детектирования нефтяных разливов\n'
    'в акваториях арктических портов по данным спутниковых систем',
    size=27, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(3.0), Inches(11.7), Inches(0.6),
    'Магистерская диссертация · Прикладная информатика (ИИ и наука о данных)',
    size=15, color=DARK, italic=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(4.2), Inches(11.7), Inches(1.4),
    'Выполнил: Байханов Владислав Камолович\n'
    'Научный руководитель: к.т.н., доцент Митько А. В.\n'
    'Рецензент: д.т.н., проф. Филиппова Н. А. (МАДИ)',
    size=16, color=DARK, align=PP_ALIGN.CENTER, sp_after=8)
txt(s, Inches(0.8), Inches(6.4), Inches(11.7), Inches(0.5),
    'Санкт-Петербург · 2026', size=14, color=GRAY, align=PP_ALIGN.CENTER)

# ════════════════════════ SLIDE 2 — ACTUALITY / NORILSK ════════════════════════
s = slide(); header(s, 'Актуальность: нефтяные риски в Арктике', 2)
bullets(s, Inches(0.45), Inches(1.3), Inches(6.0), Inches(5.4), [
    (0,'Рост грузопотока СМП: 37,9 млн т (2024) → больше операций'),
    (0,'перевалки и бункеровки в портах Мурманск, Сабетта, Дудинка.'),
    (0,'Кольский залив, 2024: два разлива мазута за сезон,'),
    (1,'источник не установлен своевременно.'),
    (0,'Норильск, 29.05.2020: авария ТЭЦ-3 «Норникеля»,'),
    (1,'≈21 тыс. т дизеля; Далдыкан → Амбарная → оз. Пясино;'),
    (1,'ущерб 146–148 млрд руб.'),
    (0,'Оптика (Sentinel-2) и полярная ночь не дают круглосуточный'),
    (1,'мониторинг; облачность > 80 % времени.'),
    (0,'SAR (Sentinel-1, C-диапазон) — всепогодный круглосуточный'),
    (1,'инструмент наблюдения акваторий.'),
])
px,py,w,h = pic_fit(s, f'{FIG}/fig_norilsk.png', Inches(6.7), Inches(1.5),
                    Inches(6.4), Inches(4.6))
caption(s, Inches(6.7), Emu(py+h)+Pt(2), Inches(6.4),
        'Норильск-2020: на SAR доминирует сезонная динамика «лёд → вода»,\n'
        'а не плёнка дизеля (мониторинг вёлся оптикой Sentinel-2).')

# ════════════════════════ SLIDE 3 — GOAL / NOVELTY ════════════════════════
s = slide(); header(s, 'Цель работы и научная новизна', 3)
txt(s, Inches(0.45), Inches(1.25), Inches(12.4), Inches(0.8),
    'Цель: разработать систему автоматического детектирования нефтяных разливов в '
    'акваториях арктических портов по данным Sentinel-1, устойчивую к арктическим '
    'ложным целям.', size=18, color=DARK, bold=False)
rect(s, Inches(0.45), Inches(2.5), Inches(12.45), Pt(1.5), LGRAY)
txt(s, Inches(0.45), Inches(2.65), Inches(12), Inches(0.4),
    'Научная новизна:', size=19, color=NAVY, bold=True)
bullets(s, Inches(0.45), Inches(3.25), Inches(12.4), Inches(3.6), [
    (0,'Трёхклассовая схема разметки SAR: «вода» / «нефть» / «лёд + суша» —'),
    (1,'впервые лёд выделен в отдельный класс (в публичных датасетах — бинарно).'),
    (0,'Адаптация DeepLabV3+ к одноканальным SAR-данным VV:'),
    (1,'энкодер ResNet-50 + блоки внимания scSE для подавления спекл-шума.'),
    (0,'Интегрированный конвейер с трёхуровневой верификацией:'),
    (1,'морфология + метео-контроль ERA5 + сопоставление с АИС судов.'),
])

# ════════════════════════ SLIDE 4 — PHYSICS / LOOK-ALIKES ════════════════════════
s = slide(); header(s, 'Физика SAR и проблема ложных целей', 4)
bullets(s, Inches(0.45), Inches(1.3), Inches(6.2), Inches(5.2), [
    (0,'Эффект Марангони: нефтяная плёнка гасит капиллярные'),
    (1,'волны → σ⁰ падает на 10–20 дБ → тёмное пятно.'),
    (0,'Но до 70 % тёмных пятен — НЕ нефть (look-alikes):'),
    (1,'начальные формы льда (жировой, нилас, шуга);'),
    (1,'ветровые тени (зоны штиля);'),
    (1,'биогенные плёнки фитопланктона.'),
    (0,'Тёмное пятно — необходимый, но НЕ достаточный'),
    (1,'признак нефти.'),
    (0,'Ключ к разделению — поляризационная разность'),
    (1,'PD = σ⁰_VV − σ⁰_VH и контекст (нейросеть):'),
    (1,'нефть 6–10 дБ; молодой лёд < 4 дБ.'),
])
# right: mini comparison table
rect(s, Inches(7.0), Inches(1.5), Inches(5.9), Inches(4.3), LGRAY)
txt(s, Inches(7.0), Inches(1.6), Inches(5.9), Inches(0.45),
    'Сравнение тёмных сигнатур в SAR', size=16, color=NAVY, bold=True,
    align=PP_ALIGN.CENTER)
rows = [['Объект','σ⁰ VV','PD (VV−VH)'],
        ['Нефтяная плёнка','низкий','6–10 дБ'],
        ['Молодой лёд (нилас)','низкий','< 4 дБ'],
        ['Ветровая тень','низкий','2–5 дБ'],
        ['Открытая вода','средний','3–6 дБ']]
ty = 2.15
for i,row in enumerate(rows):
    for j,cell in enumerate(row):
        cx = Inches(7.15)+Inches(j*1.95)
        col = NAVY if i==0 else (RED if i==1 else DARK)
        txt(s, cx, Inches(ty), Inches(1.95), Inches(0.4), cell,
            size=13.5, color=(WHITE if i==0 else col), bold=(i==0 or i==1),
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i==0:
        rect(s, Inches(7.15), Inches(ty), Inches(5.7), Inches(0.42), NAVY)
        for j,cell in enumerate(row):
            cx = Inches(7.15)+Inches(j*1.95)
            txt(s, cx, Inches(ty), Inches(1.95), Inches(0.42), cell,
                size=13.5, color=WHITE, bold=True, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    ty += 0.62

# ════════════════════════ SLIDE 5 — PECHENGA + VARANDEY ════════════════════════
s = slide(); header(s, 'Контрольные полигоны: Печенга и Варандей', 5)
txt(s, Inches(0.45), Inches(1.15), Inches(12.4), Inches(0.5),
    'Разливов в 2022–2025 гг. не было → все тёмные зоны заведомо ложные цели '
    '(нулевая гипотеза для проверки специфичности).', size=14, color=GRAY, italic=True)
p1=pic_fit(s, f'{FIG}/fig_pechenga.png', Inches(0.4), Inches(1.75), Inches(6.2), Inches(4.4))
p2=pic_fit(s, f'{FIG}/fig_varandey.png', Inches(6.85), Inches(1.75), Inches(6.2), Inches(4.4))
caption(s, Inches(0.4), Inches(6.25), Inches(6.2),
        'Печенга: ветровые тени и биогенные плёнки (безлёдный тип).')
caption(s, Inches(6.85), Inches(6.25), Inches(6.2),
        'Варандей: сезонный первогодний лёд имитирует нефть.')

# ════════════════════════ SLIDE 6 — SABETTA + TABLE ════════════════════════
s = slide(); header(s, 'Контрольный полигон: Сабетта (тяжёлый лёд)', 6)
p=pic_fit(s, f'{FIG}/fig_sabetta.png', Inches(0.4), Inches(1.3), Inches(7.3), Inches(5.4))
caption(s, Inches(0.4), Inches(6.72), Inches(7.3),
        'Жировой/ниласовый лёд и припай — сильнейшие двойники нефти.')
# right summary
txt(s, Inches(8.0), Inches(1.4), Inches(5.0), Inches(0.5),
    'Полный спектр ложных целей:', size=17, color=NAVY, bold=True)
data=[['Печенга','ветер, биоплёнки'],
      ['Варандей','сезонный лёд'],
      ['Сабетта','жировой лёд, припай']]
yy=2.05
for i,(a,b) in enumerate(data):
    rect(s, Inches(8.0), Inches(yy), Inches(4.9), Inches(0.62),
         LGRAY if i%2 else WHITE, line=LGRAY)
    txt(s, Inches(8.1), Inches(yy), Inches(1.7), Inches(0.62), a,
        size=15, color=DARK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(9.8), Inches(yy), Inches(3.0), Inches(0.62), b,
        size=14, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
    yy += 0.62
txt(s, Inches(8.0), Inches(4.4), Inches(5.0), Inches(2.5),
    'Вывод: бинарный порог даёт ложные срабатывания на всех трёх '
    'акваториях. Необходимо явное выделение льда в отдельный класс '
    'и контекстная верификация.', size=15, color=DARK)

# ════════════════════════ SLIDE 7 — ARCHITECTURE ════════════════════════
s = slide(); header(s, 'Архитектура: трёхэтапный конвейер', 7)
pic_fit(s, f'{FIG}/fig_pipeline.png', Inches(0.5), Inches(1.5), Inches(12.3), Inches(4.0))
bullets(s, Inches(0.6), Inches(5.7), Inches(12.2), Inches(1.5), [
    (0,'SNAP: калибровка к σ⁰, фильтр Lee 7×7, Range-Doppler коррекция.'),
    (0,'PyTorch: DeepLabV3+ / ResNet-50 + scSE, 3 класса, TTA.'),
    (0,'Верификация: морфология + ERA5 (ветер 3–9 м/с) + АИС судов.'),
])

# ════════════════════════ SLIDE 8 — DATASET & TRAINING ════════════════════════
s = slide(); header(s, 'Датасет и обучение модели', 8)
pic_fit(s, f'{FIG}/fig_class_dist.png', Inches(0.3), Inches(1.4), Inches(4.5), Inches(4.6))
pic_fit(s, f'{FIG}/fig_training.png', Inches(5.0), Inches(1.5), Inches(8.0), Inches(3.4))
bullets(s, Inches(5.0), Inches(5.0), Inches(8.0), Inches(2.2), [
    (0,'1125 сцен (MKLab + 13 сцен Кольского залива), 4128 тайлов 256×256.'),
    (0,'Дисбаланс компенсирован Dice-BCE с весами (w_нефть = 9,8).'),
    (0,'AdamW, lr 1e-4; лучшее val mIoU = 0,84 (эпоха 78); RTX 3090, ~7,5 ч.'),
])

# ════════════════════════ SLIDE 9 — RESULTS ════════════════════════
s = slide(); header(s, 'Результаты сегментации (Кольский залив)', 9)
pic_fit(s, f'{FIG}/fig_confusion.png', Inches(0.4), Inches(1.4), Inches(6.0), Inches(5.4))
# metrics cards
txt(s, Inches(6.9), Inches(1.5), Inches(6.0), Inches(0.5),
    'Тестовая выборка (414 тайлов):', size=18, color=NAVY, bold=True)
cards=[('Общая точность','95,8 %'),('mIoU (3 класса)','0,82'),
       ('F1 «нефть»','0,89'),('Precision «нефть»','0,911'),
       ('Recall «нефть»','0,875')]
yy=2.15
for i,(a,b) in enumerate(cards):
    rect(s, Inches(6.9), Inches(yy), Inches(5.9), Inches(0.62), LGRAY if i%2 else WHITE, line=LGRAY)
    txt(s, Inches(7.05), Inches(yy), Inches(3.8), Inches(0.62), a, size=15,
        color=DARK, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(10.7), Inches(yy), Inches(2.0), Inches(0.62), b, size=16,
        color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
    yy += 0.62
txt(s, Inches(6.9), Inches(5.5), Inches(6.0), Inches(1.3),
    'Основная ошибка: 8,4 % пикселей «нефть» → «лёд + суша» — '
    'физическая близость откликов нефти и молодого льда.',
    size=14, color=RED, italic=True)

# ════════════════════════ SLIDE 10 — TRANSFER + COMPARISON ════════════════════════
s = slide(); header(s, 'Перенос на порты и сравнение с аналогами', 10)
pic_fit(s, f'{FIG}/fig_ports_f1.png', Inches(0.35), Inches(1.4), Inches(6.4), Inches(4.4))
pic_fit(s, f'{FIG}/fig_methods.png', Inches(6.9), Inches(1.4), Inches(6.2), Inches(4.4))
caption(s, Inches(0.35), Inches(5.9), Inches(6.4),
        'Деградация F1: Кольский 0,89 → Варандей 0,84 → Сабетта 0,76.')
caption(s, Inches(6.9), Inches(5.9), Inches(6.2),
        'DeepLabV3+ scSE превосходит аналоги (F1 = 0,89).')
txt(s, Inches(0.45), Inches(6.45), Inches(12.4), Inches(0.7),
    'Рост ложных срабатываний на Сабетте (FP 1,4 % → 6,2 %) — на участках шуги и '
    'ниласа; подтверждает необходимость дообучения на арктических данных.',
    size=13.5, color=GRAY, italic=True)

# ════════════════════════ SLIDE 11 — CONCLUSIONS ════════════════════════
s = slide(); header(s, 'Выводы', 11)
bullets(s, Inches(0.5), Inches(1.35), Inches(12.4), Inches(5.0), [
    (0,'Подтверждён основной тезис: тёмное пятно в SAR — необходимый, но не'),
    (1,'достаточный признак нефти (Печенга, Варандей, Сабетта — все ложные цели).'),
    (0,'Норильск-2020 показал предел C-SAR для дизеля на реках при ледоходе —'),
    (1,'обоснован фокус на морских акваториях и выделение льда в отдельный класс.'),
    (0,'Обучена модель DeepLabV3+ (ResNet-50 + scSE), трёхклассовая разметка:'),
    (1,'точность 95,8 %, mIoU 0,82, F1 «нефть» = 0,89 (Кольский залив).'),
    (0,'Перенос на порты: F1 0,84 (Варандей) и 0,76 (Сабетта) —'),
    (1,'приоритет дальнейшей работы: расширение арктического датасета.'),
    (0,'Подход превзошёл 4 метода-аналога (0,89 против 0,71–0,86)'),
    (1,'и обеспечил разделение нефти и арктических ложных целей.'),
])
rect(s, Inches(0.5), Inches(6.55), Inches(12.3), Pt(2), RED)
txt(s, Inches(0.5), Inches(6.65), Inches(12.3), Inches(0.5),
    'Спасибо за внимание!', size=20, color=NAVY, bold=True, align=PP_ALIGN.CENTER)

prs.save(OUT)
print('SAVED', OUT, '| slides:', len(prs.slides._sldIdLst))
