import { Container } from "@/components/ui/container";
import { Button } from "@/components/ui/button";
import { CallbackButton } from "@/components/forms/callback-modal";
import { Calculator } from "@/components/home/calculator";
import { Photo } from "@/components/ui/photo";
import { Cityscape } from "@/components/brand/cityscape";
import { Icon, type IconName } from "@/lib/icons";
import { site, media } from "@/lib/site";

const trust: { icon: IconName; title: string; text: string }[] = [
  { icon: "BadgeCheck", title: "Официально", text: "В реестре НОСТРОЙ" },
  { icon: "ShieldCheck", title: "Надёжно", text: "Компенсационные фонды" },
  { icon: "Zap", title: "Быстро", text: "Решение за 1 день" },
];

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-navy-950 text-white">
      {/* Фоновое фото (с фолбэком на градиент) + затемнение для читаемости текста */}
      <Photo
        src={media.hero}
        priority
        className="absolute inset-0"
        imgClassName="opacity-25 [mask-image:linear-gradient(to_right,black,transparent_85%)]"
      />
      <div
        className="absolute inset-0 bg-gradient-to-r from-navy-950 via-navy-950/85 to-navy-900/70"
        aria-hidden
      />
      {/* Декоративный фон */}
      <div className="absolute inset-0 bg-grid opacity-40" aria-hidden />
      <div
        className="absolute -right-40 -top-40 h-[36rem] w-[36rem] rounded-full bg-navy-700/30 blur-3xl"
        aria-hidden
      />
      <div
        className="absolute -left-40 bottom-0 h-[28rem] w-[28rem] rounded-full bg-gold-600/10 blur-3xl"
        aria-hidden
      />
      {/* Фирменная архитектурная графика по нижнему краю */}
      <Cityscape className="pointer-events-none absolute inset-x-0 bottom-0 h-40 w-full text-gold-500/15" />

      <Container className="relative">
        <div className="grid items-center gap-12 py-14 lg:grid-cols-[1.05fr_0.95fr] lg:py-20">
          {/* Контент */}
          <div className="animate-rise">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-4 py-1.5 text-sm text-slate-200">
              <span className="h-2 w-2 rounded-full bg-gold-400" />
              {site.tagline} · с {site.founded} года
            </div>

            <h1 className="mt-6 font-display text-4xl font-extrabold leading-[1.08] tracking-tight text-white sm:text-5xl lg:text-[3.4rem]">
              Вступление в&nbsp;СРО&nbsp;строителей{" "}
              <span className="text-gold-gradient">за 1 день</span>
            </h1>

            <p className="mt-5 max-w-xl text-lg leading-relaxed text-slate-300">
              Без скрытых платежей и сложных процедур. Помогаем получить допуск к строительным
              работам под ключ — от заявки до записи в реестре.
            </p>

            <div className="mt-7 flex flex-wrap gap-3">
              <Button href="/membership#calculator" variant="gold" size="lg">
                Рассчитать стоимость
                <Icon name="ArrowRight" className="h-4 w-4" />
              </Button>
              <CallbackButton variant="white" label="Бесплатная консультация" />
            </div>

            <div className="mt-10 grid max-w-xl grid-cols-3 gap-4">
              {trust.map((t) => (
                <div key={t.title} className="flex items-start gap-3">
                  <span className="mt-0.5 inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/10 text-gold-400">
                    <Icon name={t.icon} className="h-5 w-5" />
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-white">{t.title}</p>
                    <p className="text-xs text-slate-400">{t.text}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Калькулятор */}
          <div id="calculator" className="animate-rise lg:scroll-mt-28">
            <Calculator variant="compact" />
          </div>
        </div>
      </Container>
    </section>
  );
}
