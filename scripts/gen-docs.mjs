// Генератор PDF-файлов документов СРО.
// Создаёт официальные информационные листы (титульная страница с реальными
// реквизитами организации и пометкой «актуальная редакция — по запросу»).
// НЕ содержит выдуманного юридического текста уставов/положений.
//
// Запуск: node scripts/gen-docs.mjs
// Результат: public/docs/*.pdf (далее страница «Документы» сама покажет «Скачать»).

import PDFDocument from "pdfkit";
import { createWriteStream, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const outDir = join(root, "public", "docs");
mkdirSync(outDir, { recursive: true });

const FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf";
const FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf";

const NAVY = "#142340";
const GOLD = "#c4933a";
const SLATE = "#475569";

const org = {
  full: 'Саморегулируемая организация Ассоциация\n«Строительный союз Северной столицы»',
  reg: "СРО-С-335-25122025",
  regDate: "25.12.2025",
  phone: "+7 (812) 703-88-77",
  email: "info@sro-ssss.ru",
  address: "191119, Санкт-Петербург, Лиговский пр-т, д. 114, лит. А",
};

// title -> имя файла (синхронно с src/lib/documents.ts)
const docs = [
  ["Устав Ассоциации «Строительный союз Северной столицы»", "ustav.pdf", "Учредительный документ"],
  ["Выписка из реестра НОСТРОЙ", "vypiska-nostroy.pdf", "Сведения о членстве в реестре"],
  ["Свидетельство о государственной регистрации", "svidetelstvo.pdf", "Регистрационные сведения"],
  ["Положение о компенсационном фонде возмещения вреда", "polozhenie-kf-vv.pdf", "Внутренний документ"],
  ["Положение о компенсационном фонде обеспечения договорных обязательств", "polozhenie-kf-odo.pdf", "Внутренний документ"],
  ["Положение о членстве, размере и порядке уплаты взносов", "polozhenie-chlenstvo.pdf", "Внутренний документ"],
  ["Положение о контроле за деятельностью членов СРО", "polozhenie-kontrol.pdf", "Внутренний документ"],
  ["Положение о мерах дисциплинарного воздействия", "polozhenie-disciplina.pdf", "Внутренний документ"],
  ["Квалификационные стандарты специалистов", "standarty-kvalifikacia.pdf", "Стандарт"],
  ["Стандарты и правила саморегулирования", "standarty-pravila.pdf", "Стандарт"],
  ["Протоколы общих собраний членов", "protokoly-sobrania.pdf", "Протоколы"],
  ["Протоколы заседаний коллегиального органа управления", "protokoly-kollegial.pdf", "Протоколы"],
  ["Заявление о приёме в члены СРО", "zayavlenie-priem.docx", "Форма / бланк"],
  ["Анкета члена СРО", "anketa.docx", "Форма / бланк"],
  ["Форма уведомления о заключённом договоре подряда", "uvedomlenie-dogovor.docx", "Форма / бланк"],
];

function buildPdf(title, kind, fileName) {
  // Формы (.docx по имени) тоже сохраняем как PDF-бланк, меняя расширение на .pdf,
  // чтобы файл реально открывался; имя в documents.ts тогда должно оканчиваться .pdf.
  const outName = fileName.replace(/\.docx$/, ".pdf");
  return new Promise((resolve) => {
    const doc = new PDFDocument({ size: "A4", margin: 64, info: { Title: title, Author: "СРО СССС" } });
    const stream = createWriteStream(join(outDir, outName));
    doc.pipe(stream);

    doc.registerFont("body", FONT);
    doc.registerFont("bold", FONT_BOLD);

    const W = doc.page.width;
    const M = doc.page.margins.left;
    const cw = W - M * 2;

    // Верхняя золотая полоса
    doc.rect(0, 0, W, 8).fill(GOLD);

    // Шапка с реквизитами
    doc.fillColor(NAVY).font("bold").fontSize(13).text("СРО «СССС»", M, 48);
    doc.font("body").fontSize(9).fillColor(SLATE)
      .text(org.full.replace("\n", " "), M, 66, { width: cw - 160 });
    doc.fontSize(8).fillColor(SLATE).text(
      `Реестр НОСТРОЙ: ${org.reg}  ·  от ${org.regDate}`,
      M, 96, { width: cw },
    );

    doc.moveTo(M, 116).lineTo(W - M, 116).strokeColor("#e2e8f0").lineWidth(1).stroke();

    // Тип документа
    doc.font("body").fontSize(10).fillColor(GOLD).text(kind.toUpperCase(), M, 150);

    // Заголовок документа
    doc.font("bold").fontSize(22).fillColor(NAVY).text(title, M, 172, { width: cw, lineGap: 4 });

    // Пояснение
    const y = doc.y + 28;
    doc.roundedRect(M, y, cw, 132, 12).fill("#f1f5f9");
    doc.fillColor(NAVY).font("bold").fontSize(12).text("О документе", M + 20, y + 18);
    doc.font("body").fontSize(11).fillColor(SLATE).text(
      "Настоящий лист является официальной справкой о документе. " +
        "Актуальная редакция предоставляется по запросу — обратитесь в Ассоциацию любым удобным способом.",
      M + 20, y + 40, { width: cw - 40, lineGap: 3 },
    );
    doc.font("bold").fillColor(NAVY).fontSize(11).text(`Телефон:  ${org.phone}`, M + 20, y + 88);
    doc.font("bold").fillColor(NAVY).fontSize(11).text(`E-mail:  ${org.email}`, M + 20, y + 106);

    // Реквизиты внизу
    const fy = doc.page.height - 120;
    doc.moveTo(M, fy).lineTo(W - M, fy).strokeColor("#e2e8f0").lineWidth(1).stroke();
    doc.font("body").fontSize(9).fillColor(SLATE)
      .text(org.full.replace("\n", " "), M, fy + 14, { width: cw })
      .text(`Адрес: ${org.address}`, M, fy + 40, { width: cw })
      .text(`Документ сформирован: ${new Date().toLocaleDateString("ru-RU")}`, M, fy + 56);

    doc.rect(0, doc.page.height - 8, W, 8).fill(NAVY);

    doc.end();
    stream.on("finish", () => resolve(outName));
  });
}

const made = [];
for (const [title, file, kind] of docs) {
  made.push(await buildPdf(title, kind, file));
}
console.log(`✓ Создано PDF: ${made.length}`);
console.log(made.join("\n"));
