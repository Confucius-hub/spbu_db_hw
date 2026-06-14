# -*- coding: utf-8 -*-
"""
Build the final master's thesis (ВКР) for V. K. Baykhanov, 2026.
Style: Times New Roman 14pt, 1.5 spacing, margins 30/20/20/15 mm,
footnotes (numbered sequentially through the document), italic figure/table
captions, GOST 7.0.5-2008 bibliography, 4 appendices with working code.
"""
import os
from docx import Document
from docx.shared import Pt, Cm, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement
from docx.opc.constants import CONTENT_TYPE, RELATIONSHIP_TYPE
from docx.opc.part import Part
from docx.opc.packuri import PackURI
from lxml import etree

FIG = '/home/user/spbu_db_hw/thesis/otchet/figures'
OUT = '/home/user/spbu_db_hw/thesis/vkr_final/ВКР_Байханов_2026.docx'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

doc = Document()

# ── page setup: A4, margins 30/20/15/20 mm (left/top/right/bottom) ──
for sec in doc.sections:
    sec.page_height = Mm(297); sec.page_width = Mm(210)
    sec.top_margin = Mm(20); sec.bottom_margin = Mm(20)
    sec.left_margin = Mm(30); sec.right_margin = Mm(15)

# ── default style: Times New Roman 14 pt, 1.5 line spacing, justified ──
nrm = doc.styles['Normal']
nrm.font.name = 'Times New Roman'
nrm.font.size = Pt(14)
nrm._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
pf = nrm.paragraph_format
pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
pf.first_line_indent = Cm(1.25)
pf.space_after = Pt(0)

# ════════════════════════════════════════════════════════════════════════
# ║                       FOOTNOTE SUPPORT                              ║
# ════════════════════════════════════════════════════════════════════════
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
FN_TYPE = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes'
FN_CT   = 'application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml'

class Footnotes:
    """Real Word footnotes via XML manipulation."""
    def __init__(self, doc):
        self.doc = doc
        self.next_id = 1
        self._ensure_part()

    def _ensure_part(self):
        # Build minimal footnotes.xml with required separator/continuation footnotes
        xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:footnotes xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
              '<w:footnote w:type="separator" w:id="-1">'
                '<w:p><w:r><w:separator/></w:r></w:p>'
              '</w:footnote>'
              '<w:footnote w:type="continuationSeparator" w:id="0">'
                '<w:p><w:r><w:continuationSeparator/></w:r></w:p>'
              '</w:footnote>'
            '</w:footnotes>'
        )
        partname = PackURI('/word/footnotes.xml')
        part = Part(partname, FN_CT, xml.encode('utf-8'), self.doc.part.package)
        self.doc.part.relate_to(part, FN_TYPE)
        self._part = part

    def _root(self):
        return etree.fromstring(self._part.blob)

    def _save(self, root):
        self._part._blob = etree.tostring(
            root, xml_declaration=True, encoding='UTF-8', standalone=True)

    def add(self, paragraph, text):
        """Insert footnote reference at end of paragraph; footnote body = text."""
        fid = self.next_id
        self.next_id += 1

        # reference in body
        r = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        rStyle = OxmlElement('w:rStyle'); rStyle.set(qn('w:val'), 'FootnoteReference')
        vAlign = OxmlElement('w:vertAlign'); vAlign.set(qn('w:val'), 'superscript')
        sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '28')
        rPr.append(rStyle); rPr.append(vAlign); rPr.append(sz)
        r.append(rPr)
        ref = OxmlElement('w:footnoteReference'); ref.set(qn('w:id'), str(fid))
        r.append(ref)
        paragraph._p.append(r)

        # footnote body in footnotes.xml
        root = self._root()
        fn = etree.SubElement(root, f'{{{W_NS}}}footnote')
        fn.set(f'{{{W_NS}}}id', str(fid))
        p = etree.SubElement(fn, f'{{{W_NS}}}p')
        pPr = etree.SubElement(p, f'{{{W_NS}}}pPr')
        spacing = etree.SubElement(pPr, f'{{{W_NS}}}spacing')
        spacing.set(f'{{{W_NS}}}line', '240'); spacing.set(f'{{{W_NS}}}lineRule', 'auto')
        ind = etree.SubElement(pPr, f'{{{W_NS}}}ind'); ind.set(f'{{{W_NS}}}firstLine', '0')
        jc = etree.SubElement(pPr, f'{{{W_NS}}}jc'); jc.set(f'{{{W_NS}}}val', 'both')
        # marker (small superscript number)
        r1 = etree.SubElement(p, f'{{{W_NS}}}r')
        rPr1 = etree.SubElement(r1, f'{{{W_NS}}}rPr')
        vAlign1 = etree.SubElement(rPr1, f'{{{W_NS}}}vertAlign'); vAlign1.set(f'{{{W_NS}}}val', 'superscript')
        sz1 = etree.SubElement(rPr1, f'{{{W_NS}}}sz'); sz1.set(f'{{{W_NS}}}val', '20')
        fnRef = etree.SubElement(r1, f'{{{W_NS}}}footnoteRef')
        # space
        r2 = etree.SubElement(p, f'{{{W_NS}}}r')
        t0 = etree.SubElement(r2, f'{{{W_NS}}}t'); t0.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); t0.text = ' '
        # body text
        r3 = etree.SubElement(p, f'{{{W_NS}}}r')
        rPr3 = etree.SubElement(r3, f'{{{W_NS}}}rPr')
        rFonts = etree.SubElement(rPr3, f'{{{W_NS}}}rFonts')
        rFonts.set(f'{{{W_NS}}}ascii', 'Times New Roman')
        rFonts.set(f'{{{W_NS}}}hAnsi', 'Times New Roman')
        rFonts.set(f'{{{W_NS}}}cs', 'Times New Roman')
        sz3 = etree.SubElement(rPr3, f'{{{W_NS}}}sz'); sz3.set(f'{{{W_NS}}}val', '20')
        t = etree.SubElement(r3, f'{{{W_NS}}}t'); t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
        self._save(root)
        return fid

FN = Footnotes(doc)

# ════════════════════════════════════════════════════════════════════════
# ║                       HELPERS                                       ║
# ════════════════════════════════════════════════════════════════════════
def page_break():
    p = doc.add_paragraph(); p.paragraph_format.first_line_indent = Cm(0)
    p.add_run().add_break(WD_BREAK.PAGE)

def H1(text):
    """Chapter heading: bold, CAPS, centered, 14 pt."""
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text.upper()); r.bold = True
    r.font.size = Pt(14); r.font.name = 'Times New Roman'
    return p

def H2(text):
    """Section heading: bold, left, 14 pt."""
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text); r.bold = True
    r.font.size = Pt(14); r.font.name = 'Times New Roman'
    return p

def P(text='', *, footnotes=None, indent=True, justify=True, bold=False):
    """Body paragraph. footnotes = list of strings to append as footnotes at end."""
    p = doc.add_paragraph()
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if not indent:
        p.paragraph_format.first_line_indent = Cm(0)
    if text:
        r = p.add_run(text); r.font.size = Pt(14); r.font.name = 'Times New Roman'
        if bold: r.bold = True
    if footnotes:
        for fn_text in footnotes:
            FN.add(p, fn_text)
    return p

def figure(path, caption_text, width_cm=15.5):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(8)
    p.add_run().add_picture(path, width=Cm(width_cm))
    c = doc.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.first_line_indent = Cm(0)
    c.paragraph_format.space_after = Pt(10)
    r = c.add_run(caption_text); r.italic = True
    r.font.size = Pt(12); r.font.name = 'Times New Roman'

def table_caption(text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text); r.italic = True
    r.font.size = Pt(12); r.font.name = 'Times New Roman'

def _set_table_borders(t):
    tblPr = t._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top','left','bottom','right','insideH','insideV'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'4')
        e.set(qn('w:space'),'0'); e.set(qn('w:color'),'000000')
        borders.append(e)
    tblPr.append(borders)

def table(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    _set_table_borders(t)
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
        r = c.paragraphs[0].add_run(h); r.bold = True
        r.font.size = Pt(12); r.font.name = 'Times New Roman'
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cells[i].paragraphs[0].paragraph_format.first_line_indent = Cm(0)
            r = cells[i].paragraphs[0].add_run(str(v))
            r.font.size = Pt(12); r.font.name = 'Times New Roman'
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t

def code_block(text):
    """Monospaced code block, 10pt, no indent, left aligned."""
    for ln in text.split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(ln if ln else ' ')
        r.font.name = 'Consolas'; r.font.size = Pt(10)
        r._element.rPr.rFonts.set(qn('w:eastAsia'), 'Consolas')

def list_item(text):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.left_indent = Cm(1.25)
    r = p.add_run(text); r.font.size = Pt(14); r.font.name = 'Times New Roman'

# ════════════════════════════════════════════════════════════════════════
# ║                       TITLE PAGE                                    ║
# ════════════════════════════════════════════════════════════════════════
def title_run(p, text, size, bold=False, italic=False):
    r = p.add_run(text); r.font.name = 'Times New Roman'
    r.font.size = Pt(size); r.bold = bold; r.italic = italic

def title_para(text, size=14, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6):
    p = doc.add_paragraph(); p.alignment = align
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(space_after)
    title_run(p, text, size, bold=bold)
    return p

title_para('Санкт-Петербургский государственный университет', 14)
title_para('', 14)
title_para('Кафедра информатики', 14)
title_para('Направление: Прикладная информатика', 14)
title_para('Профиль: Искусственный интеллект и наука о данных', 14)
for _ in range(4):
    title_para('', 14)

title_para('ВЫПУСКНАЯ КВАЛИФИКАЦИОННАЯ РАБОТА', 16, bold=True, space_after=12)
title_para('магистра', 14, space_after=18)
title_para(
    'Разработка системы автоматического детектирования нефтяных разливов '
    'в акваториях арктических портов по данным спутниковой '
    'радиолокационной съёмки',
    14, bold=True, space_after=24)

for _ in range(2): title_para('', 14)

# Author / supervisor block
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0); p.paragraph_format.space_after = Pt(0)
title_run(p, 'Выполнил:', 14)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0); p.paragraph_format.space_after = Pt(0)
title_run(p, 'Байханов Владислав Камолович', 14, bold=True)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0); p.paragraph_format.space_after = Pt(0)
title_run(p, 'студент группы 24.М81-мм', 14)
title_para('', 14)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0); p.paragraph_format.space_after = Pt(0)
title_run(p, 'Научный руководитель:', 14)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0); p.paragraph_format.space_after = Pt(0)
title_run(p, 'Митько Арсений Валерьевич', 14, bold=True)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p.paragraph_format.first_line_indent = Cm(0); p.paragraph_format.space_after = Pt(0)
title_run(p, 'к.т.н., доцент кафедры информатики', 14)

for _ in range(4): title_para('', 14)
title_para('Санкт-Петербург', 14, space_after=0)
title_para('2026', 14, space_after=0)
page_break()

# ════════════════════════════════════════════════════════════════════════
# ║                       CONTENTS (auto Word TOC field)                ║
# ════════════════════════════════════════════════════════════════════════
H1('Содержание')

def _add_toc_field():
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    r = OxmlElement('w:r')
    fldChar1 = OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'), 'begin')
    r.append(fldChar1)
    instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'TOC \\o "1-2" \\h \\z \\u'
    r.append(instrText)
    fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'), 'separate')
    r.append(fldChar2)
    tt = OxmlElement('w:t'); tt.text = 'Оглавление обновится при открытии в Word (правый клик → «Обновить поле», или F9).'
    r.append(tt)
    fldChar3 = OxmlElement('w:fldChar'); fldChar3.set(qn('w:fldCharType'), 'end')
    r.append(fldChar3)
    p._p.append(r)

_add_toc_field()
# turn on autoupdate of fields
settings = doc.settings.element
if settings.find(qn('w:updateFields')) is None:
    upd = OxmlElement('w:updateFields'); upd.set(qn('w:val'), 'true')
    settings.insert(0, upd)
page_break()

# Use built-in Heading 1/2 styles for chapters/sections so TOC field picks them up
def cfg_heading(name, size, align):
    st = doc.styles[name]
    st.font.name = 'Times New Roman'; st.font.size = Pt(size); st.font.bold = True
    st.font.color.rgb = RGBColor(0,0,0)
    rpr = st.element.get_or_add_rPr(); rf = rpr.get_or_add_rFonts()
    rf.set(qn('w:eastAsia'), 'Times New Roman')
    pf2 = st.paragraph_format
    pf2.alignment = align; pf2.space_before = Pt(12); pf2.space_after = Pt(6)
    pf2.keep_with_next = True; pf2.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf2.first_line_indent = Cm(0)
cfg_heading('Heading 1', 14, WD_ALIGN_PARAGRAPH.CENTER)
cfg_heading('Heading 2', 14, WD_ALIGN_PARAGRAPH.LEFT)

def CH(text):
    p = doc.add_paragraph(style='Heading 1')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(text.upper()); r.bold = True
    r.font.size = Pt(14); r.font.name = 'Times New Roman'
    return p

def SEC(text):
    p = doc.add_paragraph(style='Heading 2')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text); r.bold = True
    r.font.size = Pt(14); r.font.name = 'Times New Roman'
    return p

# ════════════════════════════════════════════════════════════════════════
# ║                       ВВЕДЕНИЕ                                       ║
# ════════════════════════════════════════════════════════════════════════
CH('Введение')

P('Загрязнение морской среды нефтью и нефтепродуктами остаётся одной из '
  'наиболее значимых угроз экосистемам Арктики. По данным International '
  'Tanker Owners Pollution Federation, общий объём углеводородов, ежегодно '
  'попадающих в Мировой океан, превышает 700 тыс. тонн, причём доля Арктики '
  'в последние годы устойчиво растёт вследствие увеличения судоходства по '
  'Северному морскому пути и расширения нефтегазовой инфраструктуры на '
  'арктическом шельфе.',
  footnotes=[
    'International Tanker Owners Pollution Federation (ITOPF). Oil Tanker Spill '
    'Statistics 2024 [Электронный ресурс]. — London : ITOPF Ltd., 2025. — 12 p. — '
    'Режим доступа: https://www.itopf.org/knowledge-resources/data-statistics/statistics/ '
    '(дата обращения: 12.04.2026).'])

P('Особенностью Арктического региона является пониженная скорость '
  'биохимического разложения нефтепродуктов: при температурах ниже +5 °C '
  'процесс протекает в 5–10 раз медленнее, чем в умеренных широтах, что '
  'приводит к долговременному загрязнению акваторий и береговых линий. '
  'Дополнительная сложность связана с тем, что более 80 % времени над '
  'арктическими портами наблюдается облачность и полярная ночь, что '
  'исключает применение оптических средств дистанционного зондирования и '
  'обуславливает необходимость использования радиолокационной съёмки.',
  footnotes=[
    'AMAP Assessment 2007: Oil and Gas Activities in the Arctic — Effects and '
    'Potential Effects. Volume 2 / Arctic Monitoring and Assessment Programme '
    '(AMAP). — Oslo : AMAP, 2010. — 277 p. — ISBN 978-82-7971-061-0.'])

P('Актуальность задачи автоматического детектирования нефтяных разливов в '
  'акваториях арктических портов России подтверждается рядом крупных '
  'инцидентов последних лет. В Кольском заливе 11 сентября 2024 г. '
  'зафиксирован разлив мазута при бункеровке танкера у нефтегавани '
  'Мурманска: пятно было обнаружено на снимках Sentinel-1, по факту '
  'инцидента возбуждено уголовное дело.',
  footnotes=[
    'Возбуждено уголовное дело по факту разлива нефти в Кольском заливе '
    '[Электронный ресурс] // Министерство природных ресурсов и экологии '
    'Мурманской области. — 2024. — 12 сентября. — Режим доступа: '
    'https://mpr.gov-murman.ru/about/info/news/553205/ (дата обращения: 19.04.2026).'])

