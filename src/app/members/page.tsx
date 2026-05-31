import type { Metadata } from "next";
import { Section, SectionHeading } from "@/components/ui/section";
import { PageHeader } from "@/components/layout/page-header";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Cta } from "@/components/sections/cta";
import { Icon, type IconName } from "@/lib/icons";
import { site, media } from "@/lib/site";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Членам СРО",
  description:
    "Сервисы для действующих членов СРО: личный кабинет, реестр членов, уведомления о договорах, сопровождение проверок.",
  path: "/members",
});

const services: { icon: IconName; title: string; text: string }[] = [
  { icon: "LayoutDashboard", title: "Личный кабинет (скоро)", text: "Подача уведомлений, статусы заявок и доступ к документам онлайн." },
  { icon: "ClipboardList", title: "Уведомления о договорах", text: "Передача сведений о договорах и исках в срок (правило трёх дней)." },
  { icon: "Scale", title: "Сопровождение проверок", text: "Предварительный аудит документации и помощь при проверках." },
  { icon: "TrendingUp", title: "Повышение уровня", text: "Изменение уровня ответственности по компенсационному фонду." },
  { icon: "FileText", title: "Документы и формы", text: "Актуальные бланки, положения и выписки из реестра." },
  { icon: "Headset", title: "Поддержка членов", text: "Консультации по любым вопросам саморегулирования." },
];

export default function MembersPage() {
  return (
    <>
      <PageHeader
        eyebrow="Действующим членам"
        title="Сервисы для членов СРО"
        description="Всё для удобной работы в составе СРО: сопровождение, документы и поддержка по любым вопросам саморегулирования."
        breadcrumbs={[{ label: "Членам СРО" }]}
        image={media.office}
      >
        <div className="flex flex-wrap gap-3">
          <Button href="/contacts" variant="gold" size="lg">
            <Icon name="Headset" className="h-5 w-5" />
            Связаться с менеджером
          </Button>
          <Button href="/documents" variant="white" size="lg">
            Документы и формы
          </Button>
        </div>
      </PageHeader>

      <Section tone="white">
        <SectionHeading
          eyebrow="Возможности"
          title="Что доступно членам СРО «СССС»"
        />
        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((s) => (
            <Card key={s.title} hover className="p-6">
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gold-100 text-gold-700">
                <Icon name={s.icon} className="h-6 w-6" />
              </span>
              <h3 className="mt-4 text-lg font-bold text-navy-900">{s.title}</h3>
              <p className="mt-2 text-[0.95rem] leading-relaxed text-slate-600">{s.text}</p>
            </Card>
          ))}
        </div>
      </Section>

      {/* Личный кабинет — в разработке */}
      <Section tone="navy" id="cabinet">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full bg-white/10 px-3.5 py-1.5 text-xs font-semibold text-gold-300 ring-1 ring-white/15">
              <span className="h-1.5 w-1.5 rounded-full bg-gold-400" />
              Скоро · в разработке
            </span>
            <SectionHeading
              align="left"
              tone="dark"
              className="mt-4"
              eyebrow="Личный кабинет"
              title="Управление членством онлайн"
              description="Запускаем личный кабинет: подача уведомлений, статусы заявок и доступ к документам без визитов в офис. Пока эти задачи решает ваш персональный менеджер."
            />
            <div className="mt-7 flex flex-wrap gap-3">
              <Button href="/contacts" variant="gold" size="lg">
                Запросить доступ
              </Button>
              <Button href="/contacts" variant="white" size="lg">
                Связаться с менеджером
              </Button>
            </div>
          </div>
          <Card className="bg-white/5 p-8 ring-1 ring-white/10">
            <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-gold-300">
              Что будет доступно
            </p>
            <ul className="space-y-4">
              {[
                "Уведомления о договорах и исках в пару кликов",
                "История обращений и статусы заявок",
                "Напоминания о сроках уплаты взносов",
                "Доступ к выпискам и документам 24/7",
              ].map((t) => (
                <li key={t} className="flex items-start gap-3 text-slate-200">
                  <Icon name="CheckCircle2" className="mt-0.5 h-5 w-5 shrink-0 text-gold-400" />
                  {t}
                </li>
              ))}
            </ul>
          </Card>
        </div>
      </Section>

      {/* Реестр членов — тизер на отдельную страницу */}
      <Section tone="muted" id="registry">
        <Card className="mx-auto max-w-3xl p-8 text-center">
          <span className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-navy-800 text-gold-400">
            <Icon name="Landmark" className="h-7 w-7" />
          </span>
          <h2 className="mt-5 text-2xl font-bold text-navy-900">Реестр членов СРО</h2>
          <p className="mx-auto mt-3 max-w-xl text-slate-600">
            Сведения об Ассоциации и её членах внесены в единый реестр НОСТРОЙ. Регистрационный
            номер — {site.registryNumber}.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Button href="/members/registry" variant="primary">
              Подробнее о реестре
              <Icon name="ArrowRight" className="h-4 w-4" />
            </Button>
            <Button href={site.nostroyUrl} external variant="outline">
              Открыть реестр НОСТРОЙ
              <Icon name="ExternalLink" className="h-4 w-4" />
            </Button>
          </div>
        </Card>
      </Section>

      <Cta title="Нужна помощь по членству?" text="Персональный менеджер ответит на вопросы и поможет с документами и уведомлениями." />
    </>
  );
}
