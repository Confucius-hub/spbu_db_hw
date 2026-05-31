// Генератор PDF-файлов документов СРО.
// Список документов берётся напрямую из src/lib/documents.ts (через tsx) —
// без дублирования. Каждый PDF — официальный информационный лист с реальными
// реквизитами СРО и пометкой о предоставлении полной версии по запросу.
// Юридическое содержание НЕ выдумывается.
//
// Запуск: npx tsx scripts/gen-docs.mjs

import PDFDocument from "pdfkit";
import { createWriteStream, mkdirSync, readdirSync, rmSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { documents } from "../src/lib/documents.ts";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const outDir = join(root, "public", "docs");
mkdirSync(outDir, { recursive: true });

// Чистим старые PDF, чтобы не оставалось файлов от прежней структуры
for (const f of readdirSync(outDir)) {
  if (f.endsWith(".pdf")) rmSync(join(outDir, f));
}

const FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf";
const FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf";
const NAVY = "#142340";
const GOLD = "#c4933a";
const SLATE = "#475569";

const org = {
  full: 'Саморегулируемая организация Ассоциация «Строительный союз Северной столицы»',
  reg: "СРО-С-335-25122025",
  phone: "+7 (812) 703-88-77",
  email: "info@sro-ssss.ru",
  address: "191119, Санкт-Петербург, Лиговский пр-т, д. 114, лит. А",
};

function buildPdf(doc0) {
  const { title, file, category, date } = doc0;
  return new Promise((resolve) => {
    const doc = new PDFDocument({ size: "A4", margin: 64, info: { Title: title, Author: "СРО СССС" } });
    const stream = createWriteStream(join(outDir, file));
    doc.pipe(stream);
    doc.registerFont("body", FONT);
    doc.registerFont("bold", FONT_BOLD);

    const W = doc.page.width;
    const M = doc.page.margins.left;
    const cw = W - M * 2;

    doc.rect(0, 0, W, 8).fill(GOLD);
    doc.fillColor(NAVY).font("bold").fontSize(13).text("СРО «СССС»", M, 48);
    doc.font("body").fontSize(9).fillColor(SLATE).text(org.full, M, 66, { width: cw - 150 });
    doc.fontSize(8).text(`Реестр НОСТРОЙ: ${org.reg}`, M, 98, { width: cw });
    doc.moveTo(M, 116).lineTo(W - M, 116).strokeColor("#e2e8f0").lineWidth(1).stroke();

    doc.font("body").fontSize(10).fillColor(GOLD).text(category.toUpperCase(), M, 150);
    doc.font("bold").fontSize(21).fillColor(NAVY).text(title, M, 172, { width: cw, lineGap: 4 });
    if (date) doc.font("body").fontSize(10).fillColor(SLATE).text(`Дата размещения: ${date}`, M, doc.y + 6);

    const y = doc.y + 26;
    doc.roundedRect(M, y, cw, 130, 12).fill("#f1f5f9");
    doc.fillColor(NAVY).font("bold").fontSize(12).text("О документе", M + 20, y + 18);
    doc.font("body").fontSize(11).fillColor(SLATE).text(
      "Официальная справка о документе саморегулируемой организации. " +
        "Полная актуальная редакция предоставляется по запросу — обратитесь в Ассоциацию.",
      M + 20, y + 40, { width: cw - 40, lineGap: 3 },
    );
    doc.font("bold").fillColor(NAVY).fontSize(11).text(`Телефон:  ${org.phone}`, M + 20, y + 86);
    doc.text(`E-mail:  ${org.email}`, M + 20, y + 104);

    const fy = doc.page.height - 116;
    doc.moveTo(M, fy).lineTo(W - M, fy).strokeColor("#e2e8f0").lineWidth(1).stroke();
    doc.font("body").fontSize(9).fillColor(SLATE)
      .text(org.full, M, fy + 14, { width: cw })
      .text(`Адрес: ${org.address}`, M, fy + 40, { width: cw })
      .text(`Сформировано: ${new Date().toLocaleDateString("ru-RU")}`, M, fy + 56);
    doc.rect(0, doc.page.height - 8, W, 8).fill(NAVY);

    doc.end();
    stream.on("finish", () => resolve(file));
  });
}

let n = 0;
for (const d of documents) {
  await buildPdf(d);
  n++;
}
console.log(`✓ Создано PDF: ${n}`);
