"use client";

import { useState } from "react";
import { CheckCircle2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { contactSchema, type ContactErrors } from "@/lib/validation/contact";
import { practices } from "@/lib/practices";
import { cn } from "@/lib/utils";

type Variant = "full" | "compact";
type Status = "idle" | "submitting" | "success";

const fieldBase =
  "w-full rounded-xl border bg-white px-4 py-3 text-[15px] text-ink placeholder:text-faint transition-colors focus:border-accent focus:outline-none focus:ring-4 focus:ring-accent/10";

export function ContactForm({
  variant = "full",
  className,
  tone = "default",
}: {
  variant?: Variant;
  className?: string;
  tone?: "default" | "onDark";
}) {
  const [status, setStatus] = useState<Status>("idle");
  const [errors, setErrors] = useState<ContactErrors>({});
  const [serverError, setServerError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setServerError(null);
    setErrors({});

    const fd = new FormData(e.currentTarget);
    const payload = {
      name: String(fd.get("name") ?? ""),
      phone: String(fd.get("phone") ?? ""),
      email: String(fd.get("email") ?? ""),
      topic: String(fd.get("topic") ?? ""),
      message: String(fd.get("message") ?? ""),
      company: String(fd.get("company") ?? ""),
      consent: fd.get("consent") === "on",
    };

    const parsed = contactSchema.safeParse(payload);
    if (!parsed.success) {
      const next: ContactErrors = {};
      for (const issue of parsed.error.issues) {
        const key = issue.path[0] as keyof ContactErrors;
        if (key && !next[key]) next[key] = issue.message;
      }
      setErrors(next);
      return;
    }

    setStatus("submitting");
    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed.data),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        if (data?.errors) setErrors(data.errors);
        setServerError(data?.message ?? "Не удалось отправить заявку.");
        setStatus("idle");
        return;
      }
      setStatus("success");
    } catch {
      setServerError("Проблема с сетью. Позвоните нам — мы на связи.");
      setStatus("idle");
    }
  }

  if (status === "success") {
    return (
      <div
        className={cn(
          "flex flex-col items-center gap-3 rounded-2xl border p-8 text-center",
          tone === "onDark"
            ? "border-white/10 bg-white/5 text-white"
            : "border-line bg-white text-ink",
          className,
        )}
      >
        <CheckCircle2 className="h-11 w-11 text-accent" aria-hidden />
        <h3 className="text-xl">Заявка отправлена</h3>
        <p className={tone === "onDark" ? "text-white/70" : "text-muted"}>
          Юрист свяжется с вами в течение 30 минут в рабочее время.
        </p>
      </div>
    );
  }

  const labelCls = cn(
    "mb-1.5 block text-[13px] font-medium",
    tone === "onDark" ? "text-white/70" : "text-graphite",
  );
  const errCls = "mt-1 text-[12px] text-red-600";

  return (
    <form onSubmit={onSubmit} noValidate className={cn("flex flex-col gap-4", className)}>
      <div className={variant === "full" ? "grid gap-4 sm:grid-cols-2" : "contents"}>
        <div>
          <label htmlFor="name" className={labelCls}>
            Имя <span className="text-accent">*</span>
          </label>
          <input
            id="name"
            name="name"
            autoComplete="name"
            placeholder="Как к вам обращаться"
            className={cn(fieldBase, errors.name ? "border-red-400" : "border-line-strong")}
          />
          {errors.name && <p className={errCls}>{errors.name}</p>}
        </div>
        <div>
          <label htmlFor="phone" className={labelCls}>
            Телефон <span className="text-accent">*</span>
          </label>
          <input
            id="phone"
            name="phone"
            type="tel"
            autoComplete="tel"
            placeholder="+7 (___) ___-__-__"
            className={cn(fieldBase, errors.phone ? "border-red-400" : "border-line-strong")}
          />
          {errors.phone && <p className={errCls}>{errors.phone}</p>}
        </div>
      </div>

      {variant === "full" && (
        <>
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="email" className={labelCls}>
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                placeholder="name@company.ru"
                className={cn(fieldBase, errors.email ? "border-red-400" : "border-line-strong")}
              />
              {errors.email && <p className={errCls}>{errors.email}</p>}
            </div>
            <div>
              <label htmlFor="topic" className={labelCls}>
                Направление
              </label>
              <select
                id="topic"
                name="topic"
                defaultValue=""
                className={cn(fieldBase, "border-line-strong")}
              >
                <option value="">Выберите практику</option>
                {practices.map((p) => (
                  <option key={p.slug} value={p.title}>
                    {p.title}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div>
            <label htmlFor="message" className={labelCls}>
              Кратко о задаче
            </label>
            <textarea
              id="message"
              name="message"
              rows={4}
              placeholder="Опишите ситуацию в нескольких предложениях"
              className={cn(fieldBase, "resize-none border-line-strong")}
            />
            {errors.message && <p className={errCls}>{errors.message}</p>}
          </div>
        </>
      )}

      {/* Honeypot — visually hidden, must remain empty */}
      <div className="absolute left-[-9999px]" aria-hidden>
        <label>
          Компания
          <input name="company" tabIndex={-1} autoComplete="off" />
        </label>
      </div>

      <label
        className={cn(
          "flex items-start gap-2.5 text-[13px] leading-snug",
          tone === "onDark" ? "text-white/60" : "text-muted",
        )}
      >
        <input
          type="checkbox"
          name="consent"
          className="mt-0.5 h-4 w-4 shrink-0 accent-[var(--color-accent)]"
        />
        <span>
          Согласен с обработкой персональных данных и политикой
          конфиденциальности.
        </span>
      </label>
      {errors.consent && <p className={errCls}>{errors.consent}</p>}

      {serverError && (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-[13px] text-red-700">
          {serverError}
        </p>
      )}

      <Button
        type="submit"
        variant="accent"
        size="lg"
        disabled={status === "submitting"}
      >
        {status === "submitting" ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden />
            Отправляем…
          </>
        ) : (
          "Получить консультацию"
        )}
      </Button>
    </form>
  );
}
