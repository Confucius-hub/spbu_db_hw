import { Section, SectionHeading } from "@/components/ui/section";
import { Card } from "@/components/ui/card";
import { Icon } from "@/lib/icons";
import { formatCurrency } from "@/lib/utils";

/**
 * Реальные данные с страницы «Членские взносы» исходного сайта.
 * Содержание не выдумано.
 */
const ENTRY = 5_000;
const MONTHLY = 10_000;
const QUARTER = MONTHLY * 3;

export function MembershipFees() {
  return (
    <Section tone="white" id="fees">
      <SectionHeading
        align="left"
        eyebrow="Платежи"
        title="Членские взносы"
        description="Прозрачная и фиксированная структура: вступительный взнос и регулярные членские взносы. Никаких скрытых платежей."
      />

      <div className="mt-8 grid gap-5 md:grid-cols-3">
        {/* Вступительный взнос */}
        <Card className="overflow-hidden">
          <div className="bg-navy-900 p-5 text-white">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/10 text-gold-400">
              <Icon name="BadgeCheck" className="h-5 w-5" />
            </span>
            <p className="mt-4 text-xs font-semibold uppercase tracking-wider text-gold-300">
              Вступительный взнос
            </p>
            <p className="mt-2 font-display text-3xl font-extrabold text-gold-gradient">
              {formatCurrency(ENTRY)}
            </p>
          </div>
          <div className="p-5 text-sm leading-relaxed text-slate-600">
            Единоразовый платёж при вступлении в Ассоциацию.
          </div>
        </Card>

        {/* Ежемесячный членский взнос */}
        <Card className="overflow-hidden md:col-span-2">
          <div className="bg-gradient-to-br from-gold-700 to-gold-900 p-5 text-white">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/15 text-white">
              <Icon name="Calculator" className="h-5 w-5" />
            </span>
            <p className="mt-4 text-xs font-semibold uppercase tracking-wider text-white/80">
              Регулярный ежемесячный членский взнос
            </p>
            <p className="mt-2 font-display text-3xl font-extrabold text-white">
              {formatCurrency(MONTHLY)} <span className="text-base font-medium opacity-80">/ месяц</span>
            </p>
          </div>
          <div className="p-5 text-sm leading-relaxed text-slate-600">
            Оплата осуществляется <span className="font-semibold text-navy-900">ежеквартально</span>, в течение
            10 рабочих дней с начала очередного квартала, в размере взноса за три следующих месяца.
            <div className="mt-3 inline-flex items-center gap-2 rounded-xl bg-gold-50 px-3 py-2 ring-1 ring-gold-200">
              <Icon name="Receipt" className="h-4 w-4 text-gold-700" />
              <span className="text-sm">
                <span className="font-semibold text-navy-900">Квартальный платёж:</span>{" "}
                {formatCurrency(QUARTER)}
              </span>
            </div>
          </div>
        </Card>
      </div>

      {/* Дополнительная информация */}
      <div className="mt-6 grid gap-4 rounded-2xl border border-slate-200 bg-white p-5 sm:grid-cols-3 sm:p-6">
        <div className="flex items-start gap-3">
          <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
            <Icon name="Check" className="h-4 w-4" strokeWidth={2.5} />
          </span>
          <div>
            <p className="text-sm font-semibold text-navy-900">Без скрытых платежей</p>
            <p className="mt-0.5 text-xs text-slate-500">Все суммы фиксированы и закреплены документально</p>
          </div>
        </div>
        <div className="flex items-start gap-3">
          <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
            <Icon name="Check" className="h-4 w-4" strokeWidth={2.5} />
          </span>
          <div>
            <p className="text-sm font-semibold text-navy-900">Прозрачные сроки</p>
            <p className="mt-0.5 text-xs text-slate-500">10 рабочих дней с начала квартала</p>
          </div>
        </div>
        <div className="flex items-start gap-3">
          <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
            <Icon name="Check" className="h-4 w-4" strokeWidth={2.5} />
          </span>
          <div>
            <p className="text-sm font-semibold text-navy-900">Поквартальная оплата</p>
            <p className="mt-0.5 text-xs text-slate-500">Не нужно платить каждый месяц</p>
          </div>
        </div>
      </div>
    </Section>
  );
}