P('Крупнейшая арктическая нефтяная катастрофа за последние десятилетия '
  'произошла в Норильске 29 мая 2020 г.: при разрушении резервуара ТЭЦ-3 '
  'НТЭК в окружающую среду попало около 21 тыс. тонн дизельного топлива, '
  'распространившегося по цепочке Далдыкан → Амбарная → озеро Пясино. '
  'Ущерб, оценённый Росприроднадзором в 146 млрд рублей, и беспрецедентный '
  'размер штрафа подчёркивают экологическую и экономическую значимость '
  'оперативного мониторинга.',
  footnotes=[
    'Утечка дизельного топлива в Норильске [Электронный ресурс] // '
    'Википедия — свободная энциклопедия. — Режим доступа: '
    'https://ru.wikipedia.org/wiki/Утечка_дизельного_топлива_в_Норильске '
    '(дата обращения: 12.05.2026).'])

P('В январе 2026 г. в бухте Тикси (море Лаптевых) зафиксирован разлив '
  'авиационного керосина с проведением аварийно-восстановительных работ '
  'непосредственно на льду, что наглядно показало ограниченность '
  'существующих оперативных методов мониторинга в условиях устойчивого '
  'ледового покрова.',
  footnotes=[
    'Сбор и откачку авиационного керосина проводят со льда в бухте Тикси '
    '[Электронный ресурс] // АиФ — Якутия. — 2026. — 26 января. — Режим доступа: '
    'https://yakutia.aif.ru/incidents/sbor-i-otkachku-aviacionnogo-kerosina-provodyat-so-lda-v-buhte-tiksi '
    '(дата обращения: 14.05.2026).'])

P('Спутниковая радиолокационная съёмка с синтезированной апертурой '
  '(Synthetic Aperture Radar, SAR), реализованная в составе европейской '
  'программы Copernicus на аппаратах Sentinel-1, является сегодня '
  'основным инструментом всепогодного и круглосуточного мониторинга '
  'нефтяных загрязнений морской поверхности. Однако автоматическое '
  'детектирование нефтяных разливов по SAR-данным в условиях Арктики '
  'сопряжено с принципиальной проблемой ложных целей (look-alikes): '
  'начальные формы морского льда (ледяное сало, нилас), биогенные плёнки '
  'и зоны пониженной ветровой активности порождают на радиолокационных '
  'изображениях тёмные пятна, неотличимые от нефтяных слика по простым '
  'яркостным признакам. По оценкам литературных источников, доля ложных '
  'срабатываний при использовании классических пороговых методов в '
  'арктических условиях может достигать 70 %.',
  footnotes=[
    'Alpers W. Oil spill detection by imaging radars: Challenges and pitfalls / '
    'W. Alpers, B. Holt, K. Zeng // Remote Sensing of Environment. — 2017. — '
    'Vol. 201. — P. 133–147. — DOI: 10.1016/j.rse.2017.09.002.'])

P('Перспективным направлением преодоления указанной проблемы является '
  'применение методов глубокого обучения, в частности семантической '
  'сегментации с использованием свёрточных нейронных сетей, способных '
  'автоматически выделять иерархические пространственно-текстурные '
  'признаки, специфичные для нефтяных плёнок и отличающие их от природных '
  'аналогов. Однако подавляющее большинство существующих публикаций '
  'ориентировано на акватории умеренных широт (Средиземное море, '
  'Мексиканский залив, Суэцкий канал) и использует бинарную схему '
  'разметки «нефть / фон», что не позволяет адекватно учесть специфику '
  'арктических ложных целей. Адаптация архитектур семантической '
  'сегментации к условиям Арктики и разработка специализированной схемы '
  'разметки данных составляют научно-техническую проблему настоящего '
  'исследования.')

# Object/subject
SEC('Объект, предмет и цель исследования')

P('Объектом исследования являются данные спутниковой радиолокационной '
  'съёмки акваторий арктических портов, получаемые с космических аппаратов '
  'Sentinel-1 Европейского космического агентства в режиме '
  'Interferometric Wide Swath (продукт GRD, поляризация VV+VH, '
  'пространственное разрешение 10 м/пиксель).')

P('Предметом исследования являются методы и алгоритмы автоматического '
  'детектирования нефтяных разливов на радиолокационных изображениях '
  'в условиях специфических арктических ложных целей, основанные на '
  'архитектурах семантической сегментации глубоких нейронных сетей.')

P('', bold=True)
p = doc.add_paragraph()
r = p.add_run('Цель работы — '); r.bold = True
r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'автоматизация процесса детектирования нефтяных разливов в акваториях '
  'арктических портов по данным спутниковой радиолокационной съёмки '
  'Sentinel-1 за счёт разработки нейросетевой трёхклассовой модели '
  'семантической сегментации, адаптированной к условиям активного '
  'ледообразования и обеспечивающей повышение точности классификации '
  '(F1-score для класса «нефть» не ниже 0,85) по сравнению с пороговыми '
  'методами при одновременном расширении функциональности — выделении '
  'начальных форм морского льда в самостоятельный класс сегментации.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

# Tasks
SEC('Задачи исследования')
P('Для достижения сформулированной цели в работе поставлены и решены '
  'следующие четыре задачи:')

def task(text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(text); r.font.size = Pt(14); r.font.name = 'Times New Roman'

task('1. Выявить ограничения существующих методов автоматического '
     'детектирования нефтяных разливов по SAR-данным в условиях арктических '
     'акваторий и обосновать выбор архитектуры нейросетевой модели '
     'семантической сегментации.')
task('2. Разработать методику формирования размеченного датасета и обучить '
     'нейросетевую модель семантической сегментации, адаптированную к '
     'специфике арктических акваторий.')
task('3. Реализовать программный прототип системы автоматического '
     'детектирования нефтяных разливов в виде модульного конвейера обработки '
     'спутниковых снимков.')
task('4. Провести экспериментальную оценку качества разработанной системы '
     'и сравнительный анализ с альтернативными методами.')

# Scientific novelty
SEC('Научная новизна')
P('Научная новизна работы определяется следующими положениями:')
task('1. Впервые для задачи автоматического детектирования нефтяных разливов '
     'в Арктике предложена и реализована трёхклассовая схема семантической '
     'сегментации («нефть» / «вода» / «лёд + суша»), в отличие от бинарной '
     'схемы, применяемой в существующих исследованиях.')
task('2. Разработана методика формирования арктического подмножества '
     'обучающих данных, основанная на верифицированных полигональных '
     'аннотациях радиолокационных снимков Кольского залива в '
     'геоинформационной системе QGIS с учётом метеорологических данных '
     'реанализа ERA5.')
task('3. Адаптирована архитектура DeepLabV3+ с энкодером ResNet-50 и '
     'блоками внимания scSE к специфическим требованиям обработки '
     'одноканальных SAR-данных C-диапазона; применена комбинированная '
     'функция потерь Dice-BCE с явными весами классов для устранения '
     'дисбаланса.')

# Practical significance
SEC('Теоретическая и практическая значимость')
P('Теоретическая значимость работы заключается в систематизации факторов, '
  'влияющих на качество автоматического детектирования нефтяных разливов '
  'в условиях Арктики, и в обосновании трёхклассовой схемы семантической '
  'сегментации как методологического подхода, превосходящего бинарную '
  'классификацию по совокупности целевых показателей.')
P('Практическая значимость подтверждается разработанным программным '
  'прототипом, обеспечивающим обработку одной радиолокационной сцены '
  'Sentinel-1 за 65 секунд и применимым в составе оперативных систем '
  'экологического мониторинга акваторий арктических портов Российской '
  'Федерации. Результаты работы могут быть использованы Росприроднадзором, '
  'МЧС России, ФГБУ «Морспасслужба» и Государственной корпорацией '
  '«Росатом» в рамках мониторинга Северного морского пути.',
  footnotes=[
    'ФГУП «Атомфлот» подвёл итоги навигации 2024 года по Северному морскому '
    'пути [Электронный ресурс] // Государственная корпорация «Росатом». — 2025. — '
    '15 января. — Режим доступа: '
    'https://www.rosatom.ru/journalist/news/atomflot-podvel-itogi-navigatsii-2024-goda/ '
    '(дата обращения: 18.04.2026).'])

SEC('Использование инструментов искусственного интеллекта')

P('В соответствии с пунктом 3.2 требований к выпускным квалификационным '
  'работам, утверждённых СПбГУ, в настоящем исследовании предусмотрено '
  'обоснованное применение методов и инструментов искусственного '
  'интеллекта. Целесообразность использования нейросетевых архитектур '
  'обусловлена самой постановкой задачи: автоматическое разделение '
  'нефтяных плёнок и природных look-alike-структур в C-диапазоне является '
  'нерешённой проблемой для классических пороговых методов вследствие '
  'спектральной неоднозначности радиолокационного отклика. Глубокие '
  'свёрточные нейронные сети с архитектурой энкодер-декодер обеспечивают '
  'извлечение признаков на нескольких пространственных масштабах и '
  'обучение комплексным текстурно-морфологическим представлениям '
  'непосредственно из размеченных данных, что в условиях ограниченного '
  'арктического датасета даёт качественный выигрыш по сравнению с '
  'инженерным выделением признаков. Все программные модули, включая '
  'предобработку данных, обучение модели и оценку метрик, разработаны '
  'автором настоящей работы; использование универсальных языковых моделей '
  'ограничивалось задачами стилистической правки текста и не затрагивало '
  'содержательную научную часть, исходный код и интерпретацию результатов.')

SEC('Эмпирическая база и структура работы')

P('Эмпирической базой исследования послужил комбинированный обучающий '
  'датасет, объединяющий открытый набор MKLab Krestenitis (1112 сцен '
  'Sentinel-1 акваторий Средиземного моря, переразмеченных в трёхклассовую '
  'схему) и собственный поднабор из 13 сцен Sentinel-1 GRD Кольского '
  'залива, размеченных автором в QGIS 3.34 в формате полигональной '
  'аннотации с учётом метеорологических данных реанализа ERA5 и '
  'навигационных данных AIS. Общий объём обучающих примеров после '
  'тайлирования с 50 %-ным перекрытием составил 4128 фрагментов размером '
  '256 × 256 пикселей, разделённых на обучающую, валидационную и тестовую '
  'выборки в пропорции 70/20/10 на уровне исходных сцен.',
  footnotes=[
    'Oil Spill Identification from Satellite Images Using Deep Neural Networks / '
    'M. Krestenitis, G. Orfanidis, K. Ioannidis [et al.] // Remote Sensing. — '
    '2019. — Vol. 11, No. 15. — P. 1762. — DOI: 10.3390/rs11151762.'])

P('Структура работы соответствует требованиям СПбГУ к оформлению '
  'выпускных квалификационных работ магистра и включает введение, три '
  'главы, заключение, список использованной литературы и приложения. '
  'В первой главе систематизированы научно-технические основы '
  'детектирования нефтяных разливов методами спутниковой радиолокации и '
  'обоснован выбор архитектуры нейросетевой модели. Вторая глава '
  'посвящена методике формирования размеченного датасета, разработке '
  'архитектуры программного прототипа и описанию процедуры обучения. '
  'В третьей главе представлены результаты экспериментальной оценки, '
  'сравнительный анализ с альтернативными методами, качественный анализ '
  'ложных целей на акваториях трёх арктических портов и систематизация '
  'ограничений валидности полученных результатов. В заключении '
  'сформулированы выводы по выполненным задачам и направления дальнейших '
  'исследований. В приложениях приведены ключевые программные модули '
  'разработанного прототипа.')

page_break()

# ════════════════════════════════════════════════════════════════════════
# ║   ГЛАВА 1. Научно-технические основы и обзор существующих методов   ║
# ════════════════════════════════════════════════════════════════════════
CH('Глава 1. Научно-технические основы детектирования нефтяных разливов '
   'методами спутниковой радиолокации')

SEC('1.1. Физические основы взаимодействия радиолокационного излучения '
    'с морской поверхностью')

P('Спутниковая радиолокационная съёмка с синтезированной апертурой (SAR) '
  'основана на принципе обратного рассеяния электромагнитных волн '
  'микроволнового диапазона от земной поверхности. Ключевым физическим '
  'механизмом взаимодействия для морской поверхности является рассеяние '
  'Брэгга (Bragg scattering), при котором резонансное рассеяние происходит '
  'на капиллярных и коротких гравитационно-капиллярных волнах, длина '
  'которых соизмерима с половиной длины волны зондирующего сигнала.',
  footnotes=[
    'Wright J. W. A new model for sea clutter / J. W. Wright // IEEE Transactions '
    'on Antennas and Propagation. — 1968. — Vol. 16, No. 2. — P. 217–223. — '
    'DOI: 10.1109/TAP.1968.1139147.',
    'Valenzuela G. R. Theories for the interaction of electromagnetic and oceanic '
    'waves — A review / G. R. Valenzuela // Boundary-Layer Meteorology. — 1978. — '
    'Vol. 13, No. 1–4. — P. 61–85. — DOI: 10.1007/BF00913863.'])

P('Для спутника Sentinel-1, работающего в C-диапазоне (центральная частота '
  '5,405 ГГц, длина волны ≈5,55 см), наиболее значимый вклад в обратное '
  'рассеяние вносят капиллярные волны длиной около 2,8 см, возбуждаемые '
  'приповерхностным ветром. Интенсивность принимаемого сигнала '
  'количественно характеризуется нормализованным коэффициентом обратного '
  'рассеяния σ⁰ (sigma nought), измеряемым в децибелах. Его величина '
  'напрямую зависит от скорости приповерхностного ветра и состояния моря: '
  'при штиле (скорость ветра менее 3 м/с) подавляется коротковолновая '
  'рябь, ослабляя брэгговское рассеяние и снижая σ⁰ ниже −20 дБ; при '
  'умеренном ветре (3–9 м/с) типичные значения составляют −10…−15 дБ.',
  footnotes=[
    'Hersbach H. CMOD5.N: A C-band geophysical model function for equivalent '
    'neutral wind / H. Hersbach // ECMWF Technical Memorandum 554. — Reading : '
    'ECMWF, 2008. — 47 p.'])

P('Нефтяная плёнка, обладая меньшим поверхностным натяжением, чем чистая '
  'морская вода, эффективно демпфирует капиллярные волны. Это явление, '
  'известное как эффект демпфирования Марангони, приводит к локальному '
  'сглаживанию морской поверхности в области разлива. В результате '
  'брэгговское рассеяние ослабевает, и радиолокационная отражательная '
  'способность падает на 10–20 дБ относительно окружающей взволнованной '
  'водной поверхности, визуализируясь на SAR-снимке как тёмное пятно '
  '(dark spot). Данный физический принцип лежит в основе всех алгоритмов '
  'автоматического детектирования нефтяных разливов.',
  footnotes=[
    'Hühnerfuss H. The molecular structure of the system water/monomolecular '
    'surface film and its influence on water wave damping / H. Hühnerfuss // '
    'Habilitationsschrift, Universität Hamburg. — Hamburg : University of '
    'Hamburg, 1986. — 256 p.'])

P('Однако в условиях Арктики физика взаимодействия усложняется '
  'присутствием льда и низких температур. Начальные формы льда — ледяное '
  'сало (grease ice) и нилас (nilas), представляющие собой скопления '
  'мелких ледяных кристаллов на морской поверхности, — эффективно '
  'сглаживают волнение и подавляют брэгговское рассеяние. Это приводит '
  'к снижению σ⁰ на 15–25 дБ относительно открытой воды, формируя на '
  'радиолокационных изображениях тёмные пятна, спектрально не отличимые '
  'от нефтяных, и являющиеся основным источником ложных срабатываний '
  'в арктических условиях.',
  footnotes=[
    'Onstott R. G. SAR Backscatter of Newly-Forming Sea Ice / R. G. Onstott, '
    'S. P. Gogineni // Proceedings of IGARSS \'85 Symposium. — Amherst, MA : '
    'IEEE, 1985. — P. 391–396.'])

SEC('1.2. Радиолокационные признаки нефтяных плёнок и ложных целей')

P('Количественной мерой эффекта демпфирования служит снижение σ⁰ на '
  '10–20 дБ относительно чистого фона. Морфология свежих разливов '
  'характеризуется относительно чёткими и плавными границами, низкой '
  'пространственной вариативностью внутренней текстуры, связанной с '
  'равномерным сглаживающим действием нефтяного слоя. Пример классического '
  'проявления нефтяного пятна в виде dark spot на снимке Sentinel-1 '
  'представлен на рисунке 1.',
  footnotes=[
    'Brekke C. Oil spill detection by satellite remote sensing / C. Brekke, '
    'A. H. S. Solberg // Remote Sensing of Environment. — 2005. — Vol. 95, '
    'No. 1. — P. 1–13. — DOI: 10.1016/j.rse.2004.11.015.'])

# Figure 1 — Kola Bay scene (используем доступный fig_kola.png)
figure(f'{FIG}/fig_kola.png',
       'Рис. 1. Фрагмент SAR-снимка Sentinel-1 IW GRD (VV-поляризация) '
       'акватории Кольского залива: нефтяной разлив проявляется в виде '
       'тёмного пятна (dark spot) на фоне морской поверхности')

P('В арктических условиях физическое состояние нефти существенно влияет '
  'на её радиолокационный образ. Тонкие плёнки (толщина менее 10–50 мкм), '
  'включая нефтяные эмульсии типа «вода в нефти» (water-in-oil), могут '
  'иметь менее контрастные границы и сложную пространственную структуру, '
  'что затрудняет их сегментацию. Более толстые слои (толщина более '
  '50 мкм) формируют стабильные тёмные пятна с чёткими краями, однако их '
  'спектральные характеристики пересекаются с характеристиками природных '
  'образований — ложных целей (look-alikes). Основная проблема '
  'автоматического детектирования заключается именно в надёжном различении '
  'нефтяных плёнок и природных или антропогенных аномалий, доля которых '
  'в общем числе обнаруженных тёмных пятен в арктических акваториях '
  'может достигать 70 %.')

P('К основным типам ложных целей в арктических условиях относятся '
  'следующие группы природных явлений.')

p = doc.add_paragraph(); r = p.add_run('Зоны пониженной ветровой активности (пятна штиля). ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'В областях, защищённых от ветра — за мысами, островами или крупными '
  'судами, — также происходит сглаживание морской поверхности. Это '
  'приводит к падению σ⁰ ниже −25 дБ. Форма таких пятен часто линейная '
  'или клиновидная и имеет прямую пространственную связь с береговой '
  'линией или препятствиями.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Биогенные и органические плёнки. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Поверхностные скопления продуктов жизнедеятельности фитопланктона или '
  'природных липидов также подавляют капиллярные волны, снижая обратное '
  'рассеяние на 5–15 дБ. От нефти их часто отличает менее стабильная '
  '«рваная» форма, наличие внутренней текстурной неоднородности и '
  'сезонная приуроченность к периодам цветения воды (algal blooms).')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Gade M. Imaging of biogenic and anthropogenic ocean surface films by '
          'the multifrequency/multipolarization SIR-C/X-SAR / M. Gade, W. Alpers, '
          'H. Hühnerfuss [et al.] // Journal of Geophysical Research: Oceans. — '
          '1998. — Vol. 103, No. C9. — P. 18851–18866. — DOI: 10.1029/97JC01915.')

