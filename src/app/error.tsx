"use client";

import { useEffect } from "react";
import { Container } from "@/components/ui/container";
import { Button } from "@/components/ui/button";
import { Icon } from "@/lib/icons";

/** Глобальная граница ошибок — аккуратный экран вместо «белого экрана смерти». */
export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // В реальном проде сюда можно подключить логирование (Sentry и т.п.)
    console.error(error);
  }, [error]);

  return (
    <section className="relative overflow-hidden bg-navy-950 text-white">
      <div className="absolute inset-0 bg-grid opacity-40" aria-hidden />
      <Container className="relative">
        <div className="flex min-h-[70vh] flex-col items-center justify-center py-20 text-center">
          <span className="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-white/10 text-gold-400">
            <Icon name="ShieldCheck" className="h-8 w-8" />
          </span>
          <h1 className="mt-6 text-2xl font-bold text-white sm:text-3xl">
            Что-то пошло не так
          </h1>
          <p className="mt-3 max-w-md text-slate-300">
            Произошла непредвиденная ошибка. Попробуйте обновить страницу или вернитесь на главную —
            мы уже знаем о проблеме.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <Button onClick={reset} variant="gold" size="lg">
              <Icon name="ArrowRight" className="h-4 w-4" />
              Повторить
            </Button>
            <Button href="/" variant="white" size="lg">
              На главную
            </Button>
          </div>
        </div>
      </Container>
    </section>
  );
}
