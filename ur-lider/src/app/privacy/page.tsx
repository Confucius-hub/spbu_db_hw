import type { Metadata } from "next";
import { PageHeader } from "@/components/ui/PageHeader";
import { Section } from "@/components/ui/Section";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Политика конфиденциальности",
  robots: { index: false, follow: true },
};

export default function PrivacyPage() {
  return (
    <>
      <PageHeader
        title="Политика конфиденциальности"
        crumbs={[{ label: "Главная", href: "/" }, { label: "Политика конфиденциальности" }]}
      />
      <Section tone="paper">
        <div className="max-w-3xl space-y-6 text-[16px] leading-relaxed text-graphite">
          <p>
            Настоящая политика описывает порядок обработки персональных данных,
            которые вы передаёте {site.legalName} через формы обратной связи на
            сайте {site.url}.
          </p>
          <div className="space-y-3">
            <h2 className="text-xl text-ink">Какие данные мы собираем</h2>
            <p>
              Имя, номер телефона, адрес электронной почты и текст обращения —
              только то, что вы указываете добровольно в форме заявки.
            </p>
          </div>
          <div className="space-y-3">
            <h2 className="text-xl text-ink">Цели обработки</h2>
            <p>
              Данные используются исключительно для связи с вами по вашему
              обращению и оказания юридических услуг. Мы не передаём их третьим
              лицам и не используем для рассылок без согласия.
            </p>
          </div>
          <div className="space-y-3">
            <h2 className="text-xl text-ink">Хранение и защита</h2>
            <p>
              Данные хранятся в течение срока, необходимого для обработки
              обращения, и защищены организационными и техническими мерами.
            </p>
          </div>
          <div className="space-y-3">
            <h2 className="text-xl text-ink">Ваши права</h2>
            <p>
              Вы вправе запросить удаление своих данных, направив обращение на{" "}
              <a href={`mailto:${site.email}`} className="text-accent-strong underline">
                {site.email}
              </a>
              .
            </p>
          </div>
        </div>
      </Section>
    </>
  );
}