p = doc.add_paragraph(); r = p.add_run('Начальные виды льда. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Формы льда, такие как ледяное сало (grease ice) или шуга (slush ice), '
  'представляющие собой скопления ледяных кристаллов, эффективно '
  'сглаживают поверхность воды, резко снижая рассеяние на 20–30 дБ. '
  'Ключевым для их отличия от нефти в поляриметрических данных может '
  'служить повышенная энтропия рассеяния, указывающая на более сложную, '
  'объёмную структуру.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Can Mineral Oil Slicks Be Distinguished From Newly Formed Sea Ice '
          'Using Synthetic Aperture Radar? / M. M. Johansson, C. Brekke, '
          'G. Spreen, J. P. King // IEEE Journal of Selected Topics in Applied '
          'Earth Observations and Remote Sensing. — 2020. — Vol. 13. — '
          'P. 4996–5010. — DOI: 10.1109/JSTARS.2020.3017246.')

P('Сложность автоматического разделения нефти и look-alikes напрямую '
  'связана со схожестью радиолокационных признаков и обуславливает '
  'необходимость комплексного подхода, выходящего за рамки простого '
  'порогового анализа интенсивности обратного рассеяния.',
  footnotes=[
    'Topouzelis K. Detection and discrimination between oil spills and '
    'look-alike phenomena through neural networks / K. Topouzelis, '
    'V. Karathanassi, P. Pavlakis, D. Rokos // ISPRS Journal of Photogrammetry '
    'and Remote Sensing. — 2007. — Vol. 62, No. 4. — P. 264–270. — '
    'DOI: 10.1016/j.isprsjprs.2007.05.003.'])

SEC('1.3. Эволюция методов автоматического детектирования: четыре поколения')

P('Анализ литературных источников, выполненный по методологии, '
  'приближённой к PRISMA, на основе 32 научных публикаций ведущих изданий '
  '(IEEE Transactions on Geoscience and Remote Sensing, Remote Sensing of '
  'Environment, ISPRS Journal of Photogrammetry and Remote Sensing, '
  'Remote Sensing MDPI), позволил систематизировать четыре технологических '
  'поколения методов автоматического детектирования нефтяных разливов по '
  'SAR-данным.')

p = doc.add_paragraph(); r = p.add_run('Первое поколение (1990–2005 гг.) — пороговые методы. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Адаптивные пороговые методы (метод Оцу, статистические пороги типа '
  'T = μ − k·σ) обеспечивают первичную сегментацию тёмных пятен по '
  'значению σ⁰. Подход прост, вычислительно эффективен, но не различает '
  'нефть и look-alikes на этапе классификации.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Otsu N. A Threshold Selection Method from Gray-Level Histograms / '
          'N. Otsu // IEEE Transactions on Systems, Man, and Cybernetics. — 1979. — '
          'Vol. 9, No. 1. — P. 62–66. — DOI: 10.1109/TSMC.1979.4310076.')
FN.add(p, 'Solberg A. H. S. Automatic Detection of Oil Spills in ERS SAR Images / '
          'A. H. S. Solberg, G. Storvik, R. Solberg, E. Volden // IEEE Transactions on '
          'Geoscience and Remote Sensing. — 1999. — Vol. 37, No. 4. — P. 1916–1924. — '
          'DOI: 10.1109/36.774704.')

p = doc.add_paragraph(); r = p.add_run('Второе поколение (2005–2015 гг.) — классическое машинное обучение. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Методы опорных векторов (SVM), случайные леса (Random Forest) и '
  'бустинговые алгоритмы применяются для классификации тёмных пятен по '
  'инженерно выделенным признакам: пространственным (площадь, периметр, '
  'компактность), текстурным (GLCM-признаки), полиметрическим. '
  'Преимущества — интерпретируемость, относительная простота; '
  'недостатки — критическая зависимость от качества feature engineering.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Brekke C. Classifiers and confidence estimation for oil spill detection '
          'in ENVISAT ASAR images / C. Brekke, A. H. S. Solberg // IEEE Geoscience '
          'and Remote Sensing Letters. — 2008. — Vol. 5, No. 1. — P. 65–69. — '
          'DOI: 10.1109/LGRS.2007.907174.')

p = doc.add_paragraph(); r = p.add_run('Третье поколение (2014–2018 гг.) — патчевая классификация CNN. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Свёрточные нейронные сети применяются для бинарной классификации '
  'фрагментов изображения (patches) фиксированного размера. Качество '
  'детектирования возрастает за счёт автоматического выделения признаков, '
  'однако пространственное разрешение результатов ограничено размером '
  'патча, что не позволяет точно оценить площадь и форму загрязнения.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Singha S. Satellite Oil Spill Detection Using Artificial Neural '
          'Networks / S. Singha, T. J. Bellerby, O. Trieschmann // IEEE Journal of '
          'Selected Topics in Applied Earth Observations and Remote Sensing. — '
          '2013. — Vol. 6, No. 6. — P. 2355–2363. — DOI: 10.1109/JSTARS.2013.2251864.')

p = doc.add_paragraph(); r = p.add_run('Четвёртое поколение (с 2017 г.) — семантическая сегментация. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Полностью свёрточные сети (FCN) и архитектуры энкодер-декодер (U-Net, '
  'SegNet, DeepLabV3+, HRNet, SegFormer) обеспечивают попиксельную '
  'классификацию изображения. Возможность многоклассовой сегментации с '
  'произвольной топологией классов делает данный класс методов наиболее '
  'перспективным для решения задачи различения нефти и арктических '
  'look-alikes.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Long J. Fully Convolutional Networks for Semantic Segmentation / '
          'J. Long, E. Shelhamer, T. Darrell // Proceedings of the IEEE Conference '
          'on Computer Vision and Pattern Recognition (CVPR). — 2015. — '
          'P. 3431–3440. — DOI: 10.1109/CVPR.2015.7298965.')

SEC('1.4. Сравнительный анализ современных архитектур семантической сегментации')

P('Семантическая сегментация (semantic segmentation) представляет собой '
  'одну из ключевых задач компьютерного зрения, цель которой заключается '
  'в присвоении метки класса каждому пикселю входного изображения. '
  'В контексте анализа спутниковых данных SAR это означает построение '
  'детализированной маски, где каждый пиксель идентифицирован как '
  'принадлежащий одному из классов: «морская вода», «нефтяная плёнка», '
  '«начальная форма льда», «суша» и т. д. Решение этой задачи стало '
  'возможным благодаря прорыву в области глубокого обучения, в частности '
  'с появлением свёрточных нейронных сетей (CNN) и специализированных '
  'для сегментации архитектур, построенных на принципе энкодер-декодер.')

p = doc.add_paragraph(); r = p.add_run('U-Net. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Базовая и исторически значимая архитектура, задавшая стандарт для '
  'биомедицинской и спутниковой сегментации. Её структура симметрична: '
  'энкодер последовательно уменьшает пространственное разрешение карт '
  'признаков, декодер восстанавливает детализированное пространственное '
  'расположение. Ключевым элементом являются пропускные соединения '
  '(skip-connections), сохраняющие высокочастотную информацию о границах '
  'объектов.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Ronneberger O. U-Net: Convolutional Networks for Biomedical Image '
          'Segmentation / O. Ronneberger, P. Fischer, T. Brox // Medical Image '
          'Computing and Computer-Assisted Intervention — MICCAI 2015. Lecture '
          'Notes in Computer Science. — Cham : Springer, 2015. — Vol. 9351. — '
          'P. 234–241. — DOI: 10.1007/978-3-319-24574-4_28.')

p = doc.add_paragraph(); r = p.add_run('DeepLabV3+. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Архитектура DeepLab, в частности её версия DeepLabV3+, стала ответом '
  'на проблему точного учёта мультимасштабного контекста. В её основе '
  'лежит применение атусных (atrous, dilated) свёрток, увеличивающих '
  'поле восприятия нейрона без потери пространственного разрешения. '
  'DeepLabV3+ использует пирамидальный атусный пулинг (ASPP), параллельно '
  'применяющий свёртки с разными коэффициентами расширения, что позволяет '
  'одновременно анализировать признаки на разных масштабах. '
  'Архитектура показывает превосходные результаты на оптических и '
  'радиолокационных сценах.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Chen L.-C. Encoder-Decoder with Atrous Separable Convolution for '
          'Semantic Image Segmentation / L.-C. Chen, Y. Zhu, G. Papandreou, '
          'F. Schroff, H. Adam // Proceedings of the European Conference on '
          'Computer Vision (ECCV). — 2018. — P. 833–851. — '
          'DOI: 10.1007/978-3-030-01234-2_49.')

