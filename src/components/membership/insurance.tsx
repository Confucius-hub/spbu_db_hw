import { Section, SectionHeading } from "@/components/ui/section";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Icon } from "@/lib/icons";

/**
 * Раздел «Страхование» — раздел существует на исходном сайте, но содержательная
 * часть на нём не опубликована. Здесь даём короткий блок с приглашением запросить
 * актуальные условия у менеджера. Содержание НЕ выдумано — отсылаем к контактам.
 */
export function MembershipInsurance() {
  return (
    <Section tone="muted" id="insurance">
      <SectionHeading
        align="left"
        eyebrow="Страхование"
        title="Страхование ответственности"
        description="Информация об актуальных требованиях к страхованию ответственности членов СРО и условиях предоставляется по запросу."
      />
      <Card className="mt-8 overflow-hidden">
        <div className="grid items-stretch gap-0 md:grid-cols-[1fr_auto]">
          <div className="p-6 sm:p-7">
            <div className="flex items-start gap-3">
              <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-50 text-navy-700">
                <Icon name="ShieldCheck" className="h-5 w-5" />
              </span>
              <div>
                <p className="font-semibold text-navy-900">Актуальные условия — у вашего менеджера</p>
                <p className="mt-1 text-sm text-slate-600">
                  Свяжитесь с нами — пришлём перечень аккредитованных страховых организаций,
                  требования к страховым суммам и порядок оформления.
                </p>
              </div>
            </div>
          </div>
          <div className="flex items-center justify-end border-t border-slate-100 p-6 md:border-l md:border-t-0">
            <Button href="/contacts" variant="primary">
              <Icon name="Mail" className="h-4 w-4" />
              Запросить условия
            </Button>
          </div>
        </div>
      </Card>
    </Section>
  );
}
