import type { LeadInput } from "./validation";

const TYPE_LABELS: Record<string, string> = {
  CALLBACK: "Обратный звонок",
  CONSULTATION: "Консультация",
  APPLICATION: "Заявка на вступление",
  CALCULATOR: "Расчёт стоимости",
};

/**
 * Отправка уведомления о новой заявке в Telegram.
 * Включается, если заданы TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID.
 * Без них — тихо пропускается (заявка остаётся сохранённой в БД).
 * Реализовано без внешних зависимостей (нативный fetch).
 */
export async function notifyLead(lead: LeadInput): Promise<void> {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) return;

  const esc = (s: string) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  const lines = [
    `🔔 <b>Новая заявка с сайта</b>`,
    ``,
    `<b>Тип:</b> ${esc(TYPE_LABELS[lead.type] ?? lead.type)}`,
    `<b>Имя:</b> ${esc(lead.name)}`,
    `<b>Телефон:</b> ${esc(lead.phone)}`,
    lead.email ? `<b>E-mail:</b> ${esc(lead.email)}` : "",
    lead.company ? `<b>Компания:</b> ${esc(lead.company)}` : "",
    lead.message ? `<b>Сообщение:</b> ${esc(lead.message)}` : "",
    lead.source ? `<i>Источник: ${esc(lead.source)}</i>` : "",
  ].filter(Boolean);

  try {
    await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: chatId,
        text: lines.join("\n"),
        parse_mode: "HTML",
        disable_web_page_preview: true,
      }),
      // Не блокируем ответ пользователю надолго
      signal: AbortSignal.timeout(5000),
    });
  } catch {
    // Уведомление не критично — заявка уже сохранена в БД
  }
}