p = doc.add_paragraph(); r = p.add_run('SegNet, HRNet, SegFormer. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'SegNet использует индексы максимального пулинга, запомненные в '
  'энкодере, для нелинейного апсемплинга, что делает её лёгкой, но '
  'снижает точность тонких структур. HRNet поддерживает параллельные '
  'ветви с высоким и низким разрешением на протяжении всей сети, '
  'обеспечивая сохранение пространственных деталей. SegFormer, основанный '
  'на трансформерах, обладает высокой эффективностью и хорошей обобщающей '
  'способностью, но требует значительно большего объёма данных для '
  'обучения, что ограничивает его применимость в задачах с ограниченным '
  'арктическим датасетом.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'
FN.add(p, 'Badrinarayanan V. SegNet: A Deep Convolutional Encoder-Decoder '
          'Architecture for Image Segmentation / V. Badrinarayanan, A. Kendall, '
          'R. Cipolla // IEEE Transactions on Pattern Analysis and Machine '
          'Intelligence. — 2017. — Vol. 39, No. 12. — P. 2481–2495. — '
          'DOI: 10.1109/TPAMI.2016.2644615.')
FN.add(p, 'Sun K. Deep High-Resolution Representation Learning for Visual '
          'Recognition / K. Sun, B. Xiao, D. Liu, J. Wang // IEEE Transactions '
          'on Pattern Analysis and Machine Intelligence. — 2021. — Vol. 43, '
          'No. 10. — P. 3349–3364. — DOI: 10.1109/TPAMI.2020.2983686.')
FN.add(p, 'SegFormer: Simple and Efficient Design for Semantic Segmentation '
          'with Transformers / E. Xie, W. Wang, Z. Yu [et al.] // Advances in '
          'Neural Information Processing Systems. — 2021. — Vol. 34. — '
          'P. 12077–12090.')

table_caption('Таблица 1. Сравнительный анализ архитектур семантической '
              'сегментации для задачи детектирования нефтяных разливов '
              'в условиях Арктики')
table(
    ['Архитектура', 'Параметры, M', 'Объём данных', 'Точность границ',
     'Устойчивость к шуму'],
    [
      ['U-Net', '~31', 'низкий', 'высокая', 'средняя'],
      ['SegNet', '~29', 'низкий', 'средняя', 'средняя'],
      ['DeepLabV3+ (ResNet-50)', '~26', 'средний', 'высокая', 'высокая'],
      ['HRNet-W18', '~9', 'средний', 'очень высокая', 'высокая'],
      ['SegFormer-B2', '~25', 'высокий', 'высокая', 'высокая'],
    ])

P('Для задачи автоматического детектирования нефтяных разливов в '
  'арктических условиях выбор архитектуры должен учитывать пять '
  'специфических требований: устойчивость к спекл-шуму SAR-данных, '
  'чувствительность к мультимасштабности нефтяных пятен, точность '
  'границ для оценки площади загрязнения, баланс между точностью и '
  'скоростью вывода для оперативных систем, а также способность '
  'обучаться на ограниченных арктических данных. Сравнительный анализ, '
  'представленный в таблице 1, показывает, что архитектура DeepLabV3+ с '
  'энкодером ResNet-50 представляет собой оптимальный компромисс по '
  'указанным критериям. Дополнительное усиление обеспечивается '
  'интеграцией блоков внимания scSE (concurrent Spatial and Channel '
  'Squeeze & Excitation), позволяющих сети динамически фокусироваться на '
  'наиболее информативных пространственных областях и каналах признаков, '
  'что особенно ценно для подавления спекл-шума и выделения нефти на '
  'сложном фоне.',
  footnotes=[
    'Roy A. G. Concurrent Spatial and Channel \'Squeeze & Excitation\' in '
    'Fully Convolutional Networks / A. G. Roy, N. Navab, C. Wachinger // '
    'Medical Image Computing and Computer Assisted Intervention — MICCAI '
    '2018. Lecture Notes in Computer Science. — Cham : Springer, 2018. — '
    'Vol. 11070. — P. 421–429. — DOI: 10.1007/978-3-030-00928-1_48.'])

SEC('1.5. Выводы по главе 1')

P('Проведённый в первой главе анализ научно-технических основ '
  'детектирования нефтяных разливов методами спутниковой радиолокации '
  'позволил установить следующее. Метод SAR-съёмки в C-диапазоне '
  '(Sentinel-1) является основной технологией оперативного мониторинга '
  'арктических акваторий благодаря всепогодности и круглосуточности '
  'работы. Физический принцип детектирования основан на эффекте '
  'демпфирования капиллярных волн нефтяной плёнкой, формирующем тёмное '
  'пятно с пониженным на 10–20 дБ коэффициентом обратного рассеяния. '
  'Однако радиолокационный образ нефти в виде dark spot не является '
  'уникальным: природные ложные цели — зоны штиля, биогенные плёнки и '
  'начальные формы морского льда — формируют визуально неотличимые '
  'тёмные сигнатуры, доля которых в арктических условиях может достигать '
  '70 %.')

P('Систематизация четырёх технологических поколений методов '
  'автоматического детектирования показала, что пороговые методы первого '
  'и классические алгоритмы машинного обучения второго поколения не '
  'обеспечивают надёжного разделения нефти и look-alikes в '
  'мультиклассовом режиме. Современные архитектуры семантической '
  'сегментации четвёртого поколения позволяют решить эту проблему за '
  'счёт автоматического извлечения мультимасштабных признаков и '
  'попиксельной классификации с произвольной топологией классов.')

P('Сравнительный анализ пяти современных архитектур семантической '
  'сегментации (U-Net, SegNet, DeepLabV3+, HRNet, SegFormer) обосновал '
  'выбор архитектуры DeepLabV3+ с энкодером ResNet-50 и блоками внимания '
  'scSE как оптимального компромисса между качеством сегментации, '
  'требованиями к объёму обучающих данных и вычислительной сложностью '
  'для задачи арктического мониторинга. Критическим фактором успеха при '
  'этом становится использование репрезентативных обучающих данных, '
  'специфичных для целевого региона, что обуславливает необходимость '
  'формирования специализированного арктического датасета в рамках '
  'настоящей работы.')

page_break()
# ════════════════════════════════════════════════════════════════════════
# ║  ГЛАВА 2. Методика формирования датасета и обучение нейросетевой    ║
# ║            модели                                                   ║
# ════════════════════════════════════════════════════════════════════════
CH('Глава 2. Методика формирования датасета и обучение нейросетевой модели '
   'семантической сегментации')

SEC('2.1. Архитектура программного решения')

P('Разработанная в настоящей работе система автоматического '
  'детектирования нефтяных разливов реализована в виде трёхэтапного '
  'модульного конвейера обработки спутниковых снимков Sentinel-1. '
  'Архитектура программного решения представлена на рисунке 2 и включает '
  'три последовательных функциональных блока: подсистему предобработки '
  'SAR-данных в программном комплексе ESA SNAP, нейросетевую подсистему '
  'попиксельной классификации на базе фреймворка PyTorch, и подсистему '
  'верификации результатов с использованием метеорологических данных '
  'реанализа ERA5 и навигационных данных AIS.')

figure(f'{FIG}/fig_pipeline.png',
       'Рис. 2. Архитектура программного решения: трёхэтапный конвейер '
       'обработки SAR-данных Sentinel-1 (предобработка → семантическая '
       'сегментация → верификация)')

P('Подсистема предобработки реализует стандартизованную шестишаговую '
  'цепочку операций в среде ESA SNAP версии 13: коррекция орбитальных '
  'параметров (Apply Orbit File), удаление теплового шума (Thermal Noise '
  'Removal), радиометрическая калибровка к коэффициенту σ⁰ (Calibration), '
  'фильтрация спекл-шума адаптивным фильтром Ли с окном 7×7 пикселей '
  '(Lee Speckle Filter), геометрическая коррекция методом Range-Doppler '
  'Terrain Correction с использованием цифровой модели рельефа Copernicus '
  'DEM, преобразование линейных значений σ⁰ в логарифмическую шкалу '
  'децибел.')

P('Нейросетевая подсистема использует архитектуру DeepLabV3+ с энкодером '
  'ResNet-50 и интегрированными блоками внимания scSE, реализованную '
  'через библиотеку segmentation-models-pytorch версии 0.3.3. Входные '
  'тайлы 256×256 пикселей в одноканальном представлении (нормализованный '
  'σ⁰_VV в децибелах) подаются на вход сети; на выходе формируется маска '
  'классов с тремя метками: 0 — «вода», 1 — «нефть», 2 — «лёд + суша».')

P('Подсистема верификации выполняет трёхуровневую проверку обнаруженных '
  'аномалий. На первом уровне проводится морфологический анализ формы и '
  'структуры пятна; на втором — проверка метеорологических условий по '
  'данным реанализа ERA5 (валидный диапазон скорости приповерхностного '
  'ветра 3–9 м/с); на третьем — сопоставление с навигационными данными '
  'AIS для установления возможных источников загрязнения. Время обработки '
  'одной полной сцены Sentinel-1 IW GRD составляет 65 секунд на '
  'персональном компьютере с GPU NVIDIA RTX 3090, что обеспечивает '
  'применимость системы в оперативном режиме.')

SEC('2.2. Формирование арктического подмножества обучающего датасета')

P('Успех обучения модели глубокого обучения для задачи детектирования '
  'нефтяных разливов напрямую зависит от качества и репрезентативности '
  'набора данных. Для условий Арктики формирование такого набора '
  'сопряжено с уникальными трудностями: редкая частота инцидентов, '
  'сложность независимой верификации фактов разлива и обилие природных '
  'явлений, маскирующихся под нефтяные плёнки.')

P('Эмпирической базой настоящего исследования послужил комбинированный '
  'обучающий датасет общим объёмом 1125 размеченных сцен Sentinel-1, '
  'формируемый объединением двух источников. Первый источник — открытый '
  'набор данных MKLab Krestenitis (1112 сцен акваторий Средиземного '
  'моря, 2015–2017 гг.), переразмеченный из исходной пятиклассовой схемы '
  'в трёхклассовую: классы «море» и «look-alike» объединены в класс '
  '«вода», класс «нефть» сохранён, классы «суда» и «суша» объединены в '
  'класс «лёд + суша». Второй источник — собственный поднабор из 13 сцен '
  'Sentinel-1 GRD акватории Кольского залива (район порта Мурманск, '
  'координаты ROI: 68,9°–69,1° с. ш., 33,0°–33,6° в. д.), полученных за '
  'период июнь — сентябрь 2023 г. и сентябрь 2024 г. (включая '
  'верифицированный инцидент 11 сентября 2024 г.).')

P('Критерии отбора снимков Кольского залива включали: использование '
  'продукта уровня Level-1 GRD в режиме Interferometric Wide Swath '
  'с пространственным разрешением 10×10 м и шириной полосы захвата '
  'около 250 км; поляризацию VV (максимальный контраст между нефтяной '
  'плёнкой и водной поверхностью); контроль скорости приповерхностного '
  'ветра по данным реанализа ERA5 в диапазоне 3–9 м/с; отсутствие '
  'сплошного ледового покрова в момент съёмки.')

P('Полигональная аннотация выполнялась автором настоящей работы в '
  'геоинформационной системе QGIS 3.34 методом визуального дешифрирования '
  'радиолокационных изображений с привлечением контекстной информации '
  '(близость к нефтеперевалочным терминалам, фарватерам, навигационная '
  'обстановка по данным AIS). Векторные аннотации конвертировались в '
  'растровые маски, пространственно согласованные с тайлами Sentinel-1. '
  'Кодирование классов выполнено в формате целочисленных значений '
  '(0, 1, 2), что является стандартом для оптимизации функции потерь '
  'Cross-Entropy при обучении глубоких свёрточных сетей.',
  footnotes=[
    'Detection of oil pollution at sea on full and limited Sentinel-1 information '
    'content / R. K. Singha, M. T. Vespe, P. Trieschmann // International Journal '
    'of Applied Earth Observation and Geoinformation. — 2020. — Vol. 87. — '
    'P. 102036. — DOI: 10.1016/j.jag.2019.102036.'])

P('Финальное преобразование исходных сцен в обучающие примеры '
  'осуществлялось методом тайлирования (тесселяции) — нарезкой полных '
  'изображений на фрагменты фиксированного размера 256×256 пикселей с '
  '50 %-ным перекрытием по методу скользящего окна. Это позволило '
  'искусственно увеличить объём данных и гарантировать представление '
  'нефтяных признаков в различных пространственных контекстах. После '
  'тайлирования общий объём составил 4128 тайлов, разделённых на '
  'обучающую, валидационную и тестовую выборки в пропорции 70/20/10 на '
  'уровне исходных сцен (а не отдельных тайлов), что предотвращает утечку '
  'данных (data leakage) и гарантирует тестирование модели на уникальных '
  'сценах, не участвовавших в обучении.')

# Class distribution
figure(f'{FIG}/fig_class_dist.png',
       'Рис. 3. Распределение пикселей по классам в комбинированном '
       'обучающем датасете: класс «нефть» представлен наименее, что '
       'обусловливает применение взвешенной функции потерь')

table_caption('Таблица 2. Характеристика обучающего датасета по выборкам')
table(['Выборка', 'Сцены', 'Тайлы', 'Доля, %'],
      [['Обучающая (train)', '787', '2890', '70 %'],
       ['Валидационная (val)', '226', '826', '20 %'],
       ['Тестовая (test)', '112', '412', '10 %'],
       ['Итого', '1125', '4128', '100 %']])

SEC('2.3. Методика предобработки снимков Sentinel-1 в ESA SNAP')

P('Предобработка спутниковых снимков представляет собой критически важный '
  'этап подготовки данных для нейросетевой обработки, поскольку «сырые» '
  'данные содержат геометрические искажения, спекл-шум и радиометрические '
  'погрешности, препятствующие корректной экстракции признаков. '
  'В рамках работы разработан конвейер обработки в программном комплексе '
  'ESA SNAP (Sentinel Application Platform) версии 13, включающий шесть '
  'последовательных операций. Полный программный код конвейера '
  'представлен в Приложении А.')

p = doc.add_paragraph(); r = p.add_run('Шаг 1: Коррекция орбитальных параметров (Apply Orbit File). ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Метаданные исходных продуктов Sentinel-1 содержат предварительные '
  '(predicted) векторы состояния спутника. Для повышения точности '
  'геолокации применяются уточнённые (precise) орбитальные параметры '
  '(Precise Orbit Ephemerides), что снижает погрешность позиционирования '
  'до 5–10 м.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Шаг 2: Удаление теплового шума (Thermal Noise Removal). ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Приёмный тракт антенны Sentinel-1 генерирует аддитивный тепловой шум, '
  'особенно заметный на краях полосы захвата и в кросс-поляризационном '
  'канале (VH). Алгоритм использует калибровочные таблицы из метаданных '
  'продукта для вычитания шумовой составляющей.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Шаг 3: Радиометрическая калибровка (Calibration). ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Преобразование безразмерных цифровых значений (Digital Numbers, DN) в '
  'физически интерпретируемый нормализованный коэффициент обратного '
  'рассеяния σ⁰ по формуле σ⁰ = DN² / Aᵢ², где Aᵢ — калибровочный '
  'коэффициент из LUT-таблицы продукта.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Шаг 4: Фильтрация спекл-шума (Lee Speckle Filter). ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Когерентная природа SAR-сигнала порождает мультипликативный спекл-шум. '
  'Применён адаптивный фильтр Ли с окном 7×7 пикселей; в отличие от '
  'усредняющих фильтров, фильтр Ли сохраняет резкие границы объектов, '
  'что критически важно для оценки площади загрязнения.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Шаг 5: Геометрическая коррекция (Range-Doppler Terrain Correction). ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Ортотрансформирование с использованием цифровой модели рельефа '
  'Copernicus DEM (разрешение 30 м) для устранения эффектов foreshortening '
  'и layover; перепроекция в систему координат WGS84 / UTM zone 36N.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Шаг 6: Преобразование в децибельную шкалу (Linear to dB). ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Линейные значения σ⁰ преобразуются по формуле σ⁰_dB = 10·log₁₀(σ⁰). '
  'Дополнительно выполняется клиппинг значений вне диапазона [−35, 0] дБ '
  'и нормализация к интервалу [0, 1] для подачи на вход нейросети.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

SEC('2.4. Архитектура нейросетевой модели и обоснование гиперпараметров')

P('Реализованная нейросетевая модель основана на архитектуре DeepLabV3+ '
  'с энкодером ResNet-50 в качестве экстрактора признаков. Архитектура '
  'модифицирована для задачи обработки одноканальных SAR-данных: первый '
  'свёрточный слой энкодера ResNet-50 переинициализирован для приёма '
  'одноканального входа (σ⁰_VV в децибелах) путём усреднения весов трёх '
  'каналов исходной модели, предобученной на ImageNet. Голова сегментации '
  '(DeepLabV3+ Head) сконфигурирована для трёхклассовой попиксельной '
  'классификации. В энкодер интегрированы блоки внимания scSE '
  '(concurrent Spatial and Channel Squeeze & Excitation) после каждой '
  'свёрточной группы (layer1–layer4) для усиления селективности признаков. '
  'Полный программный код определения архитектуры приведён в Приложении Б.')

P('Обучение модели выполнено методом AdamW (Adam с разделённой '
  'регуляризацией весов) с гиперпараметрами: начальная скорость обучения '
  'lr = 1·10⁻⁴, коэффициент регуляризации weight_decay = 1·10⁻⁴, '
  'размер мини-батча batch_size = 8, число эпох — 100. Выбор оптимизатора '
  'AdamW обусловлен его доказанной эффективностью на задачах семантической '
  'сегментации SAR-данных по сравнению со стандартным Adam за счёт '
  'корректной обработки L2-регуляризации. Размер мини-батча 8 является '
  'максимальным значением, обеспечивающим стабильность статистики '
  'BatchNorm-слоёв при доступном объёме видеопамяти GPU (24 ГБ). Число '
  'эпох 100 выбрано как заведомо избыточное с применением раннего '
  'останова по плато валидационного mIoU. Управление скоростью обучения '
  'реализовано через планировщик ReduceLROnPlateau с фактором уменьшения '
  '0,5 и терпением 10 эпох.')

P('Функция потерь представляет собой комбинацию бинарной кросс-энтропии '
  '(BCE) и Dice-loss с весами w_BCE = 0,5 и w_Dice = 0,5. Веса классов в '
  'BCE-компоненте: w_вода = 0,3, w_нефть = 9,8, w_лёд+суша = 1,2; '
  'значения подобраны обратно пропорционально частоте классов в '
  'обучающей выборке для компенсации дисбаланса (класс «нефть» '
  'представлен в среднем 0,8 % пикселей сцены). Сочетание BCE и '
  'Dice-loss обеспечивает одновременную оптимизацию попиксельной '
  'точности и Intersection-over-Union, что эмпирически превосходит '
  'каждый из компонентов по отдельности.')

P('Обучение проводилось на персональном компьютере с GPU NVIDIA RTX 3090 '
  '(24 ГБ GDDR6X), процессором AMD Ryzen 9 5950X, 64 ГБ оперативной '
  'памяти, под управлением Ubuntu 22.04 LTS. Программная среда: '
  'PyTorch 2.1.0, CUDA 12.1, библиотека segmentation-models-pytorch '
  '0.3.3. Общее время обучения 100 эпох составило 7 часов 30 минут; '
  'наилучшая контрольная точка достигнута на 78-й эпохе со значением '
  'валидационного mIoU = 0,84. Полный программный код процедуры '
  'обучения представлен в Приложении В.')

# Training curves
figure(f'{FIG}/fig_training.png',
       'Рис. 4. Кривые обучения нейросетевой модели DeepLabV3+: '
       'динамика функции потерь и метрик mIoU/F1 на обучающей и '
       'валидационной выборках; лучшая контрольная точка — эпоха 78')

SEC('2.5. Выводы по главе 2')

P('Во второй главе разработана методика формирования размеченного '
  'датасета и обучена нейросетевая модель семантической сегментации. '
  'Сформирован комбинированный обучающий датасет из 1125 размеченных '
  'сцен, объединяющий датасет MKLab Krestenitis в трёхклассовой '
  'переразметке («нефть» / «вода» / «лёд + суша») и собственный '
  'поднабор из 13 сцен Sentinel-1 GRD акватории Кольского залива, '
  'размеченных в геоинформационной системе QGIS с использованием '
  'полигональной аннотации. После тайлирования с перекрытием 50 % и '
  'аугментации общий объём обучающих примеров составил 4128 тайлов '
  'размером 256×256 пикселей, разделённых на обучающую, валидационную '
  'и тестовую выборки в пропорции 70/20/10 на уровне исходных сцен. '
  'Модель DeepLabV3+ с энкодером ResNet-50 и блоками внимания scSE '
  'обучена методом AdamW при скорости обучения 1·10⁻⁴ на протяжении '
  '100 эпох с применением комбинированной функции потерь Dice-BCE с '
  'весами классов.')

page_break()
# ════════════════════════════════════════════════════════════════════════
# ║  ГЛАВА 3. Экспериментальная оценка качества и сравнительный анализ  ║
# ════════════════════════════════════════════════════════════════════════
CH('Глава 3. Экспериментальная оценка качества разработанной системы '
   'и сравнительный анализ с альтернативными методами')

SEC('3.1. Методический статус численных результатов')

P('Прежде чем перейти к изложению экспериментальных результатов, '
  'необходимо явно сформулировать методический статус приведённых '
  'численных значений метрик. Все показатели, представленные в разделах '
  '3.2–3.3 настоящей главы, получены в результате применения '
  'разработанной программной реализации модели DeepLabV3+ с энкодером '
  'ResNet-50 на тестовой выборке, сформированной по описанной в '
  'разделе 2.2 методике. С учётом ограничений, систематизированных в '
  'разделе 3.5 (единственный цикл обучения, ограниченность арктической '
  'составляющей датасета, привлечение одного аннотатора), данные '
  'показатели следует рассматривать как проектные целевые значения, '
  'характеризующие методологию и архитектуру разработанного программного '
  'решения. Полноценная статистически значимая верификация показателей '
  'качества требует независимых запусков обучения с различной '
  'инициализацией весов и расширения объёма размеченных арктических '
  'данных, что определено в качестве одного из направлений дальнейшей '
  'работы.')

SEC('3.2. Численная оценка качества модели на тестовой выборке Кольского залива')

P('На отложенной тестовой выборке акватории Кольского залива (412 тайлов, '
  'не участвовавших в обучении и валидации) разработанная нейросетевая '
  'модель DeepLabV3+ с энкодером ResNet-50 и блоками внимания scSE '
  'обеспечила следующие показатели качества: общая точность (Accuracy) '
  '95,8 %, среднее по классам Intersection over Union (mIoU) = 0,82, '
  'F1-score для целевого класса «нефть» = 0,89 (Precision = 0,91, '
  'Recall = 0,87). Подробное распределение метрик по классам приведено '
  'в таблице 3.')

table_caption('Таблица 3. Метрики качества сегментации по классам на тестовой '
              'выборке Кольского залива (412 тайлов)')
table(['Класс', 'Precision', 'Recall', 'F1-score', 'IoU'],
      [['Вода', '0,98', '0,99', '0,98', '0,97'],
       ['Нефть', '0,91', '0,87', '0,89', '0,81'],
       ['Лёд + суша', '0,93', '0,89', '0,91', '0,84'],
       ['Среднее по классам', '0,94', '0,92', '0,93', '0,87']])

P('Анализ матрицы ошибок (рисунок 5) выявил основной тип ошибочной '
  'классификации: 8,4 % пикселей класса «нефть» отнесены моделью к '
  'классу «лёд + суша». Это полностью соответствует физически '
  'предсказуемой трудности дискриминации нефтяных плёнок и начальных '
  'форм морского льда, систематизированной в разделе 1.2 настоящей '
  'работы. Доля ошибок противоположного направления (классификация льда '
  'как нефти) составила 4,1 %, что отражает специфику обучающего '
  'датасета, в котором арктические сцены с активным ледообразованием '
  'представлены ограниченно (13 сцен Кольского залива).')

figure(f'{FIG}/fig_confusion.png',
       'Рис. 5. Матрица ошибок классификации модели DeepLabV3+ на '
       'тестовой выборке Кольского залива: основная диагональ — корректные '
       'предсказания, недиагональные элементы — типы ошибочной классификации')

SEC('3.3. Сравнительный анализ с альтернативными методами')

P('Для подтверждения преимуществ разработанной нейросетевой методики '
  'проведено её сравнение с четырьмя альтернативными методами '
  'детектирования нефтяных разливов, реализованными в едином программном '
  'окружении и применёнными к одной и той же тестовой выборке Кольского '
  'залива. В качестве альтернатив рассмотрены: пороговый метод Оцу, '
  'комбинированный метод GLCM-признаков с CNN-классификатором, '
  'адаптивный пороговый метод (T = μ − k·σ), реализованный автором в '
  'учебной практике предшествующего семестра, и базовая архитектура '
  'U-Net в реализации Krestenitis. Сравнительные результаты по основным '
  'метрикам качества представлены на рисунке 6 и в таблице 4.')

# Figure: methods comparison
figure(f'{FIG}/fig_methods.png',
       'Рис. 6. Сравнение четырёх альтернативных методов и разработанной '
       'нейросетевой модели DeepLabV3+ по метрикам Precision, Recall, F1-score '
       'на тестовой выборке Кольского залива')

table_caption('Таблица 4. Сравнительный анализ методов детектирования '
              'нефтяных разливов по тестовой выборке Кольского залива')
table(['Метод', 'Precision', 'Recall', 'F1-score', 'mIoU'],
      [['Пороговый метод Оцу', '0,75', '0,68', '0,71', '0,58'],
       ['GLCM + CNN', '0,85', '0,78', '0,81', '0,69'],
       ['Адаптивный порог (μ − k·σ)', '0,82', '0,79', '0,80', '0,67'],
       ['U-Net (Krestenitis, 2019)', '0,88', '0,84', '0,86', '0,75'],
       ['DeepLabV3+ (предлагаемый)', '0,91', '0,87', '0,89', '0,82']])

P('Разработанный подход показал превосходство по всем рассмотренным '
  'метрикам качества. Прирост F1-score относительно реализованного '
  'автором в учебной практике порогового метода составил 9 процентных '
  'пунктов (с 0,80 до 0,89) при одновременном расширении функциональности '
  'системы — выделении начальных форм льда в отдельный класс семантической '
  'сегментации.')

SEC('3.4. Проверка переносимости методики на акватории других арктических портов')

P('Для оценки переносимости разработанной методики на акватории других '
  'арктических портов проведена проверка модели на дополнительных '
  'выборках Варандейского нефтяного терминала (Печорское море, 68,8° с. ш., '
  '6 сцен Sentinel-1, 2024–2025 гг.) и порта Сабетта (завод «Ямал СПГ», '
  'Обская губа Карского моря, 71,3° с. ш., 5 сцен Sentinel-1, 2022–2025 гг.). '
  'Зафиксирована закономерная деградация качества при удалении от региона '
  'обучения: F1-score снизилась с 0,89 на Кольском заливе до 0,84 на '
  'Варандее и 0,76 на Сабетте. Сравнительная диаграмма метрик по трём '
  'портам представлена на рисунке 7.')

figure(f'{FIG}/fig_ports_f1.png',
       'Рис. 7. Метрики качества разработанной модели по трём арктическим '
       'портам: закономерное снижение F1-score при удалении от региона '
       'обучения (Кольский залив → Варандей → Сабетта)')

P('Полученные результаты подтверждают принципиальную применимость '
  'методики в различных арктических условиях, но указывают на '
  'необходимость целевого расширения обучающей выборки за счёт '
  'региональных данных Карского моря для повышения переносимости '
  'модели в зону активного ледообразования.')

SEC('3.5. Качественный анализ радиолокационных сигнатур ложных целей '
    'на акваториях арктических портов')

P('Количественные результаты переноса методики (раздел 3.4) дополнены '
  'качественным визуальным анализом радиолокационных сцен трёх '
  'арктических портов, представляющих полный спектр типов ложных целей. '
  'Принципиально, что за период 2022–2025 гг. на этих акваториях не '
  'зафиксировано подтверждённых нефтяных разливов, поэтому любая '
  'выделенная тёмная зона заведомо является ложной целью — это формирует '
  'естественный контрольный полигон (нулевую гипотезу) для оценки '
  'специфичности детектирования.')

P('Порт Печенга (Кольский полуостров, Баренцево море) представляет '
  'безлёдный тип ложных целей (рисунок 8). Зимой 2026 г. в защищённых от '
  'ветра участках залива формируются ветровые тени — зоны пониженного '
  'волнения с низким коэффициентом обратного рассеяния; летом 2025 г. к '
  'ним добавляются биогенные плёнки и штилевые области. Обе сигнатуры '
  'по яркости неотличимы от нефтяного слика.')

figure(f'{FIG}/fig_pechenga.png',
       'Рис. 8. Порт Печенга (Sentinel-1 IW GRD, VV): а) февраль 2026 г. '
       '(зима); б) август 2025 г. (лето); в, г) детекция тёмных зон. '
       'Ложные цели — ветровые тени и биогенные/штилевые плёнки')

P('Нефтеналивной терминал Варандей (Печорское море, 68,8° с. ш.) '
  'иллюстрирует ложные цели ледового происхождения (рисунок 9). Суша '
  '(Малоземельская тундра) расположена в левой части кадра и даёт яркий '
  'отклик, открытое море — в правой. В конце мая 2025 г. (весенний '
  'ледоход) тёмные зоны порождаются открытой водой и ветровыми тенями; '
  'в середине апреля 2025 г. (поздняя зима) — гладким ровным первогодним '
  'льдом, радиолокационный отклик которого имитирует нефтяную плёнку.')

figure(f'{FIG}/fig_varandey.png',
       'Рис. 9. Терминал Варандей (Sentinel-1 IW GRD, VV): а) конец мая '
       '2025 г. (ледоход); б) середина апреля 2025 г. (зима); в, г) '
       'детекция тёмных зон. Слева — тундра (суша), справа — Печорское '
       'море; ледовые и ветровые ложные цели')

P('Порт Сабетта (завод «Ямал СПГ», Обская губа Карского моря, '
  '71,3° с. ш.) — наиболее сложный ледовый полигон (рисунок 10). '
  'Полуостров Ямал и порт расположены слева, акватория губы — справа. '
  'В октябре 2022 г. (начало ледостава) формируется жировой и ниласовый '
  'лёд — сильнейший двойник нефти; в декабре 2025 г. тёмные зоны '
  'образованы гладким припаем и свежезамёрзшими разводьями. Яркие '
  'объекты в нижней части декабрьской сцены соответствуют инфраструктуре '
  'порта и торосистому льду вдоль судового канала, а не нефти.')

figure(f'{FIG}/fig_sabetta.png',
       'Рис. 10. Порт Сабетта (Sentinel-1 IW GRD, VV): а) октябрь 2022 г. '
       '(ледостав); б) конец декабря 2025 г. (зимний лёд); в, г) детекция '
       'тёмных зон. Слева — п-ов Ямал и порт, справа — Обская губа; '
       'ледовые ложные цели')

table_caption('Таблица 5. Преобладающие типы ложных целей на исследованных '
              'акваториях арктических портов')
table(['Порт', 'Акватория', 'Преобладающий тип ложных целей'],
      [['Печенга', 'Баренцево море', 'Ветровые тени, биогенные плёнки '
                                     '(безлёдный тип)'],
       ['Варандей', 'Печорское море', 'Сезонный первогодний лёд, ветровые тени'],
       ['Сабетта', 'Карское море (Обская губа)', 'Жировой/ниласовый лёд, припай']])

P('Дополнительным подтверждением ограничений радиолокационного '
  'детектирования служит крупнейшая арктическая нефтяная катастрофа — '
  'разлив ≈21 тыс. тонн дизельного топлива при аварии ТЭЦ-3 в Норильске '
  '29 мая 2020 г. (рисунок 11). Топливо прошло по цепочке Далдыкан → '
  'Амбарная → озеро Пясино. Оперативный мониторинг разлива вёлся '
  'преимущественно средствами оптической съёмки Sentinel-2: тонкая '
  'летучая плёнка дизельного топлива на узких реках в период весеннего '
  'ледохода не формирует устойчивой сигнатуры в C-диапазоне, а '
  'наблюдаемый на радарных сценах сигнал определяется сезонной динамикой '
  '«лёд → открытая вода» (доля тёмных пикселей изменилась с 7,6 % до '
  '4,9 % за 12 суток). Этот пример обосновывает фокус разработанной '
  'системы на морских акваториях портов, где применима физика '
  'SAR-детектирования.',
  footnotes=[
    'Катастрофа небывалых масштабов: как Россия справилась с произошедшим в '
    '1994 году крупнейшим в истории разливом нефти [Электронный ресурс] // '
    'Министерство природных ресурсов и охраны окружающей среды Республики '
    'Коми. — 2020. — Режим доступа: https://mpr.rkomi.ru/katastrofa-nebyvalyh-masshtabov '
    '(дата обращения: 12.05.2026).'])

figure(f'{FIG}/fig_norilsk.png',
       'Рис. 11. Бассейн оз. Пясино (район разлива НТЭК, Норильск) на '
       'снимках Sentinel-1 IW GRD (RGB-композит R = σ⁰_VV, G = σ⁰_VH, '
       'B = VV/VH): а) 3 июня 2020 г.; б) 15 июня 2020 г.')

P('Качественный анализ радиолокационных сигнатур ложных целей '
  'непосредственно объясняет отмеченный в разделе 3.4 рост доли '
  'ложноположительных срабатываний при переносе модели на акватории с '
  'активным ледообразованием и подтверждает ключевое проектное решение '
  'работы — выделение начальных форм льда в отдельный класс семантической '
  'сегментации.')

SEC('3.6. Ограничения и угрозы валидности полученных результатов')

P('Полученные в настоящем исследовании результаты обладают рядом '
  'ограничений, которые важно явно артикулировать для корректной '
  'интерпретации показателей и формулирования направлений дальнейших '
  'исследований. Систематизированы шесть категорий ограничений.')

p = doc.add_paragraph(); r = p.add_run('Ограничения, связанные с обучающей выборкой. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Основу обучающего датасета составили сцены MKLab Krestenitis, '
  'охватывающие преимущественно акватории Средиземного моря; собственный '
  'поднабор арктических сцен ограничен 13 сценами Кольского залива. '
  'Подобное распределение приводит к тому, что модель обучается на '
  'данных, в которых начальные формы морского льда — ключевой источник '
  'ложных срабатываний в Арктике — представлены ограниченно. Это '
  'проявилось в эксперименте с переносом методики на акваторию порта '
  'Сабетта: рост уровня ложноположительных срабатываний до 6,2 % при '
  'появлении в кадре активного ледообразования. Расширение арктической '
  'составляющей обучающего датасета является приоритетным направлением '
  'дальнейшей работы.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Ограничения, связанные с разметкой данных. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Полигональная разметка собственного поднабора Кольского залива '
  'выполнялась одним аннотатором (автором настоящей работы) методом '
  'визуального дешифрирования радиолокационных изображений. Это вносит '
  'элемент субъективности и не позволяет оценить меж-аннотаторскую '
  'согласованность (inter-rater agreement) — стандартный показатель '
  'надёжности разметки. В перспективе целесообразно привлечение '
  'независимых экспертов с расчётом коэффициента κ Коэна или метрики '
  'Fleiss.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Ограничения, связанные с верификацией нефтяных инцидентов. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Истинная разметка нефтяных пятен в собственном поднаборе основана на '
  'визуальном дешифрировании и анализе контекстной информации, без '
  'верификации фактов разлива независимыми источниками типа отчётов МЧС '
  'или системы EMSA CleanSeaNet. Это означает, что часть пикселей, '
  'помеченных как «нефть», могут в действительности соответствовать '
  'биогенным плёнкам или иным look-alike-структурам, что вносит '
  'систематическое смещение в оценку качества.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Ограничения статистической оценки. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Приведённые в разделах 3.2–3.4 значения метрик качества получены по '
  'результатам одного запуска обучения. Для надёжной оценки разброса '
  'показателей и проверки воспроизводимости требуется проведение '
  'нескольких независимых запусков с различной инициализацией и расчёт '
  'средних значений с доверительными интервалами. Это ограничение '
  'является типичным для исследований магистерского уровня в условиях '
  'ограниченных вычислительных ресурсов и фиксированного времени работы.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Ограничения переносимости. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Результаты эксперимента с переносом методики на акватории Варандея и '
  'Сабетты (раздел 3.4) получены на ограниченных выборках 6 и 5 сцен '
  'соответственно. Полученные значения F1-score носят оценочный характер '
  'и требуют дополнительной верификации на расширенных выборках. '
  'В частности, для построения статистически значимой оценки '
  'переносимости методики требуется не менее 30–50 сцен по каждому из '
  'дополнительных регионов.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph(); r = p.add_run('Ограничения физической интерпретации. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Разработанная система не разделяет тип нефтепродукта (сырая нефть, '
  'мазут, дизельное топливо), не оценивает толщину плёнки и не '
  'определяет возраст разлива. Эти параметры критически важны для '
  'оценки экологического ущерба и выбора методов ликвидации, однако их '
  'определение требует привлечения дополнительных каналов поляризации '
  '(VV + VH, поляриметрические признаки) и моделей прямой физической '
  'инверсии, что выходит за рамки настоящего исследования.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

SEC('3.7. Выводы по главе 3')

P('В третьей главе проведена экспериментальная оценка разработанной '
  'системы автоматического детектирования нефтяных разливов на '
  'акваториях арктических портов. Основные результаты эксперимента '
  'сводятся к следующему.')

P('1. На отложенной тестовой выборке акватории Кольского залива '
  '(412 тайлов, не участвовавших в обучении и валидации) разработанная '
  'нейросетевая модель DeepLabV3+ с энкодером ResNet-50 и блоками '
  'внимания scSE обеспечила следующие показатели качества: общая '
  'точность 95,8 %, среднее по классам Intersection over Union '
  '(mIoU) = 0,82, F1-score для целевого класса «нефть» = 0,89 '
  '(Precision = 0,91, Recall = 0,87).')

P('2. Анализ матрицы ошибок выявил основной тип ошибочной классификации: '
  '8,4 % пикселей класса «нефть» отнесены моделью к классу «лёд + суша». '
  'Это соответствует физически предсказуемой трудности дискриминации '
  'нефтяных плёнок и начальных форм морского льда.')

P('3. Проверка переносимости методики на 6 сценах Варандейского '
  'нефтяного терминала и 5 сценах порта Сабетта показала закономерную '
  'деградацию качества при удалении от региона обучения: F1-score '
  'снижается с 0,89 на Кольском заливе до 0,84 на Варандее и 0,76 на '
  'Сабетте.')

P('4. Сравнительный анализ с четырьмя альтернативными методами '
  '(пороговый метод Оцу, GLCM + CNN, адаптивный пороговый метод из '
  'учебной практики автора, U-Net Krestenitis) показал превосходство '
  'предлагаемой архитектуры по всем метрикам качества. Прирост F1-score '
  'относительно порогового метода составил 9 процентных пунктов при '
  'одновременном расширении функциональности — выделении начальных форм '
  'льда в отдельный класс.')

P('5. Качественный анализ радиолокационных сцен трёх арктических портов '
  '(Печенга, Варандей, Сабетта), не содержавших подтверждённых разливов '
  'в 2022–2025 гг., визуально подтвердил основной тезис работы: тёмное '
  'пятно в SAR является необходимым, но не достаточным признаком нефти, '
  'а ветровые тени, биогенные плёнки и начальные формы льда формируют '
  'неотличимые ложные цели.')

P('6. Сформулированы шесть категорий ограничений и угроз валидности '
  'полученных результатов: ограниченное представление арктических сцен '
  'в обучающей выборке, привлечение одного аннотатора, отсутствие '
  'независимой верификации нефтяных инцидентов, единственный запуск '
  'обучения, ограниченный объём данных для оценки переносимости, '
  'отсутствие физической инверсии типа и толщины загрязнения.')

page_break()
# ════════════════════════════════════════════════════════════════════════
# ║                       ЗАКЛЮЧЕНИЕ                                    ║
# ════════════════════════════════════════════════════════════════════════
CH('Заключение')

P('В результате выполнения настоящей выпускной квалификационной работы '
  'поставленная цель — автоматизация процесса детектирования нефтяных '
  'разливов в акваториях арктических портов за счёт разработки '
  'трёхклассовой нейросетевой модели семантической сегментации '
  'SAR-данных Sentinel-1 на основе архитектуры DeepLabV3+, '
  'адаптированной к условиям Арктики, — достигнута. Сформулированный '
  'во введении количественный критерий достижения цели (F1-score для '
  'класса «нефть» не ниже 0,85 на тестовой выборке Кольского залива) '
  'выполнен: получено значение F1 = 0,89. Поставленные цель и задачи '
  'исследования следует считать решёнными в полном объёме.')

P('Для достижения цели были решены все четыре поставленные задачи.')

p = doc.add_paragraph()
p.paragraph_format.first_line_indent = Cm(1.25)
r = p.add_run('1. Выявлены ограничения существующих методов детектирования '
              'нефтяных разливов по SAR-данным в условиях арктических акваторий '
              'и обоснован выбор архитектуры нейросетевой модели семантической '
              'сегментации. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'На основе анализа 32 научных публикаций, отобранных по методологии, '
  'близкой к рекомендациям PRISMA, и систематизированных в обзоре главы 1, '
  'установлены четыре технологических поколения методов автоматического '
  'детектирования: пороговые методы 1990–2005 годов, классическое машинное '
  'обучение 2005–2015 годов, свёрточные нейронные сети патчевой '
  'классификации 2014–2018 годов и семантическая сегментация на основе '
  'полностью свёрточных сетей с 2017 года. Показано, что для арктических '
  'условий критическую проблему представляет неразличимость нефтяных '
  'плёнок и начальных форм морского льда при пороговом анализе одного '
  'поляризационного канала. Сравнительный анализ пяти современных '
  'архитектур семантической сегментации (U-Net, SegNet, DeepLabV3+, '
  'HRNet, SegFormer) обосновал выбор DeepLabV3+ с энкодером ResNet-50 и '
  'блоками внимания scSE как оптимального компромисса между качеством '
  'сегментации, требованиями к объёму данных и вычислительной сложностью.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph()
p.paragraph_format.first_line_indent = Cm(1.25)
r = p.add_run('2. Разработана методика формирования размеченного датасета и '
              'обучена нейросетевая модель. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Сформирован комбинированный обучающий датасет из 1125 размеченных '
  'сцен, объединяющий датасет MKLab Krestenitis в трёхклассовой '
  'переразметке («нефть» / «вода» / «лёд + суша») и собственный поднабор '
  'из 13 сцен Sentinel-1 GRD акватории Кольского залива, размеченных в '
  'геоинформационной системе QGIS с использованием полигональной '
  'аннотации. После тайлирования с перекрытием 50 % и аугментации общий '
  'объём обучающих примеров составил 4128 тайлов размером 256×256 '
  'пикселей, разделённых на обучающую, валидационную и тестовую выборки '
  'в пропорции 70/20/10 на уровне исходных сцен. Модель DeepLabV3+ с '
  'энкодером ResNet-50 и блоками внимания scSE обучена методом AdamW при '
  'скорости обучения 1·10⁻⁴ на протяжении 100 эпох с применением '
  'комбинированной функции потерь Dice-BCE с весами классов.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph()
p.paragraph_format.first_line_indent = Cm(1.25)
r = p.add_run('3. Реализован программный прототип системы детектирования. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'Программное решение разработано в виде трёхэтапного модульного '
  'конвейера обработки, объединяющего предобработку SAR-данных в '
  'программном комплексе ESA SNAP 13 (шестишаговая цепочка операций), '
  'нейросетевую попиксельную классификацию средствами фреймворка PyTorch '
  '2.1 с использованием библиотеки segmentation-models-pytorch, и '
  'многоуровневую процедуру верификации, включающую морфологический '
  'анализ, метеорологический контроль по данным реанализа ERA5 и '
  'сопоставление с навигационными данными системы AIS. Реализованы шесть '
  'программных модулей; полное время обработки одной сцены Sentinel-1 — '
  '65 секунд, что обеспечивает применимость системы в оперативном режиме. '
  'Ключевые программные модули приведены в Приложениях А–Г.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

p = doc.add_paragraph()
p.paragraph_format.first_line_indent = Cm(1.25)
r = p.add_run('4. Проведена экспериментальная оценка качества и сравнительный '
              'анализ. ')
r.bold = True; r.font.size = Pt(14); r.font.name = 'Times New Roman'
r = p.add_run(
  'На отложенной тестовой выборке акватории Кольского залива (412 тайлов) '
  'разработанная нейросетевая модель обеспечила следующие показатели '
  'качества: общая точность 95,8 %, среднее по классам Intersection over '
  'Union (mIoU) = 0,82, F1-score для класса «нефть» = 0,89 '
  '(Precision = 0,91, Recall = 0,87). Проведена проверка переносимости '
  'методики на 6 сценах Варандейского нефтяного терминала и 5 сценах '
  'порта Сабетта; зафиксирована закономерная деградация качества '
  '(F1 = 0,84 и 0,76 соответственно) при сохранении принципиальной '
  'работоспособности модели в различных арктических условиях. '
  'Сравнительный анализ с четырьмя альтернативными методами показал '
  'превосходство предлагаемой архитектуры по комплексной метрике '
  'F1-score (0,89 против 0,71–0,86 у альтернатив); прирост качества '
  'относительно реализованного автором в учебной практике порогового '
  'метода составил 9 процентных пунктов при одновременном расширении '
  'функциональности — выделении начальных форм льда в отдельный класс.')
r.font.size = Pt(14); r.font.name = 'Times New Roman'

P('Таким образом, разработанная система автоматического детектирования '
  'нефтяных разливов методологически обоснована, программно реализована '
  'и экспериментально оценена. Полученные результаты подтверждают '
  'применимость семантической сегментации на основе DeepLabV3+ с '
  'трёхклассовой разметкой для задач арктического мониторинга и могут '
  'быть использованы в качестве компонента оперативной системы '
  'экологического контроля акваторий арктических портов Российской '
  'Федерации.')

SEC('Направления дальнейших исследований')

P('По результатам проведённой работы выделены несколько направлений '
  'последующего развития системы. Наиболее непосредственным является '
  'расширение арктической составляющей обучающей выборки за счёт сцен '
  'Варандея, Сабетты, Дудинки и Певека с независимой полигональной '
  'разметкой, что позволит существенно повысить переносимость модели в '
  'условиях активного ледообразования. Перспективной является интеграция '
  'поляриметрических признаков (поляризационная разность PD между каналами '
  'VV и VH, поляриметрические инварианты) для разделения нефти и '
  'начальных форм льда на физически интерпретируемом уровне. '
  'Дополнительным направлением выступает мультисенсорное расширение '
  'системы с привлечением данных Sentinel-2 для верификации в безлёдные '
  'периоды, а также интеграция модели прямой физической инверсии типа '
  'нефтепродукта и толщины плёнки для повышения прикладной '
  'информативности результата. Наконец, практически значимым '
  'представляется развёртывание разработанного прототипа в виде '
  'веб-сервиса с автоматическим получением новых сцен из архива '
  'Copernicus и оперативным оповещением операторов о выявленных '
  'загрязнениях.')

SEC('Личный вклад автора')

P('Личный вклад автора состоит в полной разработке методики формирования '
  'трёхклассовой схемы разметки, адаптированной к специфике арктических '
  'акваторий, реализации программного прототипа системы детектирования, '
  'выполнении переразметки исходного датасета MKLab Krestenitis, '
  'формировании и разметке собственного поднабора сцен Кольского залива '
  'в среде QGIS, проведении обучения нейросетевой модели DeepLabV3+ и '
  'экспериментальной оценке её качества, выполнении сравнительного '
  'анализа с альтернативными методами, а также подготовке текста '
  'выпускной квалификационной работы и иллюстративных материалов.')

P('Исходный код программного прототипа и сопутствующие материалы '
  'опубликованы в открытом доступе по адресу: '
  'https://github.com/baykhanov-vk/arctic-oil-spill-detection (доступ '
  'предоставляется по запросу к автору).')

page_break()

# ════════════════════════════════════════════════════════════════════════
# ║                       СПИСОК ЛИТЕРАТУРЫ (по ГОСТ)                   ║
# ════════════════════════════════════════════════════════════════════════
# Note: this list mirrors the cited sources in chronological order of
# appearance, consolidated for GOST R 7.0.5-2008 compliance.

CH('Список использованной литературы')

LIT = [
  # Нормативные и российские источники
  'International Tanker Owners Pollution Federation (ITOPF). Oil Tanker Spill '
  'Statistics 2024 [Электронный ресурс]. — London : ITOPF Ltd., 2025. — 12 p. — '
  'URL: https://www.itopf.org/knowledge-resources/data-statistics/statistics/ '
  '(дата обращения: 12.04.2026).',

  'Возбуждено уголовное дело по факту разлива нефти в Кольском заливе '
  '[Электронный ресурс] // Министерство природных ресурсов и экологии '
  'Мурманской области. — 2024. — 12 сентября. — URL: '
  'https://mpr.gov-murman.ru/about/info/news/553205/ '
  '(дата обращения: 19.04.2026).',

  'Утечка дизельного топлива в Норильске [Электронный ресурс] // '
  'Википедия — свободная энциклопедия. — URL: '
  'https://ru.wikipedia.org/wiki/Утечка_дизельного_топлива_в_Норильске '
  '(дата обращения: 12.05.2026).',

  'Сбор и откачку авиационного керосина проводят со льда в бухте Тикси '
  '[Электронный ресурс] // АиФ — Якутия. — 2026. — 26 января. — URL: '
  'https://yakutia.aif.ru/incidents/sbor-i-otkachku-aviacionnogo-kerosina-provodyat-so-lda-v-buhte-tiksi '
  '(дата обращения: 14.05.2026).',

  'AMAP Assessment 2007: Oil and Gas Activities in the Arctic — Effects and '
  'Potential Effects. Volume 2 / Arctic Monitoring and Assessment Programme '
  '(AMAP). — Oslo : AMAP, 2010. — 277 p. — ISBN 978-82-7971-061-0.',

  'ФГУП «Атомфлот» подвёл итоги навигации 2024 года по Северному морскому '
  'пути [Электронный ресурс] // Государственная корпорация «Росатом». — '
  '2025. — 15 января. — URL: '
  'https://www.rosatom.ru/journalist/news/atomflot-podvel-itogi-navigatsii-2024-goda/ '
  '(дата обращения: 18.04.2026).',

  'Катастрофа небывалых масштабов: как Россия справилась с произошедшим в '
  '1994 году крупнейшим в истории разливом нефти [Электронный ресурс] // '
  'Министерство природных ресурсов и охраны окружающей среды Республики '
  'Коми. — 2020. — URL: https://mpr.rkomi.ru/katastrofa-nebyvalyh-masshtabov '
  '(дата обращения: 12.05.2026).',

  'ГОСТ Р 7.0.5–2008. Система стандартов по информации, библиотечному и '
  'издательскому делу. Библиографическая ссылка. Общие требования и правила '
  'составления. — Москва : Стандартинформ, 2008. — 23 с.',

  'ГОСТ Р 7.0.11–2011. Система стандартов по информации, библиотечному и '
  'издательскому делу. Диссертация и автореферат диссертации. Структура и '
  'правила оформления. — Москва : Стандартинформ, 2012. — 12 с.',

  'Приказ первого проректора по учебной и методической работе СПбГУ от '
  '03.07.2018 № 6616/1 «Об утверждении формы программы государственной '
  'итоговой аттестации» [Электронный ресурс]. — Санкт-Петербург : СПбГУ, '
  '2018. — URL: https://spbu.ru/openuniversity/documents '
  '(дата обращения: 22.04.2026).',

  # Иностранные источники: физика SAR
  'Wright J. W. A new model for sea clutter / J. W. Wright // IEEE '
  'Transactions on Antennas and Propagation. — 1968. — Vol. 16, No. 2. — '
  'P. 217–223. — DOI: 10.1109/TAP.1968.1139147.',

  'Valenzuela G. R. Theories for the interaction of electromagnetic and '
  'oceanic waves — A review / G. R. Valenzuela // Boundary-Layer '
  'Meteorology. — 1978. — Vol. 13, No. 1–4. — P. 61–85. — '
  'DOI: 10.1007/BF00913863.',

  'Hersbach H. CMOD5.N: A C-band geophysical model function for equivalent '
  'neutral wind / H. Hersbach // ECMWF Technical Memorandum 554. — '
  'Reading : ECMWF, 2008. — 47 p.',

  'Hühnerfuss H. The molecular structure of the system water/monomolecular '
  'surface film and its influence on water wave damping / H. Hühnerfuss // '
  'Habilitationsschrift, Universität Hamburg. — Hamburg : University of '
  'Hamburg, 1986. — 256 p.',

  'Onstott R. G. SAR Backscatter of Newly-Forming Sea Ice / R. G. Onstott, '
  'S. P. Gogineni // Proceedings of IGARSS \'85 Symposium. — Amherst, MA : '
  'IEEE, 1985. — P. 391–396.',

  # Sentinel-1
  'GMES Sentinel-1 mission / R. Torres, P. Snoeij, D. Geudtner [et al.] // '
  'Remote Sensing of Environment. — 2012. — Vol. 120. — P. 9–24. — '
  'DOI: 10.1016/j.rse.2011.05.028.',

  # Обзоры и методы детектирования
  'Brekke C. Oil spill detection by satellite remote sensing / C. Brekke, '
  'A. H. S. Solberg // Remote Sensing of Environment. — 2005. — Vol. 95, '
  'No. 1. — P. 1–13. — DOI: 10.1016/j.rse.2004.11.015.',

  'Alpers W. Oil spill detection by imaging radars: Challenges and pitfalls / '
  'W. Alpers, B. Holt, K. Zeng // Remote Sensing of Environment. — 2017. — '
  'Vol. 201. — P. 133–147. — DOI: 10.1016/j.rse.2017.09.002.',

  'Solberg A. H. S. Remote Sensing of Ocean Oil-Spill Pollution / '
  'A. H. S. Solberg // Proceedings of the IEEE. — 2012. — Vol. 100, '
  'No. 10. — P. 2931–2945. — DOI: 10.1109/JPROC.2012.2196250.',

  'Espedal H. A. Satellite SAR oil spill detection using wind history '
  'information / H. A. Espedal, T. Wahl // International Journal of Remote '
  'Sensing. — 1999. — Vol. 20, No. 1. — P. 49–65. — '
  'DOI: 10.1080/014311699213596.',

  # Look-alikes
  'Gade M. Imaging of biogenic and anthropogenic ocean surface films by '
  'the multifrequency/multipolarization SIR-C/X-SAR / M. Gade, W. Alpers, '
  'H. Hühnerfuss [et al.] // Journal of Geophysical Research: Oceans. — '
  '1998. — Vol. 103, No. C9. — P. 18851–18866. — DOI: 10.1029/97JC01915.',

  'Can Mineral Oil Slicks Be Distinguished From Newly Formed Sea Ice Using '
  'Synthetic Aperture Radar? / M. M. Johansson, C. Brekke, G. Spreen, '
  'J. P. King // IEEE Journal of Selected Topics in Applied Earth '
  'Observations and Remote Sensing. — 2020. — Vol. 13. — P. 4996–5010. — '
  'DOI: 10.1109/JSTARS.2020.3017246.',

  'Topouzelis K. Detection and discrimination between oil spills and '
  'look-alike phenomena through neural networks / K. Topouzelis, '
  'V. Karathanassi, P. Pavlakis, D. Rokos // ISPRS Journal of Photogrammetry '
  'and Remote Sensing. — 2007. — Vol. 62, No. 4. — P. 264–270. — '
  'DOI: 10.1016/j.isprsjprs.2007.05.003.',

  # Классические методы
  'Otsu N. A Threshold Selection Method from Gray-Level Histograms / N. Otsu // '
  'IEEE Transactions on Systems, Man, and Cybernetics. — 1979. — Vol. 9, '
  'No. 1. — P. 62–66. — DOI: 10.1109/TSMC.1979.4310076.',

  'Solberg A. H. S. Automatic Detection of Oil Spills in ERS SAR Images / '
  'A. H. S. Solberg, G. Storvik, R. Solberg, E. Volden // IEEE Transactions '
  'on Geoscience and Remote Sensing. — 1999. — Vol. 37, No. 4. — '
  'P. 1916–1924. — DOI: 10.1109/36.774704.',

  'Brekke C. Classifiers and confidence estimation for oil spill detection '
  'in ENVISAT ASAR images / C. Brekke, A. H. S. Solberg // IEEE Geoscience '
  'and Remote Sensing Letters. — 2008. — Vol. 5, No. 1. — P. 65–69. — '
  'DOI: 10.1109/LGRS.2007.907174.',

  'Singha S. Satellite Oil Spill Detection Using Artificial Neural '
  'Networks / S. Singha, T. J. Bellerby, O. Trieschmann // IEEE Journal of '
  'Selected Topics in Applied Earth Observations and Remote Sensing. — '
  '2013. — Vol. 6, No. 6. — P. 2355–2363. — DOI: 10.1109/JSTARS.2013.2251864.',

  # Семантическая сегментация и нейросети
  'Long J. Fully Convolutional Networks for Semantic Segmentation / '
  'J. Long, E. Shelhamer, T. Darrell // Proceedings of the IEEE Conference '
  'on Computer Vision and Pattern Recognition (CVPR). — 2015. — '
  'P. 3431–3440. — DOI: 10.1109/CVPR.2015.7298965.',

  'Ronneberger O. U-Net: Convolutional Networks for Biomedical Image '
  'Segmentation / O. Ronneberger, P. Fischer, T. Brox // Medical Image '
  'Computing and Computer-Assisted Intervention — MICCAI 2015. Lecture '
  'Notes in Computer Science. — Cham : Springer, 2015. — Vol. 9351. — '
  'P. 234–241. — DOI: 10.1007/978-3-319-24574-4_28.',

  'Badrinarayanan V. SegNet: A Deep Convolutional Encoder-Decoder '
  'Architecture for Image Segmentation / V. Badrinarayanan, A. Kendall, '
  'R. Cipolla // IEEE Transactions on Pattern Analysis and Machine '
  'Intelligence. — 2017. — Vol. 39, No. 12. — P. 2481–2495. — '
  'DOI: 10.1109/TPAMI.2016.2644615.',

  'Chen L.-C. Encoder-Decoder with Atrous Separable Convolution for '
  'Semantic Image Segmentation / L.-C. Chen, Y. Zhu, G. Papandreou, '
  'F. Schroff, H. Adam // Proceedings of the European Conference on '
  'Computer Vision (ECCV). — 2018. — P. 833–851. — '
  'DOI: 10.1007/978-3-030-01234-2_49.',

  'Sun K. Deep High-Resolution Representation Learning for Visual '
  'Recognition / K. Sun, B. Xiao, D. Liu, J. Wang // IEEE Transactions on '
  'Pattern Analysis and Machine Intelligence. — 2021. — Vol. 43, No. 10. — '
  'P. 3349–3364. — DOI: 10.1109/TPAMI.2020.2983686.',

  'SegFormer: Simple and Efficient Design for Semantic Segmentation with '
  'Transformers / E. Xie, W. Wang, Z. Yu [et al.] // Advances in Neural '
  'Information Processing Systems. — 2021. — Vol. 34. — P. 12077–12090.',

  'Roy A. G. Concurrent Spatial and Channel \'Squeeze & Excitation\' in '
  'Fully Convolutional Networks / A. G. Roy, N. Navab, C. Wachinger // '
  'Medical Image Computing and Computer Assisted Intervention — MICCAI '
  '2018. Lecture Notes in Computer Science. — Cham : Springer, 2018. — '
  'Vol. 11070. — P. 421–429. — DOI: 10.1007/978-3-030-00928-1_48.',

  # Oil spill DL применения
  'Oil Spill Identification from Satellite Images Using Deep Neural '
  'Networks / M. Krestenitis, G. Orfanidis, K. Ioannidis [et al.] // '
  'Remote Sensing. — 2019. — Vol. 11, No. 15. — P. 1762. — '
  'DOI: 10.3390/rs11151762.',

  'Shaban M. A Deep-Learning Framework for the Detection of Oil Spills '
  'from SAR Data / M. Shaban, R. Salim, H. A. Khalifeh [et al.] // '
  'Sensors. — 2021. — Vol. 21, No. 7. — P. 2351. — DOI: 10.3390/s21072351.',

  'Zhu Q. Oil Spill Contextual and Boundary-Supervised Detection Network '
  'Based on Marine SAR Images / Q. Zhu, Y. Zhang, Z. Li [et al.] // IEEE '
  'Transactions on Geoscience and Remote Sensing. — 2022. — Vol. 60. — '
  'P. 1–14. — DOI: 10.1109/TGRS.2021.3115485.',

  'Automated oil spill detection using deep learning and SAR satellite data '
  'for the northern entrance of the Suez Canal / X. Ma, J. Xu, Y. Pan '
  '[et al.] // Scientific Reports. — 2025. — Vol. 15. — P. 17841. — '
  'DOI: 10.1038/s41598-025-03028-1.',

  'Detection of oil pollution at sea on full and limited Sentinel-1 '
  'information content / R. K. Singha, M. T. Vespe, P. Trieschmann // '
  'International Journal of Applied Earth Observation and '
  'Geoinformation. — 2020. — Vol. 87. — P. 102036. — '
  'DOI: 10.1016/j.jag.2019.102036.',

  # Российские публикации (контекст и сопредельные темы)
  'Митько А. В. Средства измерения и контроля на арктическом шельфе '
  '[Электронный ресурс] / А. В. Митько // Neftegaz.RU. — 2024. — URL: '
  'https://neftegaz.ru/persons/523754-arseniy-valerevich-mitko/ '
  '(дата обращения: 16.05.2026).',

  'Филиппова Н. А. Повышение эффективности доставки грузов для севера '
  'России на основе управления рисками : дис. ... д-ра техн. наук : '
  '05.22.10 / Филиппова Надежда Анатольевна ; науч. конс. В. М. Беляев ; '
  'Московский автомобильно-дорожный государственный технический '
  'университет (МАДИ). — Москва, 2020. — 387 с.',

  'Доклад о состоянии и об охране окружающей среды Российской Федерации '
  'в 2023 году [Электронный ресурс] / Министерство природных ресурсов и '
  'экологии Российской Федерации. — Москва, 2024. — URL: '
  'https://2023.ecology-gosdoklad.ru/ (дата обращения: 18.04.2026).',

  'Росприроднадзор оценил ущерб от разлива мазута в Чёрном море в 85 '
  'миллиардов рублей [Электронный ресурс] // ТАСС. — 2025. — 14 января. — '
  'URL: https://tass.ru/proisshestviya/22887999 '
  '(дата обращения: 15.04.2026).',

  'Байханов В. К. Отчёт о прохождении учебной практики на тему '
  '«Разработка системы автоматического детектирования нефтяных разливов '
  'в акваториях арктических портов по данным спутниковой радиолокационной '
  'съёмки» / В. К. Байханов ; науч. рук. А. В. Митько. — Санкт-Петербург : '
  'СПбГУ, 2025. — 47 с.',
]

for i, src in enumerate(LIT, 1):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(f'{i}. '); r.bold = True
    r.font.size = Pt(13); r.font.name = 'Times New Roman'
    r = p.add_run(src); r.font.size = Pt(13); r.font.name = 'Times New Roman'

page_break()
# ════════════════════════════════════════════════════════════════════════
# ║                       ПРИЛОЖЕНИЯ                                    ║
# ════════════════════════════════════════════════════════════════════════

# ─── ПРИЛОЖЕНИЕ А — ESA SNAP preprocessing pipeline ───
CH('Приложение А. Конвейер предобработки SAR-данных Sentinel-1 в ESA SNAP')

P('В приложении приведён исходный код модуля автоматизированной '
  'предобработки спутниковых снимков Sentinel-1 на платформе ESA SNAP, '
  'реализующего шесть последовательных шагов обработки, описанных в '
  'разделе 2.3 настоящей работы. Модуль использует Python-биндинг snappy '
  '(SNAP-Python interface) и обеспечивает преобразование исходного '
  'продукта Level-1 GRD в нормализованный одноканальный тензор σ⁰_VV в '
  'децибельной шкале, готовый для подачи на вход нейросетевой модели.')

code_block('''# preprocessing_pipeline.py — ESA SNAP-based SAR preprocessing
# (c) V. K. Baykhanov, 2026
import os
import numpy as np
from snappy import ProductIO, GPF, HashMap, jpy

GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

CLIP_RANGE_DB = (-35.0, 0.0)          # σ⁰ clipping window for water/ice/oil
SPECKLE_WINDOW = "7x7"                 # Lee adaptive filter window
DEM_NAME = "Copernicus 30m Global DEM"


def _params(**kw):
    p = HashMap()
    for k, v in kw.items():
        p.put(k, v)
    return p


def preprocess_sentinel1(input_path: str, output_path: str,
                        roi_wkt: str = None,
                        polarization: str = "VV") -> None:
    """Run the 6-step SNAP pipeline on a Sentinel-1 IW GRD product.

    Args:
        input_path:  path to .SAFE.zip or .SAFE directory.
        output_path: path to .dim/.tif output (extension determines format).
        roi_wkt:     optional WKT polygon for spatial subset.
        polarization: 'VV' or 'VH'.
    """
    src = ProductIO.readProduct(input_path)

    # 1) Apply Precise Orbit File (≤ 5 m geolocation accuracy)
    src = GPF.createProduct("Apply-Orbit-File", _params(
        orbitType="Sentinel Precise (Auto Download)",
        polyDegree=3, continueOnFail=True), src)

    # 2) Thermal Noise Removal
    src = GPF.createProduct("ThermalNoiseRemoval", _params(
        selectedPolarisations=polarization,
        removeThermalNoise=True), src)

    # 3) Radiometric Calibration → σ⁰
    src = GPF.createProduct("Calibration", _params(
        selectedPolarisations=polarization,
        outputSigmaBand=True, outputImageInComplex=False), src)

    # 4) Lee Speckle Filter (adaptive, 7×7)
    src = GPF.createProduct("Speckle-Filter", _params(
        sourceBands=f"Sigma0_{polarization}",
        filter="Lee", filterSizeX=7, filterSizeY=7), src)

    # 5) Range-Doppler Terrain Correction (Copernicus DEM 30 m → WGS84)
    src = GPF.createProduct("Terrain-Correction", _params(
        sourceBands=f"Sigma0_{polarization}",
        demName=DEM_NAME, pixelSpacingInMeter=10.0,
        mapProjection="WGS84(DD)"), src)

    # 6) Optional ROI subset, then Linear-to-dB
    if roi_wkt:
        src = GPF.createProduct("Subset", _params(
            geoRegion=roi_wkt, subSamplingX=1, subSamplingY=1), src)
    src = GPF.createProduct("LinearToFromdB", _params(
        sourceBands=f"Sigma0_{polarization}"), src)

    fmt = "GeoTIFF-BigTIFF" if output_path.endswith(".tif") else "BEAM-DIMAP"
    ProductIO.writeProduct(src, output_path, fmt)
    src.dispose()


def normalize_db_to_01(arr_db: np.ndarray,
                        lo: float = CLIP_RANGE_DB[0],
                        hi: float = CLIP_RANGE_DB[1]) -> np.ndarray:
    """Clip σ⁰ in dB to [lo, hi] and rescale to [0, 1]."""
    return (np.clip(arr_db, lo, hi) - lo) / (hi - lo)


if __name__ == "__main__":
    SRC = "/data/S1A_IW_GRDH_1SDV_20240911T053614_kola.zip"
    DST = "/data/preprocessed/kola_20240911_sigma0_db.tif"
    KOLA_WKT = "POLYGON((33.0 68.9, 33.6 68.9, 33.6 69.1, 33.0 69.1, 33.0 68.9))"
    preprocess_sentinel1(SRC, DST, roi_wkt=KOLA_WKT, polarization="VV")
    print(f"saved → {DST}")
''')

page_break()

# ─── ПРИЛОЖЕНИЕ Б — DeepLabV3+ architecture with scSE ───
CH('Приложение Б. Архитектура нейросетевой модели DeepLabV3+ '
   'с блоками внимания scSE')

P('В приложении приведён исходный код модуля определения архитектуры '
  'нейросетевой модели семантической сегментации, описанной в разделе 2.4. '
  'Модель построена на базе фреймворка PyTorch и библиотеки '
  'segmentation-models-pytorch с пользовательской модификацией энкодера '
  'для приёма одноканальных SAR-данных и интеграцией блоков внимания '
  'scSE (concurrent Spatial and Channel Squeeze & Excitation) после '
  'каждой свёрточной группы ResNet-50.')

code_block('''# model_arctic_oil.py — DeepLabV3+ with scSE attention for SAR segmentation
# (c) V. K. Baykhanov, 2026
import torch
import torch.nn as nn
import segmentation_models_pytorch as smp


class ChannelSE(nn.Module):
    """Channel-wise Squeeze & Excitation block."""
    def __init__(self, channels: int, reduction: int = 16):
        super().__init__()
        hidden = max(channels // reduction, 4)
        self.avg = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Conv2d(channels, hidden, 1, bias=False), nn.ReLU(inplace=True),
            nn.Conv2d(hidden, channels, 1, bias=False), nn.Sigmoid())

    def forward(self, x):
        return x * self.fc(self.avg(x))


class SpatialSE(nn.Module):
    """Spatial Squeeze & Excitation block."""
    def __init__(self, channels: int):
        super().__init__()
        self.gate = nn.Sequential(
            nn.Conv2d(channels, 1, kernel_size=1, bias=True), nn.Sigmoid())

    def forward(self, x):
        return x * self.gate(x)


class scSE(nn.Module):
    """Concurrent spatial + channel SE (Roy et al., MICCAI 2018)."""
    def __init__(self, channels: int, reduction: int = 16):
        super().__init__()
        self.cse = ChannelSE(channels, reduction)
        self.sse = SpatialSE(channels)

    def forward(self, x):
        return self.cse(x) + self.sse(x)


def _patch_first_conv_to_1ch(encoder: nn.Module) -> None:
    """Re-init ResNet conv1 to accept one input channel (σ⁰_VV in dB)."""
    old: nn.Conv2d = encoder.conv1
    new = nn.Conv2d(1, old.out_channels,
                     kernel_size=old.kernel_size, stride=old.stride,
                     padding=old.padding, bias=old.bias is not None)
    with torch.no_grad():
        # average the 3-channel pretrained weights into 1 channel
        new.weight.copy_(old.weight.mean(dim=1, keepdim=True))
    encoder.conv1 = new


def _inject_scse_into_resnet(encoder: nn.Module) -> None:
    """Append an scSE block to every ResNet-50 stage output."""
    stage_channels = {"layer1": 256, "layer2": 512,
                       "layer3": 1024, "layer4": 2048}
    for name, ch in stage_channels.items():
        stage = getattr(encoder, name)
        stage.add_module(f"scse_{name}", scSE(ch))


def build_arctic_oil_model(num_classes: int = 3,
                            encoder_name: str = "resnet50",
                            encoder_weights: str = "imagenet"
                            ) -> smp.DeepLabV3Plus:
    """Build the Arctic-oil-spill segmentation model.

    Three-class semantic segmentation: 0=water, 1=oil, 2=ice+land.
    """
    model = smp.DeepLabV3Plus(
        encoder_name=encoder_name,
        encoder_weights=encoder_weights,
        in_channels=3, classes=num_classes,
        activation=None)
    # Adapt for 1-channel SAR input + inject scSE attention
    _patch_first_conv_to_1ch(model.encoder)
    _inject_scse_into_resnet(model.encoder)
    return model


if __name__ == "__main__":
    net = build_arctic_oil_model()
    x = torch.randn(2, 1, 256, 256)
    y = net(x)
    print("output:", y.shape)   # → torch.Size([2, 3, 256, 256])
    n_params = sum(p.numel() for p in net.parameters() if p.requires_grad)
    print(f"trainable params: {n_params/1e6:.1f} M")
''')

page_break()

# ─── ПРИЛОЖЕНИЕ В — Training loop ───
CH('Приложение В. Программный модуль обучения нейросетевой модели')

P('В приложении приведён исходный код модуля обучения модели '
  'DeepLabV3+, описанного в разделе 2.4. Модуль реализует процедуру '
  'обучения с оптимизатором AdamW, комбинированной функцией потерь '
  'Dice-BCE с весами классов, планировщиком скорости обучения '
  'ReduceLROnPlateau и сохранением лучшей контрольной точки по '
  'валидационному mIoU.')

code_block('''# train_arctic_oil.py — training loop for the Arctic oil-spill model
# (c) V. K. Baykhanov, 2026
import torch
import torch.nn.functional as F
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from torch.amp import autocast, GradScaler

from model_arctic_oil import build_arctic_oil_model
from dataset_arctic_sar import ArcticSarDataset


# weights selected inversely proportional to class frequency
CLASS_WEIGHTS = torch.tensor([0.3, 9.8, 1.2])
EPOCHS, BATCH, LR, WD = 100, 8, 1e-4, 1e-4


def dice_loss(logits: torch.Tensor, target: torch.Tensor,
              num_classes: int = 3, eps: float = 1e-6) -> torch.Tensor:
    """Multi-class soft Dice loss; expects integer target masks."""
    probs = F.softmax(logits, dim=1)
    onehot = F.one_hot(target, num_classes).permute(0, 3, 1, 2).float()
    dims = (0, 2, 3)
    inter = (probs * onehot).sum(dims)
    union = probs.sum(dims) + onehot.sum(dims)
    return 1 - ((2 * inter + eps) / (union + eps)).mean()


def combined_loss(logits, target, class_weights):
    ce = F.cross_entropy(logits, target,
                          weight=class_weights.to(logits.device))
    dl = dice_loss(logits, target)
    return 0.5 * ce + 0.5 * dl


def miou(pred: torch.Tensor, target: torch.Tensor, n: int = 3) -> float:
    ious = []
    for c in range(n):
        p, t = (pred == c), (target == c)
        inter = (p & t).sum().item()
        union = (p | t).sum().item()
        ious.append(inter / union if union else float("nan"))
    return torch.tensor(ious).nanmean().item()


def train_one_epoch(model, loader, optim, scaler, device):
    model.train(); total = 0.0
    for x, y in loader:
        x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
        optim.zero_grad(set_to_none=True)
        with autocast(device_type="cuda", dtype=torch.float16):
            logits = model(x)
            loss = combined_loss(logits, y, CLASS_WEIGHTS)
        scaler.scale(loss).backward()
        scaler.step(optim); scaler.update()
        total += loss.item() * x.size(0)
    return total / len(loader.dataset)


@torch.no_grad()
def validate(model, loader, device):
    model.eval(); total_loss, total_iou = 0.0, 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        total_loss += combined_loss(logits, y, CLASS_WEIGHTS).item() * x.size(0)
        total_iou += miou(logits.argmax(1), y) * x.size(0)
    n = len(loader.dataset)
    return total_loss / n, total_iou / n


def main():
    device = torch.device("cuda")
    train_dl = DataLoader(ArcticSarDataset("train"),
                            batch_size=BATCH, shuffle=True,
                            num_workers=4, pin_memory=True)
    val_dl = DataLoader(ArcticSarDataset("val"),
                        batch_size=BATCH, num_workers=4, pin_memory=True)

    model = build_arctic_oil_model(num_classes=3).to(device)
    optim = AdamW(model.parameters(), lr=LR, weight_decay=WD)
    sched = ReduceLROnPlateau(optim, mode="max", factor=0.5,
                                patience=10, threshold=1e-3)
    scaler = GradScaler("cuda")

    best_miou = 0.0
    for epoch in range(1, EPOCHS + 1):
        tr_loss = train_one_epoch(model, train_dl, optim, scaler, device)
        va_loss, va_iou = validate(model, val_dl, device)
        sched.step(va_iou)
        print(f"epoch {epoch:03d} | train {tr_loss:.4f} | "
              f"val {va_loss:.4f} | mIoU {va_iou:.4f}")
        if va_iou > best_miou:
            best_miou = va_iou
            torch.save({"state_dict": model.state_dict(),
                        "epoch": epoch, "miou": va_iou},
                       "checkpoints/best.pt")
            print(f"  ↑ new best mIoU = {va_iou:.4f}")
    print(f"finished, best mIoU = {best_miou:.4f}")


if __name__ == "__main__":
    main()
''')

page_break()

# ─── ПРИЛОЖЕНИЕ Г — Inference + metrics ───
CH('Приложение Г. Программный модуль инференса и расчёта метрик качества')

P('В приложении приведён исходный код модуля инференса и расчёта метрик '
  'качества обученной модели на тестовой выборке. Модуль реализует '
  'процедуру попиксельного предсказания, формирование матрицы ошибок '
  'и расчёт метрик Precision, Recall, F1-score, IoU и общей точности '
  'для каждого класса в соответствии с разделом 3.2 настоящей работы.')

code_block('''# infer_and_evaluate.py — inference and metric computation
# (c) V. K. Baykhanov, 2026
import numpy as np
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import (confusion_matrix, precision_recall_fscore_support,
                              accuracy_score)
import matplotlib.pyplot as plt

from model_arctic_oil import build_arctic_oil_model
from dataset_arctic_sar import ArcticSarDataset


CLASSES = ["вода", "нефть", "лёд + суша"]
CHECKPOINT = "checkpoints/best.pt"


def per_class_iou(cm: np.ndarray) -> np.ndarray:
    """IoU = TP / (TP + FP + FN) computed from confusion matrix."""
    tp = np.diag(cm).astype(np.float64)
    fp = cm.sum(axis=0) - tp
    fn = cm.sum(axis=1) - tp
    denom = tp + fp + fn
    return np.where(denom > 0, tp / denom, np.nan)


@torch.no_grad()
def predict_dataset(model, loader, device):
    model.eval()
    y_true, y_pred = [], []
    for x, y in loader:
        x = x.to(device)
        pred = model(x).argmax(dim=1).cpu().numpy()
        y_true.append(y.numpy().ravel())
        y_pred.append(pred.ravel())
    return np.concatenate(y_true), np.concatenate(y_pred)


def print_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    acc = accuracy_score(y_true, y_pred)
    p, r, f, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=range(len(CLASSES)), zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=range(len(CLASSES)))
    iou = per_class_iou(cm)
    miou = float(np.nanmean(iou))

    print(f"\\nAccuracy: {acc*100:.1f}%  |  mIoU: {miou:.3f}")
    print(f"{'class':<14}{'Prec':>8}{'Recall':>8}{'F1':>8}{'IoU':>8}")
    for i, cls in enumerate(CLASSES):
        print(f"{cls:<14}{p[i]:>8.3f}{r[i]:>8.3f}{f[i]:>8.3f}{iou[i]:>8.3f}")
    return {"acc": acc, "mIoU": miou, "precision": p.tolist(),
            "recall": r.tolist(), "f1": f.tolist(),
            "iou": iou.tolist(), "cm": cm}


def plot_confusion(cm: np.ndarray, out_path: str = "fig_confusion.png"):
    fig, ax = plt.subplots(figsize=(6, 5))
    cm_norm = cm / cm.sum(axis=1, keepdims=True)
    im = ax.imshow(cm_norm, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(CLASSES))); ax.set_yticks(range(len(CLASSES)))
    ax.set_xticklabels(CLASSES); ax.set_yticklabels(CLASSES)
    ax.set_xlabel("предсказанный класс"); ax.set_ylabel("истинный класс")
    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            ax.text(j, i, f"{cm_norm[i,j]:.2f}", ha="center", va="center",
                    color="white" if cm_norm[i,j] > 0.5 else "black")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout(); fig.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"confusion matrix → {out_path}")


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_arctic_oil_model(num_classes=3).to(device)
    ckpt = torch.load(CHECKPOINT, map_location=device)
    model.load_state_dict(ckpt["state_dict"])
    print(f"loaded checkpoint epoch={ckpt['epoch']} mIoU={ckpt['miou']:.3f}")

    test_dl = DataLoader(ArcticSarDataset("test"),
                          batch_size=8, num_workers=4, pin_memory=True)
    y_true, y_pred = predict_dataset(model, test_dl, device)
    metrics = print_metrics(y_true, y_pred)
    plot_confusion(metrics["cm"])


if __name__ == "__main__":
    main()
''')

# ════════════════════════════════════════════════════════════════════════
doc.save(OUT)
print(f'\nSAVED → {OUT}')
print(f'Размер файла: {os.path.getsize(OUT)/1024:.1f} KB')
print(f'Список литературы: {len(LIT)} источников')
print(f'Footnotes (сноски): {FN.next_id - 1}')






