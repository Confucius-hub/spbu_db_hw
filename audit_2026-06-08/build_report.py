#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пересборка отчёта проверки членов СРО по ИСПРАВЛЕННОЙ методике.

Что чинит этот скрипт (по фидбэку):
  2) Статус НОСТРОЙ берётся пер-компанийно из собранных данных
     (действителен / приостановлен / исключён), а не "действителен" для всех.
  3) Судебные дела: учитываются ТОЛЬКО дела категории «...подряда»
     (категория/предмет содержит слово "подряд"), и только потом фильтр на 2025+.
  4) Описание спора = номер дела + сумма иска + роль компании
     (истец / ответчик / третье лицо), без «хаотичного» текста.
  5) Ссылка ведёт на конкретную карточку дела (kad.arbitr.ru/Card/...),
     а не на главную сайта.

Модель «проверено» — РАЗДЕЛЬНАЯ, чтобы не выдавать ложный «0 дел»:
  • nostroy_checked — статус/ОДО в НОСТРОЙ подтверждены;
  • cases_checked   — дела действительно перечислены по полному источнику
                      (kad.arbitr.ru или платный Rusprofile). Если источник
                      показал не все дела (пейволл) — cases_checked=false,
                      и в отчёте стоит «не проверено», а не «нет дел».

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

