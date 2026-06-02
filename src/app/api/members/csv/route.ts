import { members } from "@/lib/members-registry";

export const dynamic = "force-static";

const HEADERS = [
  "Наименование",
  "Тип",
  "Статус",
  "Рег. номер",
  "Дата регистрации",
  "ОГРН/ОГРНИП",
  "ИНН",
  "КФ ВВ (руб.)",
  "Лимит по одному договору",
];

function escape(value: string | number): string {
  const s = String(value);
  if (/[",\n;]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
  return s;
}

export function GET() {
  const rows = members.map((m) =>
    [m.name, m.type, m.status, m.reg, m.date, m.ogrn, m.inn, m.kfVv, m.maxContract]
      .map(escape)
      .join(";"),
  );
  // BOM для корректного открытия в Excel с кириллицей
  const csv = "﻿" + [HEADERS.join(";"), ...rows].join("\r\n");

  return new Response(csv, {
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": 'attachment; filename="sro-ssss-members.csv"',
      "Cache-Control": "public, max-age=300",
    },
  });
}
