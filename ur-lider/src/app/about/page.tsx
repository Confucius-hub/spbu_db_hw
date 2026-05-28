import type { Metadata } from "next";
import { ShieldCheck, Scale, HeartHandshake, Lock } from "lucide-react";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";
import { CtaBand } from "@/components/sections/CtaBand";

export const metadata: Metadata = {
  title: "О компании",
  description:
    "Юридическая компания «Лидер»: 14 лет практики, команда профильных юристов, принципы работы и ценности.",
};

const values = [
  {
    icon: Scale,
    title: "Честная оценка",
    text: "Не беремся за бесперспективные дела ради гонорара. Говорим как есть.",
  },
  {
    icon: ShieldCheck,
    title: "Ответственность",
    text: "Закрепляем условия и сроки в договоре и отвечаем за результат.",
  },
  {
    icon: Lock,
    title: "Конфиденциальность",
    text: "Все обстоятельства дела защищены и не покидают стен компании.",
  },
  {
    icon: HeartHandshake,
    title: "Партнёрство",
    text: "Ценим долгосрочные отношения выше разовой выгоды.",
  },
];

const team = [
  { name: "Дмитрий Лидер", role: "Управляющий партнёр", exp: "22 года практики", initials: "ДЛ" },
  { name: "Елена Соколова", role: "Партнёр, налоговая практика", exp: "16 лет практики", initials: "ЕС" },
  { name: "Артём Власов", role: "Руководитель арбитражной практики", exp: "14 лет практики", initials: "АВ" },
  { name: "Ольга Нечаева", role: "Руководитель практики банкротства", exp: "12 лет практики", initials: "ОН" },
];

export default function AboutPage() {
  return (
    <>
      <PageHeader
        eyebrow="О компании"
        title="14 лет защищаем интересы клиентов"
        subtitle="«Лидер» — команда юристов и адвокатов, для которых репутация важнее сиюминутной выгоды. Мы соединяем глубокую экспертизу с человеческим подходом."
        crumbs={[{ label: "Главная", href: "/" }, { label: "О компании" }]}
      />

      {/* Intro + key facts */}
      <Section tone="paper">
        <div className="grid gap-12 lg:grid-cols-2 lg:gap-16">
          <div className="space-y-5 text-[17px] leading-relaxed text-graphite">
            <Reveal>
              <p>
                Компания основана в 2010 году группой практикующих юристов с
                опытом работы в крупном бизнесе и государственных органах. За это
                время мы провели более 3 200 дел и взыскали для клиентов свыше
                5 миллиардов рублей.
              </p>
            </Reveal>
            <Reveal delay={60}>
              <p>
                Сегодня «Лидер» — это шесть профильных практик и выделенные
                команды под каждое направление. Мы одинаково уверенно работаем
                с предпринимателями, крупными компаниями и частными клиентами.
              </p>
            </Reveal>
            <Reveal delay={120}>
              <p>
                Наш принцип прост: браться за дело только тогда, когда мы видим
                реальный путь к результату — и доводить его до конца.
              </p>
            </Reveal>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {[
              { v: "2010", l: "год основания" },
              { v: "3 200+", l: "проведённых дел" },
              { v: "5,4 млрд ₽", l: "взыскано для клиентов" },
              { v: "92%", l: "дел в пользу клиента" },
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
          title="Партнёры и руководители практик"
          subtitle="С вами работают специалисты, которые лично отвечают за результат по своему направлению."
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
