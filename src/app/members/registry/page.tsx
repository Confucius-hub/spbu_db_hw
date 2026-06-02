import type { Metadata } from "next";
import { Section, SectionHeading } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Cta } from "@/components/sections/cta";
import { MembersTable } from "@/components/members/members-table";
import { Icon, type IconName } from "@/lib/icons";
import { site } from "@/lib/site";
import { members } from "@/lib/members-registry";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Реестр членов СРО",
  description:
    "Единый реестр членов СРО и их обязательств по договорам подряда в НОСТРОЙ. Как проверить статус компании по регистрационному номеру СРО-С-335-25122025.",
  path: "/members/registry",
});

const steps: { icon: IconName; title: string; text: string }[] = [
  {
    icon: "ExternalLink",
    title: "Откройте единый реестр НОСТРОЙ",
    text: "Реестр членов СРО и их обязательств ведётся Национальным объединением строителей и доступен публично.",
  },
  {
    icon: "Search",
    title: "Найдите организацию",
    text: "Поиск по наименованию, ИНН компании или по регистрационному номеру нашей СРО.",
  },
  {
    icon: "BadgeCheck",
    title: "Проверьте сведения",
    text: "Статус членства, уровень ответственности по компенсационным фондам и обязательства по договорам.",
  },
];

const shows = [
  "Факт и дата членства компании в СРО",
  "Уровень ответственности по компенсационному фонду возмещения вреда",
  "Уровень ответственности по фонду обеспечения договорных обязательств",
  "Сведения об обязательствах по договорам строительного подряда",
  "Право выполнять работы и наличие ограничений",
];

export default function MembersRegistryPage() {
  return (
    <>
      <PageHeader
        eyebrow="Членам СРО"
        title="Реестр членов СРО"
        description="Единый реестр членов СРО и их обязательств по договорам подряда ведётся в НОСТРОЙ и открыт для проверки."
        breadcrumbs={[{ label: "Членам СРО", href: "/members" }, { label: "Реестр членов" }]}
      >
        <Button href={site.nostroyUrl} external variant="gold" size="lg">
          <Icon name="ExternalLink" className="h-5 w-5" />
          Открыть реестр НОСТРОЙ
        </Button>
      </PageHeader>

      {/* Реестр компаний — членов СРО (реальные данные с sro-ssss.ru/register) */}
      <Section tone="muted">
        <SectionHeading
          align="left"
          eyebrow="Реестр компаний"
          title="Члены СРО «СССС»"
          description="Сведения о действующих членах саморегулируемой организации. Полная версия реестра ведётся в НОСТРОЙ."
        />
        <div className="mt-8">
          <MembersTable members={members} />
        </div>
      </Section>

      {/* Карточка организации в реестре */}
      <Section tone="white">
        <div className="grid items-start gap-10 lg:grid-cols-2">
          <div>
            <SectionHeading
              align="left"
              eyebrow="Наш статус"
              title="Проверьте нас в государственном реестре"
              description="Сведения об Ассоциации и её членах внесены в единый реестр НОСТРОЙ. Проверка занимает меньше минуты."
            />
            <ul className="mt-6 space-y-3">
              {shows.map((s) => (
                <li key={s} className="flex items-start gap-3 text-slate-700">
                  <span className="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                    <Icon name="Check" className="h-4 w-4" strokeWidth={2.5} />
                  </span>
                  {s}
                </li>
              ))}
            </ul>
          </div>

          <Card className="overflow-hidden">
            <div className="bg-navy-900 p-6 text-white">
              <div className="flex items-center gap-3">
                <span className="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-white/10 text-gold-400">
                  <Icon name="Landmark" className="h-6 w-6" />
                </span>
                <div>
                  <p className="font-semibold text-white">Реестр НОСТРОЙ</p>
                  <p className="text-sm text-slate-300">Национальное объединение строителей</p>
                </div>
              </div>
            </div>
            <dl className="divide-y divide-slate-100">
              {[
                ["Организация", site.legalName],
                ["Регистрационный номер", site.registryNumber],
                ["Дата внесения в реестр", site.registryDate],
              ].map(([k, v]) => (
                <div key={k} className="grid gap-1 px-6 py-4 sm:grid-cols-3 sm:gap-4">
                  <dt className="text-sm text-slate-500">{k}</dt>
                  <dd className="font-medium text-navy-900 sm:col-span-2">{v}</dd>
                </div>
              ))}
            </dl>
            <div className="border-t border-slate-100 p-5">
              <Button href={site.nostroyUrl} external variant="outline" className="w-full">
                Проверить в реестре
                <Icon name="ExternalLink" className="h-4 w-4" />
              </Button>
            </div>
          </Card>
        </div>
      </Section>

      {/* Как проверить — 3 шага */}
      <Section tone="muted">
        <SectionHeading
          eyebrow="Инструкция"
          title="Как проверить компанию в реестре"
          description="Любой заказчик может самостоятельно убедиться в статусе члена СРО."
        />
        <div className="mt-12 grid gap-5 md:grid-cols-3">
          {steps.map((s, i) => (
            <Card key={s.title} className="relative p-6">
              <span className="absolute right-5 top-5 font-display text-3xl font-extrabold text-slate-100">
                {i + 1}
              </span>
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gold-100 text-gold-700">
                <Icon name={s.icon} className="h-6 w-6" />
              </span>
              <h3 className="mt-4 text-lg font-bold text-navy-900">{s.title}</h3>
              <p className="mt-2 text-[0.95rem] leading-relaxed text-slate-600">{s.text}</p>
            </Card>
          ))}
        </div>
      </Section>

      <Cta
        title="Нужна выписка из реестра?"
        text="Поможем получить актуальную выписку о членстве и подтвердить статус для заказчика или тендера."
      />
    </>
  );
}
