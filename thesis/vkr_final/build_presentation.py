# -*- coding: utf-8 -*-
"""Финальная презентация ВКР Байханова В. К. — 10 слайдов, регламент 10 минут.
Тема: автоматическое детектирование нефтяных разливов в арктических портах
по данным Sentinel-1 (трёхклассовая семантическая сегментация DeepLabV3+)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

FIG = "/home/user/spbu_db_hw/thesis/otchet/figures"

# ── палитра ────────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x0B, 0x2E, 0x4F)   # тёмно-синий (Арктика)
BLUE   = RGBColor(0x1F, 0x6F, 0xB2)
ACCENT = RGBColor(0xE0, 0x6C, 0x18)   # оранжевый акцент (нефть)
GREY   = RGBColor(0x3A, 0x3A, 0x3A)
LIGHT  = RGBColor(0xF2, 0xF6, 0xFA)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, color, line=None):
    from pptx.enum.shapes import MSO_SHAPE
    sp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(1)
    sp.shadow.inherit = False
    return sp


def txt(s, x, y, w, h, text, size=18, color=GREY, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font="Calibri", line_spacing=1.0):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = font
    return tb


def bullets(s, x, y, w, h, items, size=18, color=GREY, gap=6, marker="•  "):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.line_spacing = 1.05
        if isinstance(it, tuple):     # (текст, уровень)
            text, lvl = it
        else:
            text, lvl = it, 0
        r = p.add_run()
        r.text = (marker if lvl == 0 else "      – ") + text
        r.font.size = Pt(size if lvl == 0 else size - 2)
        r.font.color.rgb = color; r.font.name = "Calibri"
        r.font.bold = False
    return tb


def header(s, num, title, kicker=None):
    """Шапка контентного слайда: цветная плашка + номер + заголовок."""
    rect(s, 0, 0, SW, Inches(1.15), NAVY)
    rect(s, 0, Inches(1.15), SW, Pt(4), ACCENT)
    txt(s, Inches(0.45), Inches(0.12), Inches(0.9), Inches(0.9),
        f"{num:02d}", size=30, color=ACCENT, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.35), Inches(0.05), Inches(11.4), Inches(1.05),
        title, size=25, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if kicker:
        txt(s, Inches(1.37), Inches(0.78), Inches(11.4), Inches(0.32),
            kicker, size=12, color=RGBColor(0xBE, 0xD6, 0xEC), bold=False)


def footer(s, n):
    txt(s, Inches(0.4), Inches(7.05), Inches(9), Inches(0.35),
        "Байханов В. К.  •  ВКР  •  СПбГУ, 2026", size=10, color=RGBColor(0x9A, 0x9A, 0x9A))
    txt(s, Inches(12.4), Inches(7.05), Inches(0.7), Inches(0.35),
        str(n), size=11, color=RGBColor(0x9A, 0x9A, 0x9A), align=PP_ALIGN.RIGHT)


def pic_fit(s, path, x, y, w, h):
    """Вписать картинку в рамку w×h без искажений, по центру."""
    from PIL import Image
    iw, ih = Image.open(path).size
    ar_box = w / h; ar_img = iw / ih
    if ar_img > ar_box:
        nw = w; nh = int(w / ar_img)
    else:
        nh = h; nw = int(h * ar_img)
    nx = x + (w - nw) // 2; ny = y + (h - nh) // 2
    return s.shapes.add_picture(path, nx, ny, nw, nh)


# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 1 — Титул
# ════════════════════════════════════════════════════════════════════════════
s = slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, Inches(4.55), SW, Pt(3), ACCENT)
txt(s, Inches(0.8), Inches(0.55), Inches(11.7), Inches(0.4),
    "Санкт-Петербургский государственный университет", size=16,
    color=RGBColor(0xBE, 0xD6, 0xEC), align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.35),
    "Магистерская программа «Искусственный интеллект и наука о данных»",
    size=13, color=RGBColor(0x8F, 0xB0, 0xCE), align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(2.0), Inches(11.7), Inches(2.4),
    "Разработка системы автоматического\nдетектирования нефтяных разливов\n"
    "в акваториях арктических портов\nпо данным спутниковой радиолокационной съёмки",
    size=29, color=WHITE, bold=True, align=PP_ALIGN.CENTER, line_spacing=1.12)
txt(s, Inches(0.8), Inches(4.85), Inches(11.7), Inches(0.5),
    "Выпускная квалификационная работа", size=16,
    color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(1.2), Inches(5.7), Inches(5.6), Inches(1.2),
    "Выполнил:\nБайханов Владислав Камолович", size=15, color=WHITE)
txt(s, Inches(7.0), Inches(5.7), Inches(5.4), Inches(1.2),
    "Научный руководитель:\nк.т.н., доцент Митько А. В.", size=15, color=WHITE,
    align=PP_ALIGN.RIGHT)
txt(s, Inches(0.8), Inches(6.95), Inches(11.7), Inches(0.4),
    "Санкт-Петербург · 2026", size=13, color=RGBColor(0x8F, 0xB0, 0xCE),
    align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 2 — Актуальность и проблема
# ════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, 1, "Актуальность и научно-техническая проблема",
       "Зачем нужно детектировать нефть в Арктике автоматически")
bullets(s, Inches(0.55), Inches(1.5), Inches(7.0), Inches(5.2), [
    "В Мировой океан ежегодно попадает > 700 тыс. т углеводородов; доля Арктики растёт из-за Севморпути и шельфа",
    "При t < +5 °C нефть разлагается в 5–10 раз медленнее → долговременное загрязнение",
    "> 80 % времени — облачность и полярная ночь → оптика не работает, нужен радар (SAR)",
    "Sentinel-1 SAR — всепогодный круглосуточный мониторинг",
    "Проблема: природные «двойники» нефти (лёд, биоплёнки, штиль) → до 70 % ложных срабатываний",
], size=17, gap=12)
rect(s, Inches(7.85), Inches(1.55), Inches(5.0), Inches(2.35), LIGHT)
txt(s, Inches(8.05), Inches(1.7), Inches(4.6), Inches(2.1),
    "Крупные инциденты:\n\n"
    "• Норильск, 2020 — ≈21 тыс. т, ущерб 146 млрд ₽\n"
    "• Кольский залив, 11.09.2024 — разлив мазута\n"
    "• Бухта Тикси, 2026 — керосин на льду",
    size=15, color=NAVY, line_spacing=1.1)
pic_fit(s, f"{FIG}/fig_kola.png", Inches(7.85), Inches(4.05), Inches(5.0), Inches(2.7))
footer(s, 2)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 3 — Цель и задачи
# ════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, 2, "Цель, объект и задачи исследования")
rect(s, Inches(0.55), Inches(1.5), Inches(12.25), Inches(1.5), LIGHT)
txt(s, Inches(0.8), Inches(1.62), Inches(11.8), Inches(1.3),
    "Цель — автоматизация процесса детектирования нефтяных разливов в акваториях "
    "арктических портов по данным Sentinel-1 за счёт нейросетевой трёхклассовой "
    "модели семантической сегментации, обеспечивающей F1 ≥ 0,85 для класса «нефть».",
    size=18, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1)
txt(s, Inches(0.55), Inches(3.25), Inches(12), Inches(0.4),
    "Задачи:", size=18, color=ACCENT, bold=True)
bullets(s, Inches(0.7), Inches(3.75), Inches(12.0), Inches(3.2), [
    "Выявить ограничения существующих методов детектирования по SAR-данным в Арктике и обосновать выбор архитектуры",
    "Разработать методику формирования размеченного датасета и обучить нейросетевую модель сегментации",
    "Реализовать программный прототип в виде модульного конвейера обработки спутниковых снимков",
    "Провести экспериментальную оценку качества и сравнительный анализ с альтернативными методами",
], size=17, gap=14)
footer(s, 3)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 4 — Научная новизна (главная идея — 3 класса)
# ════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, 3, "Научная новизна: трёхклассовая сегментация",
       "Ключевое отличие от всех существующих работ")
txt(s, Inches(0.55), Inches(1.45), Inches(5.9), Inches(0.5),
    "Было (бинарная схема):", size=18, color=GREY, bold=True)
rect(s, Inches(0.55), Inches(2.0), Inches(5.9), Inches(1.2), RGBColor(0xE8, 0xE8, 0xE8))
txt(s, Inches(0.75), Inches(2.1), Inches(5.5), Inches(1.0),
    "нефть  /  фон\n\nлёд и биоплёнки путаются с нефтью → ложные тревоги",
    size=16, color=GREY, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(6.9), Inches(1.45), Inches(6.0), Inches(0.5),
    "Стало (наш подход):", size=18, color=ACCENT, bold=True)
rect(s, Inches(6.9), Inches(2.0), Inches(5.95), Inches(1.2), LIGHT)
txt(s, Inches(7.1), Inches(2.1), Inches(5.6), Inches(1.0),
    "вода  /  нефть  /  лёд + суша\n\nлёд вынесен в отдельный класс → меньше ложных срабатываний",
    size=16, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, Inches(0.55), Inches(3.55), Inches(12.2), Inches(3.2), [
    "Впервые для арктической задачи начальные формы льда выделены в самостоятельный класс сегментации",
    "Методика формирования арктического подмножества: полигональная разметка Кольского залива в QGIS с учётом реанализа ERA5 и данных AIS",
    "Архитектура DeepLabV3+ (ResNet-50 + scSE) адаптирована к одноканальным SAR-данным C-диапазона; функция потерь Dice-BCE с весами классов",
], size=17, gap=14)
footer(s, 4)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 5 — Архитектура решения (конвейер)
# ════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, 4, "Архитектура программного решения",
       "Трёхэтапный модульный конвейер обработки SAR")
pic_fit(s, f"{FIG}/fig_pipeline.png", Inches(0.55), Inches(1.45), Inches(7.4), Inches(5.2))
bullets(s, Inches(8.2), Inches(1.7), Inches(4.7), Inches(5.0), [
    "1. Предобработка (ESA SNAP): 6 шагов — орбита, шумы, калибровка σ⁰, фильтр Ли 7×7, геокоррекция, дБ",
    "2. Сегментация: DeepLabV3+ ResNet-50 + scSE → 3 класса",
    "3. Верификация: морфология пятна + контекст",
    "Скорость: 1 сцена за 65 секунд",
    "Реализация: Python, PyTorch 2.1, CUDA 12.1, RTX 3090",
], size=16, gap=14)
footer(s, 5)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 6 — Данные и обучение
# ════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, 5, "Датасет и обучение модели")
bullets(s, Inches(0.55), Inches(1.55), Inches(6.3), Inches(3.0), [
    "1125 размеченных сцен Sentinel-1:",
    ("1112 — открытый набор MKLab Krestenitis (Средиземное море)", 1),
    ("13 — собственный поднабор Кольского залива (QGIS)", 1),
    "4128 тайлов 256×256, перекрытие 50 %",
    "Деление 70 / 20 / 10 на уровне сцен",
    "AdamW, lr 1·10⁻⁴, 100 эпох, batch 8, AMP",
], size=16, gap=8)
rect(s, Inches(0.55), Inches(4.85), Inches(6.3), Inches(1.7), LIGHT)
txt(s, Inches(0.75), Inches(4.98), Inches(5.9), Inches(1.5),
    "Главная сложность — дисбаланс классов:\n«нефть» < 1 % пикселей.\n"
    "Решение: веса классов в Dice-BCE (w_нефть = 9,8)",
    size=15, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1)
pic_fit(s, f"{FIG}/fig_class_dist.png", Inches(7.1), Inches(1.5), Inches(5.8), Inches(2.55))
pic_fit(s, f"{FIG}/fig_training.png", Inches(7.1), Inches(4.1), Inches(5.8), Inches(2.55))
footer(s, 6)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 7 — Результаты на Кольском заливе
# ════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, 6, "Результаты на тестовой выборке (Кольский залив)",
       "412 тайлов, не участвовавших в обучении")
# карточки метрик
cards = [("F1 (нефть)", "0,89"), ("mIoU", "0,82"), ("Accuracy", "95,8 %")]
cx = Inches(0.55)
for i, (k, v) in enumerate(cards):
    x = Emu(int(cx) + i * int(Inches(2.35)))
    rect(s, x, Inches(1.5), Inches(2.1), Inches(1.5), NAVY)
    txt(s, x, Inches(1.6), Inches(2.1), Inches(0.7), v, size=34, color=WHITE,
        bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x, Inches(2.42), Inches(2.1), Inches(0.45), k, size=14,
        color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
bullets(s, Inches(0.55), Inches(3.3), Inches(6.7), Inches(3.4), [
    "Класс «нефть»: Precision 0,91 · Recall 0,87",
    "Основная ошибка: 8,4 % пикселей «нефть» → «лёд + суша» (физически схожие тёмные сигнатуры)",
    "Прирост F1 относительно порогового метода Оцу: +0,18",
    "Превосходство по всем метрикам над 4 альтернативными методами",
], size=16, gap=12)
pic_fit(s, f"{FIG}/fig_confusion.png", Inches(7.4), Inches(1.5), Inches(5.5), Inches(2.7))
pic_fit(s, f"{FIG}/fig_methods.png", Inches(7.4), Inches(4.25), Inches(5.5), Inches(2.45))
footer(s, 7)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 8 — Переносимость и ложные цели
# ════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, 7, "Переносимость методики и анализ ложных целей",
       "Печенга · Варандей · Сабетта")
pic_fit(s, f"{FIG}/fig_ports_f1.png", Inches(0.55), Inches(1.5), Inches(6.0), Inches(5.1))
bullets(s, Inches(6.85), Inches(1.7), Inches(6.0), Inches(5.0), [
    "Закономерная деградация при удалении от региона обучения:",
    ("Кольский залив — F1 = 0,89", 1),
    ("Варандей (Печорское море) — F1 = 0,84", 1),
    ("Сабетта (Обская губа) — F1 = 0,76", 1),
    "Типы ложных целей по акваториям:",
    ("Печенга — ветровые тени, биоплёнки (безлёдный тип)", 1),
    ("Варандей — сезонный первогодний лёд", 1),
    ("Сабетта — жировой/ниласовый лёд, припай", 1),
    "Вывод: методика применима, но требует целевого дообучения под ледовые акватории",
], size=15, gap=8)
footer(s, 8)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 9 — Заключение
# ════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, 8, "Заключение")
txt(s, Inches(0.55), Inches(1.45), Inches(12.2), Inches(0.6),
    "Цель достигнута: критерий F1 ≥ 0,85 для класса «нефть» выполнен (F1 = 0,89). "
    "Решены все четыре задачи.", size=18, color=NAVY, bold=True, line_spacing=1.1)
bullets(s, Inches(0.55), Inches(2.5), Inches(12.2), Inches(3.0), [
    "Систематизированы ограничения существующих методов; обоснован выбор DeepLabV3+ (ResNet-50 + scSE)",
    "Создан комбинированный датасет (1125 сцен, 4128 тайлов) с оригинальной трёхклассовой разметкой",
    "Реализован программный прототип-конвейер (65 с/сцена); код опубликован в открытом доступе",
    "Экспериментально подтверждено превосходство над пороговыми и классическими методами",
], size=17, gap=12)
rect(s, Inches(0.55), Inches(5.55), Inches(12.25), Inches(1.1), LIGHT)
txt(s, Inches(0.8), Inches(5.68), Inches(11.8), Inches(0.9),
    "Практическая значимость: применимо в системах экологического мониторинга "
    "акваторий арктических портов (Росприроднадзор, МЧС, «Морспасслужба», "
    "«Росатом» / Севморпуть).", size=16, color=NAVY, anchor=MSO_ANCHOR.MIDDLE,
    line_spacing=1.1)
footer(s, 9)

# ════════════════════════════════════════════════════════════════════════════
# СЛАЙД 10 — Спасибо
# ════════════════════════════════════════════════════════════════════════════
s = slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, Inches(3.5), SW, Pt(3), ACCENT)
txt(s, Inches(0.8), Inches(2.4), Inches(11.7), Inches(1.0),
    "Спасибо за внимание!", size=40, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(3.8), Inches(11.7), Inches(0.6),
    "Готов ответить на ваши вопросы", size=20,
    color=RGBColor(0xBE, 0xD6, 0xEC), align=PP_ALIGN.CENTER)
txt(s, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.4),
    "Байханов Владислав Камолович\n"
    "Разработка системы автоматического детектирования нефтяных разливов\n"
    "в акваториях арктических портов по данным спутниковой радиолокационной съёмки\n"
    "СПбГУ · 2026", size=14, color=RGBColor(0x8F, 0xB0, 0xCE), align=PP_ALIGN.CENTER,
    line_spacing=1.2)

out = "/home/user/spbu_db_hw/thesis/vkr_final/Презентация_Байханов_2026.pptx"
prs.save(out)
print("saved:", out)
print("slides:", len(prs.slides._sldIdLst))
