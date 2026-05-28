import { Star, ShieldCheck, ArrowRight } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Reveal } from "@/components/ui/Reveal";
import { ContactForm } from "./ContactForm";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-ink text-white">
      {/* Background layers */}
      <div aria-hidden className="absolute inset-0 bg-grid-dark opacity-60" />
      <div
        aria-hidden
        className="absolute -right-40 -top-40 h-[520px] w-[520px] rounded-full opacity-50 blur-3xl"
        style={{
          background:
            "radial-gradient(circle, rgba(168,124,79,0.35), transparent 65%)",
        }}
      />
      <div
        aria-hidden
        className="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-b from-transparent to-ink"
      />

      <Container className="relative grid items-center gap-14 pb-20 pt-16 lg:grid-cols-12 lg:gap-10 lg:pb-28 lg:pt-24">
        {/* Copy */}
        <div className="lg:col-span-7">
          <Reveal>
            <Badge tone="onDark">С 2010 года · Москва</Badge>
          </Reveal>
          <Reveal delay={60}>
            <h1 className="mt-6 max-w-2xl text-balance text-4xl leading-[1.06] text-white sm:text-5xl lg:text-6xl">
              Защищаем ваш бизнес
              <br />
              и капитал —{" "}
              <span className="italic text-accent">по существу</span>.
            </h1>
          </Reveal>
          <Reveal delay={120}>
            <p className="mt-6 max-w-xl text-lg leading-relaxed text-white/70">
              Юридическая компания «Лидер» — стратегия и результат в спорах,
              банкротстве, налогах и сделках. Берёмся за дело, только когда
              видим реальный путь к победе.
            </p>
          </Reveal>

          <Reveal delay={180}>
            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Button href="/contacts" variant="accent" size="lg">
                Бесплатная консультация
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Button>
              <Button href="/practices" variant="onDark" size="lg">
                Наши практики
              </Button>
            </div>
          </Reveal>

          <Reveal delay={240}>
            <div className="mt-10 flex flex-wrap items-center gap-x-8 gap-y-4 border-t border-white/10 pt-7">
              <div className="flex items-center gap-2.5">
                <div className="flex" aria-hidden>
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star
                      key={i}
                      className="h-4 w-4 fill-accent text-accent"
                    />
                  ))}
                </div>
                <span className="text-sm text-white/70">
                  <span className="font-semibold text-white">4.9</span> · 200+
                  отзывов
                </span>
              </div>
              <div className="flex items-center gap-2.5 text-sm text-white/70">
                <ShieldCheck className="h-5 w-5 text-accent" aria-hidden />
                <span>
                  <span className="font-semibold text-white">3 200+</span>{" "}
                  выигранных дел
                </span>
              </div>
            </div>
          </Reveal>
        </div>

        {/* Quick lead card */}
        <div className="lg:col-span-5">
          <Reveal delay={160}>
            <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6 shadow-[var(--shadow-lift)] backdrop-blur sm:p-7">
              <div className="mb-5">
                <h2 className="font-sans text-xl font-semibold text-white">
                  Разберём вашу ситуацию
                </h2>
                <p className="mt-1 text-sm text-white/60">
                  Бесплатно, конфиденциально. Ответим в течение 30 минут.
                </p>
              </div>
              <ContactForm variant="compact" tone="onDark" />
            </div>
          </Reveal>
        </div>
      </Container>
    </section>
  );
}
