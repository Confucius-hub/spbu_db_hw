#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерирует отзыв руководителя о прохождении учебной практики (.docx)."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = '/home/user/spbu_db_hw/thesis/otziv/Отзыв_о_практике_Байханов.docx'
FONT = 'Times New Roman'


def set_font(run, name=FONT, size=14, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(attr), name)


def para(doc, text='', size=14, bold=False, italic=False,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=6, first_indent=1.0):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.15
    if first_indent:
        pf.first_line_indent = Cm(first_indent)
    if text:
        r = p.add_run(text)
        set_font(r, size=size, bold=bold, italic=italic)
    return p


def bullet(doc, text, size=14):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Cm(1.0)
    r = p.add_run(text)
    set_font(r, size=size)
    return p


def set_cell(cell, text, bold=False, italic=False, size=12):
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(text)
    set_font(r, size=size, bold=bold, italic=italic)


# ── Документ ────────────────────────────────────────────────────────────────
doc = Document()
sec = doc.sections[0]
sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
sec.left_margin = Cm(3.0); sec.right_margin = Cm(1.5)

style = doc.styles['Normal']
style.font.name = FONT
style.font.size = Pt(14)
style.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)

# Заголовок
h = doc.add_paragraph(); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
h.paragraph_format.space_after = Pt(2)
r = h.add_run('Отзыв о прохождении'); set_font(r, size=16, bold=False)
h2 = doc.add_paragraph(); h2.alignment = WD_ALIGN_PARAGRAPH.CENTER
h2.paragraph_format.space_after = Pt(12)
r = h2.add_run('учебной практики'); set_font(r, size=16, bold=False)

# Таблица: Студент / Дата
tbl = doc.add_table(rows=2, cols=2)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.style = 'Table Grid'
tbl.columns[0].width = Cm(3.0)
tbl.columns[1].width = Cm(13.0)
set_cell(tbl.rows[0].cells[0], 'Студент', italic=True, size=12)
set_cell(tbl.rows[0].cells[1], 'Байханов Владислав Камолович', bold=True, size=12)
set_cell(tbl.rows[1].cells[0], 'Дата', size=12)
set_cell(tbl.rows[1].cells[1], '12.05.2026', italic=True, size=12)
for row in tbl.rows:
    for c in row.cells:
        c.width = Cm(3.0) if c is row.cells[0] else Cm(13.0)

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# Вводный абзац (тема)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.first_line_indent = Cm(1.0)
p.paragraph_format.line_spacing = 1.15; p.paragraph_format.space_after = Pt(6)
r = p.add_run('В период прохождения учебной практики студент Байханов Владислав '
              'Камолович выполнял работу по теме: '); set_font(r)
r = p.add_run('«Разработка системы автоматического детектирования нефтяных разливов '
              'в акваториях арктических портов по данным спутниковых радиолокационных '
              'систем»'); set_font(r, bold=True)
r = p.add_run('.'); set_font(r)

# Постановка задачи
para(doc,
     'Перед студентом была поставлена задача разработать и описать программно-аналитическое '
     'решение для автоматического обнаружения нефтяных разливов в акваториях арктических '
     'портов по данным радиолокационной спутниковой съёмки Sentinel-1. Особое внимание в '
     'ходе практики уделялось предобработке радиолокационных данных, формированию '
     'трёхклассового аннотированного датасета, адаптации архитектуры глубокого обучения '
     'DeepLabV3+ под одноканальные SAR-данные и верификации результатов по независимым '
     'источникам (метеоданные реанализа ERA5, AIS-трафик судов).')

# Перечень задач
para(doc,
     'В ходе прохождения практики Байханов Владислав Камолович качественно и своевременно '
     'выполнил следующие задачи:', after=4)

bullet(doc, 'Изучил прикладной контекст мониторинга нефтяных разливов в акваториях '
            'арктических портов (Кольский залив, Варандей, Сабетта, Печенга);')
