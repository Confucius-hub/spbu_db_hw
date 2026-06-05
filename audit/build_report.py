#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пересборка отчёта проверки членов СРО по ИСПРАВЛЕННОЙ методике.

Что чинит этот скрипт (по фидбэку):
  2) Статус НОСТРОЙ берётся пер-компанийно из собранных данных
     (действителен / приостановлен / исключён), а не "действителен" для всех.
  3) Судебные дела: учитываются ТОЛЬКО дела категории «...подряда»
     (категория содержит слово "подряд"), и только потом фильтр на 2025+.
     Источник — Rusprofile (там категория прописана явно).
  4) Описание спора = номер дела + сумма иска + роль компании
     (истец / ответчик / третье лицо), без «хаотичного» текста.
  5) Ссылка ведёт на конкретную карточку дела (kad.arbitr.ru/Card/...),
     а не на главную сайта.

Вход:
  audit/companies.csv          — выверенная база (имя, ИНН, вид, контракты, сумма, штрафы)
  audit/collected_data.json    — данные, собранные браузерным расширением (по ИНН)
  audit/source/audit_report_FINAL_1.xlsx — для переноса листа «По видам закупок» как есть

Выход:
  audit/audit_report_corrected.xlsx
"""

import csv
import json
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = os.path.dirname(os.path.abspath(__file__))
COMPANIES_CSV = os.path.join(BASE, "companies.csv")
COLLECTED_JSON = os.path.join(BASE, "collected_data.json")
SOURCE_XLSX = os.path.join(BASE, "source", "audit_report_FINAL_1.xlsx")
OUT_XLSX = os.path.join(BASE, "audit_report_corrected.xlsx")

# ---- Параметры оценки риска (можно править) -------------------------------
# Граница «крупных» штрафов: >= этой суммы трактуется как существенные
# штрафы/неустойки (признак Высокого риска); меньше — «небольшие» (Средний).
BIG_FINE = 1_000_000
# --------------------------------------------------------------------------

PENDING = "⏳ ожидает данных"   # маркер: веб-проверка ещё не проведена


# ============================ Загрузка входных данных ======================

def load_companies():
    rows = []
    with open(COMPANIES_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["contracts"] = int(float(r["contracts"])) if r["contracts"] else 0
            r["contract_sum"] = float(r["contract_sum"]) if r["contract_sum"] else 0.0
            r["fines"] = float(r["fines"]) if r["fines"] else 0.0
            rows.append(r)
    return rows


def load_collected():
    """Данные расширения, ключ — ИНН (строка). Если файла нет — пустой словарь."""
    if not os.path.exists(COLLECTED_JSON):
        return {}
    with open(COLLECTED_JSON, encoding="utf-8") as f:
        data = json.load(f)
    # допускаем как dict{inn:...}, так и list[{inn:...}]
    if isinstance(data, list):
        data = {str(item["inn"]): item for item in data}
    return {str(k): v for k, v in data.items()}


# ============================ Оценка риска =================================

def assess_risk(c, collected):
    """Возвращает (уровень, основание, флаг_проверено)."""
    info = collected.get(c["inn"])
    fines = c["fines"] or 0

    if not info or not info.get("checked"):
        # Веб-проверка ещё не проведена — оценить нельзя
        reasons = []
        if fines >= BIG_FINE:
            reasons.append(f"крупные штрафы/неустойки {fines:,.0f} ₽".replace(",", " "))
        elif fines > 0:
            reasons.append(f"небольшие штрафы/неустойки {fines:,.0f} ₽".replace(",", " "))
        base = "; ".join(reasons) if reasons else ""
        return (PENDING, base, False)

    nostroy = (info.get("nostroy") or {})
    status = (nostroy.get("status") or "").strip().lower()
    odo = (nostroy.get("odo_level") or "").strip().lower()
    cases = info.get("podryad_cases_2025plus") or []
    n_cases = len(cases)

    high, med = [], []

    if "приостан" in status:
        high.append("статус НОСТРОЙ: приостановлен")
    if "исключ" in status or "прекращ" in status:
        high.append(f"статус НОСТРОЙ: {nostroy.get('status')}")
    if odo in ("не установлен", "не установлено", "отсутствует", "нет"):
        high.append("уровень ответственности (ОДО) не установлен")
    if n_cases >= 1:
        high.append(f"арбитражные дела по подряду 2025+ ({n_cases})")
    if fines >= BIG_FINE:
        high.append(f"штрафы/неустойки {fines:,.0f} ₽".replace(",", " "))
    elif fines > 0:
        med.append(f"небольшие штрафы/неустойки {fines:,.0f} ₽".replace(",", " "))

    if status in ("не найден", "не найдена", "нет данных", ""):
        med.append("статус НОСТРОЙ не подтверждён (спорные данные)")

    if high:
        return ("Высокий", "; ".join(high), True)
    if med:
        return ("Средний", "; ".join(med), True)
    return ("Низкий", "НОСТРОЙ действителен; дел по подряду 2025+ нет; штрафов нет", True)


# ============================ Формирование строк ===========================

def case_brief(case):
    """Короткая строка по делу для столбца «описание»: № — сумма — роль."""
    num = case.get("case_number", "?")
    amt = case.get("claim_amount")
    role = case.get("our_role", "")
    amt_s = f"{float(amt):,.0f} ₽".replace(",", " ") if amt not in (None, "", "—") else "сумма н/д"
    parts = [num, amt_s]
    if role:
        parts.append(role)
    return " — ".join(parts)


def build_rows(companies, collected):
    out = []
    for c in companies:
        info = collected.get(c["inn"]) or {}
        checked = bool(info.get("checked"))
        nostroy = info.get("nostroy") or {}
        cases = info.get("podryad_cases_2025plus") or []

        if checked:
            status_str = nostroy.get("status") or "не найден"
            odo_str = nostroy.get("odo_level") or "не установлен"
            has_cases = "Да" if cases else "Нет"
            n_cases = len(cases)
            descr = "; ".join(case_brief(x) for x in cases) if cases else "—"
        else:
            status_str = PENDING
            odo_str = PENDING
            has_cases = PENDING
            n_cases = ""
            descr = PENDING

        risk, basis, _ = assess_risk(c, collected)

        out.append({
            "name": c["name"], "inn": c["inn"], "vid": c["vid_zakupki"],
            "contracts": c["contracts"], "contract_sum": c["contract_sum"],
            "nostroy_status": status_str, "odo": odo_str,
            "has_cases": has_cases, "n_cases": n_cases, "descr": descr,
            "fines": c["fines"], "risk": risk, "basis": basis,
            "cases": cases,
        })
    return out


# ============================ Стили / запись Excel =========================

THIN = Side(style="thin", color="D0D0D0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD_FILL = PatternFill("solid", fgColor="1F4E78")
HEAD_FONT = Font(bold=True, color="FFFFFF", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
RISK_FILL = {
    "Высокий": PatternFill("solid", fgColor="F4CCCC"),
    "Средний": PatternFill("solid", fgColor="FFF2CC"),
    "Низкий":  PatternFill("solid", fgColor="D9EAD3"),
}


def style_header(ws, row, ncols):
    for col in range(1, ncols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = BORDER


def write_final_sheet(wb, rows, meta):
    ws = wb.create_sheet("Итоговый отчёт", 0)
    ws.append([meta])
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=13)
    ws.cell(1, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(1, 1).font = Font(italic=True, size=9)
    ws.row_dimensions[1].height = 95

    headers = ["Наименование компании", "ИНН", "Вид закупки", "Количество контрактов",
               "Общая сумма контрактов, ₽", "Статус права в реестре НОСТРОЙ",
               "Уровень ответственности (ОДО)", "Судебные дела по подряду 2025+ (Да/Нет)",
               "Количество судебных дел", "Краткое описание судебных споров (№ дела — сумма иска — роль)",
               "Сумма штрафов/неустоек, ₽", "Общая оценка риска", "Основание оценки"]
    ws.append(headers)
    style_header(ws, 2, len(headers))

    for r in rows:
        ws.append([r["name"], r["inn"], r["vid"], r["contracts"], r["contract_sum"],
                   r["nostroy_status"], r["odo"], r["has_cases"], r["n_cases"],
                   r["descr"], r["fines"], r["risk"], r["basis"]])
        rr = ws.max_row
        for col in range(1, 14):
            ws.cell(rr, col).border = BORDER
            ws.cell(rr, col).alignment = WRAP
        ws.cell(rr, 5).number_format = '# ##0.00'
        ws.cell(rr, 11).number_format = '# ##0.00'
        if r["risk"] in RISK_FILL:
            ws.cell(rr, 12).fill = RISK_FILL[r["risk"]]
            ws.cell(rr, 12).font = Font(bold=True)

    widths = [26, 13, 14, 11, 18, 16, 16, 14, 12, 46, 16, 12, 34]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A3"
    return ws


def write_cases_sheet(wb, rows):
    ws = wb.create_sheet("Судебные дела (подряд) 2025+")
    headers = ["Компания", "ИНН", "Номер дела", "Дата регистрации", "Категория спора",
               "Истец", "Ответчик", "Третье / иное лицо", "Роль проверяемой компании",
               "Сумма иска, ₽", "Исход", "Текущий статус", "Ссылка на карточку дела (КАД)"]
    ws.append(headers)
    style_header(ws, 1, len(headers))

    any_case = False
    for r in rows:
        for case in r["cases"]:
            any_case = True
            ws.append([
                r["name"], r["inn"], case.get("case_number", ""),
                case.get("reg_date", ""), case.get("category", ""),
                case.get("plaintiff", ""), case.get("defendants", ""),
                case.get("other_party", ""), case.get("our_role", ""),
                case.get("claim_amount", ""), case.get("outcome", ""),
                case.get("status", ""), case.get("kad_url", ""),
            ])
            rr = ws.max_row
            for col in range(1, 14):
                ws.cell(rr, col).border = BORDER
                ws.cell(rr, col).alignment = WRAP
            if isinstance(case.get("claim_amount"), (int, float)):
                ws.cell(rr, 10).number_format = '# ##0.00'

    if not any_case:
        ws.append(["⏳ Данные по делам ещё не собраны браузерным расширением — "
                   "будут заполнены после прогона по Rusprofile.", "", "", "", "", "", "", "", "", "", "", "", ""])
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=13)

    widths = [22, 13, 18, 14, 34, 24, 24, 22, 16, 16, 18, 16, 30]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    return ws


def write_risk_sheet(wb, rows):
    ws = wb.create_sheet("Сводка рисков")
    headers = ["Уровень риска", "Компания", "ИНН", "Статус НОСТРОЙ", "ОДО",
               "Дел по подряду 2025+", "Штрафы, ₽", "Основание"]
    ws.append(headers)
    style_header(ws, 1, len(headers))

    order = {"Высокий": 0, "Средний": 1, "Низкий": 2, PENDING: 3}
    for r in sorted(rows, key=lambda x: (order.get(x["risk"], 9), -(x["n_cases"] or 0))):
        ws.append([r["risk"], r["name"], r["inn"], r["nostroy_status"], r["odo"],
                   r["n_cases"], r["fines"], r["basis"]])
        rr = ws.max_row
        for col in range(1, 9):
            ws.cell(rr, col).border = BORDER
            ws.cell(rr, col).alignment = WRAP
        ws.cell(rr, 7).number_format = '# ##0.00'
        if r["risk"] in RISK_FILL:
            ws.cell(rr, 1).fill = RISK_FILL[r["risk"]]
            ws.cell(rr, 1).font = Font(bold=True)

    widths = [14, 24, 13, 16, 16, 12, 16, 40]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    return ws


def copy_vidy_sheet(wb):
    """Лист «По видам закупок» переносим как есть — цифры выверены."""
    if not os.path.exists(SOURCE_XLSX):
        return
    src = load_workbook(SOURCE_XLSX, data_only=True)
    if "По видам закупок" not in src.sheetnames:
        return
    s = src["По видам закупок"]
    ws = wb.create_sheet("По видам закупок")
    for row in s.iter_rows(values_only=True):
        ws.append(row)
    style_header(ws, 1, s.max_column)
    for col in range(1, s.max_column + 1):
        for rr in range(2, ws.max_row + 1):
            ws.cell(rr, col).border = BORDER
        ws.cell(ws.max_row, col)
    for i, w in enumerate([14, 30, 14, 12, 20], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


# ============================ main ========================================

def main():
    companies = load_companies()
    collected = load_collected()
    rows = build_rows(companies, collected)

    checked = sum(1 for c in companies if collected.get(c["inn"], {}).get("checked"))
    dist = {}
    for r in rows:
        dist[r["risk"]] = dist.get(r["risk"], 0) + 1
    n_susp = sum(1 for r in rows if "приостан" in r["nostroy_status"].lower())
    n_noodo = sum(1 for r in rows if r["odo"] == "не установлен")
    n_cases_companies = sum(1 for r in rows if r["cases"])

    meta = (
        f"Проверка членов СРО (исправленная методика). Компаний: {len(companies)}. "
        f"Веб-проверка пройдена: {checked}/{len(companies)}. "
        f"Фильтр контрактов: дата окончания ≥ 01.01.2023 (цифры из выверенной выгрузки ЦИСК). "
        f"НОСТРОЙ (reestr.nostroy.ru): статус права + уровень ОДО; приостановлено: {n_susp}, ОДО не установлен: {n_noodo}. "
        f"Суды (Rusprofile → kad.arbitr.ru): берутся ТОЛЬКО дела категории «…по договорам подряда», затем дата ≥ 01.01.2025. "
        f"Описание спора = № дела + сумма иска + роль (истец/ответчик/третье лицо). "
        f"С делами по подряду 2025+: {n_cases_companies}. "
        f"Риск — Высокий: {dist.get('Высокий',0)}, Средний: {dist.get('Средний',0)}, "
        f"Низкий: {dist.get('Низкий',0)}, Ожидает: {dist.get(PENDING,0)}."
    )

    wb = Workbook()
    wb.remove(wb.active)
    write_final_sheet(wb, rows, meta)
    copy_vidy_sheet(wb)
    write_cases_sheet(wb, rows)
    write_risk_sheet(wb, rows)
    wb.save(OUT_XLSX)

    print(f"✓ Сохранено: {OUT_XLSX}")
    print(f"  Компаний: {len(companies)} | проверено вебом: {checked}")
    print(f"  Риск: {dist}")
    print(f"  Приостановлено НОСТРОЙ: {n_susp} | ОДО не установлен: {n_noodo} | с делами по подряду: {n_cases_companies}")


if __name__ == "__main__":
    main()
