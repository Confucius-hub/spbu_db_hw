#!/usr/bin/env python3
"""Вставляет/обновляет блок «Страхование по уровням 1–5» в локальном клоне сайта СССС.

Использование (на Mac пользователя):
    python3 scripts/insert-insurance-clone.py [путь_к_index.html]

По умолчанию путь: ~/Downloads/sro-ssss-clone/sro-ssss.ru/new_main/index.html
- Если блок уже есть — заменяет его на актуальную версию (апгрейд оформления).
- Резервная копия: index.html.bak (создаётся при первом изменении за запуск).
Суммы — из референса пользователя (sro-ism.ru → Страхование); правятся в ROWS.
"""

import re
import shutil
import sys
from pathlib import Path

DEFAULT = Path.home() / "Downloads/sro-ssss-clone/sro-ssss.ru/new_main/index.html"
INDEX = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT

TEAL = "#2e7e92"       # фирменный бирюзовый клона (шапка/футер)
HEAD = "#27495e"       # тёмный сине-серый заголовков
TEXT = "#51626f"
LINE = "#e3e9ed"

ROWS = [
    (1, "Первый уровень ответственности", "4&nbsp;000&nbsp;000,00&nbsp;₽"),
    (2, "Второй уровень ответственности", "15&nbsp;000&nbsp;000,00&nbsp;₽"),
    (3, "Третий уровень ответственности", "100&nbsp;000&nbsp;000,00&nbsp;₽"),
    (4, "Четвёртый уровень ответственности", "200&nbsp;000&nbsp;000,00&nbsp;₽"),
    (5, "Пятый уровень ответственности", "200&nbsp;000&nbsp;000,00&nbsp;₽"),
]


def row_html(i: int, n: int, label: str, total: str) -> str:
    bg = "#ffffff" if i % 2 == 0 else "#f7fafb"
    badge = (
        f'<span style="display:inline-block;width:26px;height:26px;line-height:26px;'
        f"text-align:center;border-radius:50%;background:#eaf3f6;color:{TEAL};"
        f'font-weight:700;font-size:13px;margin-right:12px;vertical-align:middle;">{n}</span>'
    )
    return (
        f'      <tr style="background:{bg};">'
        f'<td style="padding:13px 18px;border-top:1px solid {LINE};color:{HEAD};">{badge}{label}</td>'
        f'<td style="padding:13px 18px;border-top:1px solid {LINE};text-align:right;'
        f'font-weight:700;color:{HEAD};white-space:nowrap;">{total}</td></tr>'
    )


ROWS_HTML = "\n".join(row_html(i, n, label, total) for i, (n, label, total) in enumerate(ROWS))

BLOCK = f"""
<!-- === Страхование: градация по уровням (вставлено скриптом) === -->
<section id="strahovanie-block" style="max-width:1100px;margin:48px auto;padding:0 16px;font-family:inherit;">
  <div style="background:#fff;border:1px solid {LINE};border-radius:14px;box-shadow:0 8px 28px rgba(31,68,84,.08);overflow:hidden;">

    <div style="padding:30px 32px 6px;">
      <div style="font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:{TEAL};">Раскрытие информации</div>
      <h2 style="margin:10px 0 0;color:{HEAD};font-size:26px;font-weight:700;line-height:1.25;">Страхование ответственности членов Ассоциации</h2>
      <div style="width:56px;height:3px;background:{TEAL};border-radius:2px;margin:14px 0 16px;"></div>
      <p style="color:{TEXT};margin:0;line-height:1.6;max-width:860px;">
        Минимальный размер страховой суммы по договору страхования гражданской ответственности&nbsp;(ВВ)
        зависит от уровня ответственности члена Ассоциации в&nbsp;соответствии со&nbsp;ст.&nbsp;55.16
        Градостроительного кодекса&nbsp;РФ:
      </p>
    </div>

    <div style="padding:20px 32px 4px;overflow-x:auto;">
      <div style="border:1px solid {LINE};border-radius:10px;overflow:hidden;min-width:560px;">
        <table style="border-collapse:collapse;width:100%;font-size:15px;">
          <thead>
            <tr style="background:{TEAL};color:#fff;">
              <th style="padding:13px 18px;text-align:left;font-weight:600;">Уровень ответственности члена Ассоциации</th>
              <th style="padding:13px 18px;text-align:right;font-weight:600;white-space:nowrap;">Страховая сумма, не&nbsp;менее</th>
            </tr>
          </thead>
          <tbody>
{ROWS_HTML}
          </tbody>
        </table>
      </div>
      <p style="color:#8b9aa6;font-size:12.5px;margin:10px 2px 0;">Уровни ответственности — по стоимости работ по одному договору строительного подряда (ст.&nbsp;55.16 ГрК&nbsp;РФ).</p>
    </div>

    <div style="margin:18px 32px 30px;padding:16px 20px;background:#f3f8fa;border-left:4px solid {TEAL};border-radius:0 10px 10px 0;">
      <div style="font-weight:700;color:{HEAD};margin-bottom:4px;">Страхование по договорам (ОДО)</div>
      <div style="color:{TEXT};line-height:1.6;">
        По договорам подряда, заключённым конкурентными способами, член Ассоциации обеспечивает действующий
        договор комбинированного страхования риска ответственности по каждому такому договору.
        Полные требования и перечень страховых организаций&nbsp;— по&nbsp;запросу.
      </div>
    </div>

  </div>
</section>
"""

OLD_BLOCK_RE = re.compile(r"\n?<!-- === Страхование[\s\S]*?</section>\s*", re.I)


def main() -> None:
    if not INDEX.exists():
        sys.exit(f"✗ Файл не найден: {INDEX}\n  Укажи путь: python3 insert-insurance-clone.py /путь/к/index.html")

    html = INDEX.read_text(encoding="utf-8", errors="ignore")
    backup = INDEX.with_suffix(".html.bak")
    shutil.copy(INDEX, backup)

    if OLD_BLOCK_RE.search(html):
        html = OLD_BLOCK_RE.sub(BLOCK, html, count=1)
        msg = "✓ Существующий блок заменён на новую версию оформления."
    else:
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
        html = html[:pos] + BLOCK + html[pos:]
        msg = "✓ Блок вставлен перед футером."

    INDEX.write_text(html, encoding="utf-8")
    print(msg)
    print(f"✓ Резервная копия: {backup}")


if __name__ == "__main__":
    main()
