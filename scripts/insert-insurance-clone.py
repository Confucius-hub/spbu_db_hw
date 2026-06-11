#!/usr/bin/env python3
"""Вставляет блок «Страхование по уровням 1–5» в локальный клон старого сайта СССС.

Использование (на Mac пользователя):
    python3 scripts/insert-insurance-clone.py [путь_к_index.html]

По умолчанию путь: ~/Downloads/sro-ssss-clone/sro-ssss.ru/new_main/index.html
Делает резервную копию index.html.bak. Повторный запуск ничего не дублирует.
Суммы — из референса пользователя (sro-ism.ru → Страхование); правятся в BLOCK ниже.
"""

import re
import shutil
import sys
from pathlib import Path

DEFAULT = Path.home() / "Downloads/sro-ssss-clone/sro-ssss.ru/new_main/index.html"
INDEX = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT

ROWS = [
    ("Первый уровень ответственности", "4&nbsp;000&nbsp;000,00&nbsp;₽"),
    ("Второй уровень ответственности", "15&nbsp;000&nbsp;000,00&nbsp;₽"),
    ("Третий уровень ответственности", "100&nbsp;000&nbsp;000,00&nbsp;₽"),
    ("Четвёртый уровень ответственности", "200&nbsp;000&nbsp;000,00&nbsp;₽"),
    ("Пятый уровень ответственности", "200&nbsp;000&nbsp;000,00&nbsp;₽"),
]

TD = 'style="border:1px solid #d9d9d9;padding:8px 14px;"'
TDR = 'style="border:1px solid #d9d9d9;padding:8px 14px;text-align:right;"'
ROWS_HTML = "\n".join(
    f"      <tr><td {TD}>{name}</td><td {TDR}>{total}</td></tr>" for name, total in ROWS
)

BLOCK = f"""
<!-- === Страхование: градация по уровням (вставлено скриптом) === -->
<section id="strahovanie-block" style="max-width:1100px;margin:40px auto;padding:0 16px;font-family:inherit;">
  <h2 style="color:#3e7595;font-weight:600;margin:0 0 6px;">Страхование ответственности членов Ассоциации</h2>
  <p style="color:#444;margin:0 0 18px;">
    Минимальный размер страховой суммы по договору страхования гражданской ответственности (ВВ)
    зависит от уровня ответственности члена Ассоциации (ст. 55.16 ГрК РФ):
  </p>
  <table style="border-collapse:collapse;width:100%;max-width:760px;font-size:15px;">
    <thead>
      <tr style="background:#f2f6f8;">
        <th style="border:1px solid #d9d9d9;padding:9px 14px;text-align:left;color:#3e7595;">Уровень ответственности члена Ассоциации</th>
        <th style="border:1px solid #d9d9d9;padding:9px 14px;text-align:right;color:#3e7595;">Размер страховой суммы, не&nbsp;менее</th>
      </tr>
    </thead>
    <tbody>
{ROWS_HTML}
    </tbody>
  </table>
  <p style="color:#444;margin:16px 0 0;max-width:760px;">
    По договорам подряда, заключённым конкурентными способами (ОДО), член Ассоциации обеспечивает
    действующий договор комбинированного страхования риска ответственности по каждому такому договору.
    Полные требования и перечень страховых организаций — по запросу.
  </p>
</section>
"""


def main() -> None:
    if not INDEX.exists():
        sys.exit(f"✗ Файл не найден: {INDEX}\n  Укажи путь: python3 insert-insurance-clone.py /путь/к/index.html")

    html = INDEX.read_text(encoding="utf-8", errors="ignore")

    if 'id="strahovanie-block"' in html:
        print("✓ Блок уже вставлен — ничего не меняю.")
        return

    backup = INDEX.with_suffix(".html.bak")
    shutil.copy(INDEX, backup)

    pos = None
    m = re.search(r"<footer", html, re.I)
    if m:
        pos = m.start()
    else:
        m = re.search(r"Юридический адрес", html)
        if m:
            pos = html.rfind("<", 0, m.start())
        else:
            m = re.search(r"</body>", html, re.I)
            pos = m.start() if m else len(html)

    INDEX.write_text(html[:pos] + BLOCK + html[pos:], encoding="utf-8")
    print(f"✓ Блок вставлен перед футером.\n✓ Резервная копия: {backup}")


if __name__ == "__main__":
    main()