PENDING = "⏳ ожидает данных"        # НОСТРОЙ ещё не проверен
CASES_PENDING = "⏳ не проверено (kad)"  # дела ещё не собраны по полному источнику
NO_STATUS = {"не установлен", "не установлено", "отсутствует", "нет", "—", ""}
NOT_FOUND = {"не найден", "не найдена", "нет данных", ""}


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
    """Данные расширения, ключ — ИНН (строка). Нормализуем флаги проверки."""
    if not os.path.exists(COLLECTED_JSON):
        return {}
    with open(COLLECTED_JSON, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        data = {str(item["inn"]): item for item in data}
    out = {}
    for k, v in data.items():
        if k.startswith("_") or not isinstance(v, dict):
            continue  # служебные ключи вроде "_comment"
        # обратная совместимость: старый общий флаг "checked"
        if "checked" in v and "nostroy_checked" not in v:
            v["nostroy_checked"] = bool(v["checked"])
            v["cases_checked"] = bool(v["checked"])
        v.setdefault("nostroy_checked", False)
        v.setdefault("cases_checked", False)
        out[str(k)] = v
    return out


# ============================ Оценка риска =================================

def assess_risk(c, info):
    """Возвращает (уровень, основание). Учитывает раздельные флаги проверки."""
    fines = c["fines"] or 0
    nostroy_checked = bool(info.get("nostroy_checked"))
    cases_checked = bool(info.get("cases_checked"))
    nostroy = info.get("nostroy") or {}
    found = nostroy.get("found", True)
    status = (nostroy.get("status") or "").strip().lower()
    odo = (nostroy.get("odo_level") or "").strip().lower()
    n_cases = len(info.get("podryad_cases_2025plus") or [])

    high, med, pending = [], [], []

    # --- НОСТРОЙ ---
    if nostroy_checked:
        if "приостан" in status:
            high.append("статус НОСТРОЙ приостановлен")
        elif "исключ" in status or "прекращ" in status:
            high.append(f"статус НОСТРОЙ: {nostroy.get('status')}")
        elif (not found) or status in NOT_FOUND:
            med.append("не найден в НОСТРОЙ (спорные данные)")
        if found and odo in NO_STATUS:
            high.append("уровень ответственности (ОДО) не установлен")
    else:
        pending.append("НОСТРОЙ не проверен")

    # --- Суды ---
    if cases_checked:
        if n_cases >= 1:
            high.append(f"арбитражные дела по подряду 2025+ ({n_cases})")
    else:
        pending.append("дела по подряду не проверены")

    # --- Штрафы ---
    if fines >= BIG_FINE:
        high.append(f"крупные штрафы/неустойки {fines:,.0f} ₽".replace(",", " "))
    elif fines > 0:
        med.append(f"небольшие штрафы/неустойки {fines:,.0f} ₽".replace(",", " "))

    # --- Итог ---
    if high:
        return ("Высокий", "; ".join(high))
    if pending:
        # нельзя финализировать «Низкий», пока не проверено то, что может поднять риск
        base = "ожидается проверка: " + ", ".join(pending)
        if med:
            base += "; " + "; ".join(med)
        return (PENDING, base)
    if med:
        return ("Средний", "; ".join(med))
    return ("Низкий", "НОСТРОЙ действителен; дел по подряду 2025+ нет; штрафов нет")


# ============================ Формирование строк ===========================

def case_brief(case):
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
        nostroy_checked = bool(info.get("nostroy_checked"))
        cases_checked = bool(info.get("cases_checked"))
        nostroy = info.get("nostroy") or {}
        cases = info.get("podryad_cases_2025plus") or []

        if nostroy_checked:
            status_str = nostroy.get("status") or "не найден"
            odo_str = nostroy.get("odo_level") or "не установлен"
        else:
            status_str = PENDING
            odo_str = PENDING

        if cases_checked:
            has_cases = "Да" if cases else "Нет"
            n_cases = len(cases)
            descr = "; ".join(case_brief(x) for x in cases) if cases else "—"
        else:
            has_cases = CASES_PENDING
            n_cases = ""
            descr = CASES_PENDING

        risk, basis = assess_risk(c, info)

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
        ws.append(["⏳ Дела по подряду ещё не собраны по полному источнику (kad.arbitr.ru). "
                   "Rusprofile показывает категории дел только по платной подписке.",
                   "", "", "", "", "", "", "", "", "", "", "", ""])
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

    widths = [16, 24, 13, 16, 16, 12, 16, 40]
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
    for i, w in enumerate([14, 30, 14, 12, 20], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


# ============================ main ========================================

def main():
    companies = load_companies()
    collected = load_collected()
    rows = build_rows(companies, collected)

    n_nostroy = sum(1 for c in companies if collected.get(c["inn"], {}).get("nostroy_checked"))
    n_cases_chk = sum(1 for c in companies if collected.get(c["inn"], {}).get("cases_checked"))
    dist = {}
    for r in rows:
        dist[r["risk"]] = dist.get(r["risk"], 0) + 1
    n_susp = sum(1 for r in rows if "приостан" in str(r["nostroy_status"]).lower())
    n_noodo = sum(1 for r in rows if r["odo"] == "не установлен")
    n_cases_companies = sum(1 for r in rows if r["cases"])

    meta = (
        f"Проверка членов СРО (исправленная методика). Компаний: {len(companies)}. "
        f"НОСТРОЙ проверено: {n_nostroy}/{len(companies)}; дела проверены: {n_cases_chk}/{len(companies)}. "
        f"Фильтр контрактов: дата окончания ≥ 01.01.2023 (цифры из выверенной выгрузки ЦИСК). "
        f"НОСТРОЙ (reestr.nostroy.ru): статус права + уровень КФ ОДО (обеспечение договорных обязательств, "
        f"не путать с КФ ВВ); приостановлено: {n_susp}, ОДО не установлен: {n_noodo}. "
        f"Суды: берутся ТОЛЬКО дела категории «…по договорам подряда», затем дата ≥ 01.01.2025. "
        f"Описание = № дела + сумма иска + роль (истец/ответчик/третье лицо). "
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
    print(f"  Компаний: {len(companies)} | НОСТРОЙ проверено: {n_nostroy} | дела проверены: {n_cases_chk}")
    print(f"  Риск: {dist}")
    print(f"  Приостановлено: {n_susp} | ОДО не установлен: {n_noodo} | с делами по подряду: {n_cases_companies}")


if __name__ == "__main__":
    main()