bullet(doc, 'Рассмотрел физические основы радиолокационного зондирования (эффект Марангони) '
            'и проблему ложных целей (look-alikes) — начальных форм льда, зон штиля и '
            'биогенных плёнок;')
bullet(doc, 'Реализовал восьмишаговый конвейер предобработки снимков Sentinel-1 в среде '
            'ESA SNAP: применение точных орбит, удаление теплового шума, калибровка σ⁰, '
            'фильтрация спекла (Lee 7×7), геометрическая коррекция;')
bullet(doc, 'Сформировал трёхклассовый аннотированный датасет «вода / нефть / лёд + суша» '
            '(1125 сцен, 4128 тайлов 256×256), впервые выделив лёд в отдельный класс;')
bullet(doc, 'Адаптировал архитектуру DeepLabV3+ (энкодер ResNet-50, блоки внимания scSE) '
            'под одноканальные радиолокационные данные;')
bullet(doc, 'Обучил нейросетевую модель с комбинированной функцией потерь Dice-BCE и провёл '
            'количественную оценку качества (mIoU = 0,82; F1 = 0,89; точность 95,8 %);')
bullet(doc, 'Выполнил проверку переноса обученной модели на новые арктические акватории '
            '(Варандей, Сабетта, Печенга) и количественно оценил деградацию качества;')
bullet(doc, 'Подготовил иллюстративные материалы, таблицы и аналитическое описание '
            'полученных результатов; обозначил ограничения метода и условия его применимости.')

# Качества студента
para(doc,
     'В процессе выполнения практики студент проявил самостоятельность, аккуратность и '
     'заинтересованность в решении поставленных задач. Он продемонстрировал уверенные навыки '
     'программирования на языке Python, владение методами компьютерного зрения и глубокого '
     'обучения, а также понимание принципов обработки данных дистанционного зондирования '
     'Земли. Работа выполнена последовательно, с соблюдением логики научно-технического '
     'исследования: от постановки задачи и предобработки данных до обучения модели, анализа '
     'результатов и формулирования выводов.', before=4)

# Результат
para(doc,
     'В результате прохождения практики была разработана программно-аналитическая система '
     'детектирования нефтяных разливов, объединяющая конвейер предобработки SAR-данных, '
     'нейросетевую сегментацию и трёхуровневую верификацию результатов. Полученные '
     'результаты показывают, что студент способен применять современные методы машинного '
     'обучения и анализа данных дистанционного зондирования для решения прикладных задач '
     'экологического мониторинга арктических акваторий.')

# Оформление
para(doc,
     'Отчёт по практике оформлен полно, структура работы выдержана, цель и задачи раскрыты. '
     'Представленные материалы подтверждают, что студент успешно справился с поставленной '
     'задачей и приобрёл практические навыки разработки, обучения и верификации '
     'интеллектуальных систем обработки спутниковых данных.')

# Оценка
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.first_line_indent = Cm(1.0)
p.paragraph_format.line_spacing = 1.15; p.paragraph_format.space_before = Pt(4)
r = p.add_run('Считаю, что Байханов Владислав Камолович за прохождение учебной практики '
              'заслуживает оценку '); set_font(r)
r = p.add_run('«зачтено»'); set_font(r, bold=True)
r = p.add_run(' (в системе ECTS — '); set_font(r)
r = p.add_run('«A»'); set_font(r, bold=True)
r = p.add_run(').'); set_font(r)

# Подпись
doc.add_paragraph().paragraph_format.space_after = Pt(10)
sp = doc.add_paragraph(); sp.alignment = WD_ALIGN_PARAGRAPH.LEFT
sp.paragraph_format.line_spacing = 1.15
r = sp.add_run('Руководитель практики          /                          /          '
               'к.т.н. Митько Арсений Валерьевич')
set_font(r, size=12)

doc.save(OUT)
print('Saved →', OUT)
print('Paragraphs:', len(doc.paragraphs))
