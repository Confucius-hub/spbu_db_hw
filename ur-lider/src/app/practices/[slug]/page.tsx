import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Check } from "lucide-react";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import { Reveal } from "@/components/ui/Reveal";
import { Faq } from "@/components/sections/Faq";
import { ContactForm } from "@/components/sections/ContactForm";
import { CtaBand } from "@/components/sections/CtaBand";
import { getPractice, practices } from "@/lib/practices";
import { site } from "@/lib/site";

export function generateStaticParams() {
  return practices.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const practice = getPractice(slug);
  if (!practice) return { title: "Практика не найдена" };
  return {
    title: practice.title,
    description: practice.summary,
  };
}

export default async function PracticePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const practice = getPractice(slug);
  if (!practice) notFound();

  return (
    <>
      <PageHeader
        eyebrow={practice.audience}
        title={practice.title}
        subtitle={practice.summary}
        crumbs={[
          { label: "Главная", href: "/" },
          { label: "Практики", href: "/practices" },
          { label: practice.title },
        ]}
      />

      <Section tone="paper">
        <div className="grid gap-10 lg:grid-cols-[1fr_360px] lg:gap-14">
          {/* Main */}
          <div className="flex flex-col gap-16">
            {/* Services */}
            <div>
              <h2 className="text-2xl text-ink sm:text-3xl">Что входит в работу</h2>
              <ul className="mt-7 grid gap-x-8 gap-y-4 sm:grid-cols-2">
                {practice.services.map((s, i) => (
                  <Reveal as="li" key={s} delay={(i % 2) * 60}>
                    <div className="flex items-start gap-3">
                      <span className="mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded-full bg-accent-soft text-accent-strong">
                        <Check className="h-3.5 w-3.5" strokeWidth={3} aria-hidden />
                      </span>
                      <span className="text-[15px] leading-relaxed text-graphite">
                        {s}
                      </span>
                    </div>
                  </Reveal>
                ))}
              </ul>
            </div>

            {/* Outcomes */}
            <div>
              <h2 className="text-2xl text-ink sm:text-3xl">Результаты практики</h2>
              <div className="mt-7 grid gap-4 sm:grid-cols-3">
                {practice.outcomes.map((o, i) => (
                  <Reveal key={o.label} delay={i * 70}>
                    <div className="rounded-2xl border border-line bg-white p-6">
                      <div className="font-serif text-3xl font-semibold text-ink">
                        {o.value}
                      </div>
                      <div className="mt-1.5 text-sm text-muted">{o.label}</div>
                    </div>
                  </Reveal>
                ))}
              </div>
            </div>

            {/* FAQ */}
            <div>
              <h2 className="text-2xl text-ink sm:text-3xl">Частые вопросы</h2>
              <div className="mt-7">
                <Faq items={practice.faq} />
              </div>
            </div>
          </div>

          {/* Sticky aside */}
          <aside className="lg:sticky lg:top-28 lg:self-start">
            <div className="rounded-2xl border border-line bg-white p-6 shadow-[var(--shadow-card)]">
              <h2 className="font-sans text-lg font-semibold text-ink">
                Нужна помощь по этому направлению?
              </h2>
              <p className="mt-1.5 text-sm text-muted">
                Оставьте контакты — профильный юрист перезвонит и оценит
                ситуацию бесплатно.
              </p>
              <div className="mt-5">
                <ContactForm variant="compact" />
              </div>
              <a
                href={`tel:${site.phoneHref}`}
                className="mt-4 block text-center text-[15px] font-semibold text-ink hover:text-accent-strong"
              >
                {site.phone}
              </a>
            </div>
          </aside>
        </div>
      </Section>

      <CtaBand />
    </>
  );
}
