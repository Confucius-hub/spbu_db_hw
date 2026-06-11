import { Section, SectionHeading } from "@/components/ui/section";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Icon } from "@/lib/icons";
import { formatCurrency } from "@/lib/utils";

/**
 * Страхование гражданской ответственности членов СРО.
 * Градация минимальных страховых сумм по уровням ответственности
 * (ст. 55.16 ГрК РФ). Структура — по образцу профильных СРО СПб
 * (референс пользователя: sro-ism.ru → Страхование).
 *
 * ВНИМАНИЕ: значения сумм редактируются в одном месте — массив ниже.
 * Если внутренними документами СССС утверждены иные суммы — поменяйте здесь.
 */
const INSURANCE_VV = [
  { level: 1, label: "Первый уровень ответственности", sum: 4_000_000 },
  { level: 2, label: "Второй уровень ответственности", sum: 15_000_000 },
  { level: 3, label: "Третий уровень ответственности", sum: 100_000_000 },
  { level: 4, label: "Четвёртый уровень ответственности", sum: 200_000_000 },
  { level: 5, label: "Пятый уровень ответственности", sum: 200_000_000 },
] as const;

export function MembershipInsurance() {
  return (
    <Section tone="muted" id="insurance">
      <SectionHeading
        align="left"
        eyebrow="Страхование"
        title="Страхование ответственности"
        description="Размер страховой суммы по договору страхования гражданской ответственности члена Ассоциации зависит от уровня ответственности по ст. 55.16 Градостроительного кодекса РФ."
      />

      <div className="mt-8 grid items-start gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        {/* Градация страховых сумм (ВВ) */}
        <Card className="overflow-hidden">
          <div className="border-b border-slate-100 p-5">
            <h3 className="font-bold text-navy-900">
              Страхование риска гражданской ответственности (ВВ)
            </h3>
            <p className="text-sm text-slate-500">
              Минимальная страховая сумма на срок действия договора страхования
              и ретроактивного периода
            </p>
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500">
                <th className="px-5 py-3 font-semibold">Уровень ответственности</th>
                <th className="px-5 py-3 text-right font-semibold">Страховая сумма, не менее</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {INSURANCE_VV.map((row) => (
                <tr key={row.level} className="transition-colors hover:bg-gold-50/50">
                  <td className="px-5 py-3.5">
                    <span className="mr-3 inline-flex h-7 w-7 items-center justify-center rounded-lg bg-navy-800 font-display text-xs font-extrabold text-gold-400">
                      {row.level}
                    </span>
                    <span className="font-medium text-navy-900">{row.label}</span>
                  </td>
                  <td className="px-5 py-3.5 text-right font-semibold text-navy-900">
                    {formatCurrency(row.sum)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="border-t border-slate-100 px-5 py-3 text-xs text-slate-500">
            Уровни ответственности соответствуют ст. 55.16 ГрК РФ (по стоимости работ по одному
            договору подряда).
          </p>
        </Card>

        {/* ОДО + запрос условий */}
        <div className="space-y-5">
          <Card className="p-6">
            <div className="flex items-start gap-3">
              <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-50 text-navy-700">
                <Icon name="FileCheck2" className="h-5 w-5" />
              </span>
              <div>
                <p className="font-semibold text-navy-900">
                  Страхование по договорам (ОДО)
                </p>
                <p className="mt-1.5 text-sm leading-relaxed text-slate-600">
                  По договорам строительного подряда, заключённым конкурентными способами,
                  действует комбинированное страхование риска ответственности — отдельно по
                  каждому такому договору. Страховая сумма определяется условиями договора
                  страхования.
                </p>
              </div>
            </div>
          </Card>

          <Card className="bg-navy-900 p-6 text-white">
            <Icon name="ShieldCheck" className="h-8 w-8 text-gold-400" />
            <p className="mt-3 font-semibold text-white">
              Полные требования к страхованию
            </p>
            <p className="mt-1.5 text-sm text-slate-300">
              Пришлём требования к договору страхования, перечень аккредитованных страховых
              организаций и порядок оформления.
            </p>
            <Button href="/contacts" variant="gold" className="mt-5 w-full">
              <Icon name="Mail" className="h-4 w-4" />
              Запросить условия
            </Button>
          </Card>
        </div>
      </div>
    </Section>
  );
}
