import type { Metadata } from "next";
import { ShieldCheck, Scale, HeartHandshake, Lock } from "lucide-react";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Container } from "@/components/ui/Container";
import { Reveal } from "@/components/ui/Reveal";
import { CtaBand } from "@/components/sections/CtaBand";

export const metadata: Metadata = {
  title: "О компании",
  description:
    "«ЮРЛИДЕР» — оформление допусков СРО в Санкт-Петербурге с 2010 года. Официальная аккредитация в надёжных СРО, прозрачные условия и сопровождение под ключ.",
};

const values = [
  {
    icon: Scale,
    title: "Прозрачные условия",
    text: "Называем итоговую сумму сразу. Вы платите только взнос в компенсационный фонд — без скрытых комиссий.",
  },
  {
    icon: ShieldCheck,
    title: "Надёжные СРО",
    text: "Работаем только с аккредитованными СРО, внесёнными в государственный реестр НОСТРОЙ и НОПРИЗ.",
  },
  {
    icon: Lock,
    title: "Ответственность",
    text: "Фиксируем сроки в договоре и доводим оформление допуска до результата.",
  },
  {
    icon: HeartHandshake,
    title: "Сопровождение",
    text: "Остаёмся на связи и после вступления: выписки, НРС, продление и переход в другую СРО.",
  },
];

const team = [
  { name: "Дмитрий Лидер", role: "Руководитель компании", exp: "с 2010 года в СРО", initials: "ДЛ" },
  { name: "Елена Соколова", role: "Специалист по СРО строителей", exp: "12 лет в сфере", initials: "ЕС" },
  { name: "Артём Власов", role: "Специалист по проектированию и изысканиям", exp: "10 лет в сфере", initials: "АВ" },
  { name: "Ольга Нечаева", role: "Специалист по НРС и выпискам", exp: "9 лет в сфере", initials: "ОН" },
];

export default function AboutPage() {
  return (
    <>
      <PageHeader
        eyebrow="О компании"
        title="Оформляем допуски СРО с 2010 года"
        subtitle="«ЮРЛИДЕР» — компания из Санкт-Петербурга, которая помогает строителям, проектировщикам и изыскателям быстро и без переплат получить допуск СРО."
        crumbs={[{ label: "Главная", href: "/" }, { label: "О компании" }]}
      />

      {/* Photo */}
      <Container className="pt-12">
        <Reveal>
          <div className="relative h-72 overflow-hidden rounded-3xl sm:h-96 lg:h-[460px]">
            <div
              aria-hidden
              className="absolute inset-0 bg-cover bg-center"
              style={{
                backgroundImage:
                  "url('https://images.unsplash.com/photo-1503387762-592deb58ef4e?q=80&w=2000&auto=format&fit=crop')",
              }}
            />
            <div
              aria-hidden
              className="absolute inset-0 bg-gradient-to-t from-ink/50 via-ink/10 to-transparent"
            />
          </div>
        </Reveal>
      </Container>

      {/* Intro + key facts */}
      <Section tone="paper">
        <div className="grid gap-12 lg:grid-cols-2 lg:gap-16">
          <div className="space-y-5 text-[17px] leading-relaxed text-graphite">
            <Reveal>
              <p>
                Компания работает с 2010 года и специализируется на оформлении
                допусков СРО для строительной, проектной и изыскательской
                деятельности. За это время мы оформили более 1 500 допусков.
              </p>
            </Reveal>
            <Reveal delay={60}>
              <p>
                Мы официально аккредитованы в надёжных СРО Санкт-Петербурга и
                берём на себя всю работу: подбор организации, подготовку
                документов и внесение специалистов в Национальный реестр.
              </p>
            </Reveal>
            <Reveal delay={120}>
              <p>
                Наш принцип — прозрачность и скорость: вы оплачиваете только
                взнос в компенсационный фонд и получаете допуск за 24 часа,
                без скрытых платежей.
              </p>
            </Reveal>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {[
              { v: "2010", l: "год основания" },
              { v: "1 500+", l: "оформленных допусков" },
              { v: "24 часа", l: "до получения допуска" },
              { v: "0 ₽", l: "за подготовку документов" },
            ].map((s, i) => (
              <Reveal key={s.l} delay={i * 60}>
                <div className="rounded-2xl border border-line bg-white p-7">
                  <div className="font-serif text-3xl font-semibold text-ink sm:text-4xl">
                    {s.v}
                  </div>
                  <div className="mt-2 text-sm text-muted">{s.l}</div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </Section>

      {/* Values */}
      <Section tone="white">
        <SectionHeading
          eyebrow="Принципы"
          title="Ценности, на которых стоит компания"
        />
        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {values.map((v, i) => (
            <Reveal key={v.title} delay={(i % 4) * 60}>
              <div className="flex h-full flex-col rounded-2xl border border-line bg-paper p-7">
                <span className="grid h-12 w-12 place-items-center rounded-xl bg-white text-accent shadow-[var(--shadow-card)]">
                  <v.icon className="h-6 w-6" strokeWidth={1.6} aria-hidden />
                </span>
                <h3 className="mt-5 text-lg text-ink">{v.title}</h3>
                <p className="mt-2 text-[15px] leading-relaxed text-muted">
                  {v.text}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </Section>

      {/* Team */}
      <Section tone="paper">
        <SectionHeading
          eyebrow="Команда"
          title="Специалисты по СРО"
          subtitle="С вами работают специалисты, которые лично ведут оформление допуска от заявки до выписки."
        />
        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {team.map((m, i) => (
            <Reveal key={m.name} delay={(i % 4) * 60}>
              <div className="flex h-full flex-col rounded-2xl border border-line bg-white p-7 text-center">
                <span className="mx-auto grid h-20 w-20 place-items-center rounded-full bg-ink font-serif text-2xl font-semibold text-accent">
                  {m.initials}
                </span>
                <h3 className="mt-5 text-lg text-ink">{m.name}</h3>
                <p className="mt-1 text-[14px] text-accent-strong">{m.role}</p>
                <p className="mt-2 text-[13px] text-muted">{m.exp}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </Section>

      <CtaBand />
    </>
  );
}
