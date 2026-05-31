"use client";

import { useMemo, useState } from "react";
import { computeCalculator } from "@/lib/calculator";
import { formatCurrency, cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { LeadForm } from "@/components/forms/lead-form";
import { Icon } from "@/lib/icons";

const fieldCls =
  "w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-[0.95rem] font-medium text-navy-900 transition-colors focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-200";

const labelCls = "mb-1.5 block text-sm font-medium text-slate-600";

export function Calculator({ variant = "compact" }: { variant?: "compact" | "full" }) {
  const [amount, setAmount] = useState(10_000_000);
  const [needsOpo, setNeedsOpo] = useState(false);
  const [specialists, setSpecialists] = useState(2);
  const [needsContractFund, setNeedsContractFund] = useState(false);
  const [fundAmount, setFundAmount] = useState(10_000_000);
  const [modalOpen, setModalOpen] = useState(false);

  const result = useMemo(
    () =>
      computeCalculator({
        contractAmount: amount,
        needsOpo,
        specialists,
        needsContractFund,
        contractFundAmount: fundAmount,
      }),
    [amount, needsOpo, specialists, needsContractFund, fundAmount],
  );

  const payload = {
    contractAmount: amount,
    needsOpo,
    specialists,
    needsContractFund,
    contractFundAmount: needsContractFund ? fundAmount : 0,
    oneTimeTotal: result.oneTimeTotal,
    yearlyTotal: result.yearlyTotal,
    vvLevel: result.vvLevel,
  };

  const full = variant === "full";

  return (
    <div
      className={cn(
        "rounded-3xl bg-white p-6 shadow-lift sm:p-7",
        full ? "border border-slate-200" : "",
      )}
    >
      <div className="flex items-center gap-3">
        <span className="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-gold-100 text-gold-700">
          <Icon name="Calculator" className="h-6 w-6" />
        </span>
        <div>
          <h3 className="text-lg font-bold text-navy-900">Калькулятор стоимости</h3>
          <p className="text-sm text-slate-500">Рассчитайте взносы в СРО онлайн</p>
        </div>
      </div>

      <div className="mt-6 space-y-4">
        <div>
          <label className={labelCls} htmlFor="calc-amount">
            Сумма по одному договору подряда
          </label>
          <div className="relative">
            <input
              id="calc-amount"
              inputMode="numeric"
              value={amount ? amount.toLocaleString("ru-RU") : ""}
              onChange={(e) => setAmount(Number(e.target.value.replace(/\D/g, "")) || 0)}
              className={cn(fieldCls, "pr-9")}
              placeholder="10 000 000"
            />
            <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
              ₽
            </span>
          </div>
        </div>

        <div className={cn(full ? "grid gap-4 sm:grid-cols-2" : "space-y-4")}>
          <div>
            <label className={labelCls} htmlFor="calc-opo">
              Допуск на особо опасные объекты
            </label>
            <select
              id="calc-opo"
              value={needsOpo ? "yes" : "no"}
              onChange={(e) => setNeedsOpo(e.target.value === "yes")}
              className={fieldCls}
            >
              <option value="no">Не требуется</option>
              <option value="yes">Требуется</option>
            </select>
          </div>

          <div>
            <label className={labelCls} htmlFor="calc-spec">
              Специалистов в НРС
            </label>
            <input
              id="calc-spec"
              inputMode="numeric"
              value={specialists}
              onChange={(e) =>
                setSpecialists(Math.min(999, Number(e.target.value.replace(/\D/g, "")) || 0))
              }
              className={fieldCls}
              placeholder="2"
            />
          </div>
        </div>

        {full && (
          <div className="rounded-xl border border-slate-200 p-4">
            <label className="flex cursor-pointer items-start gap-3">
              <input
                type="checkbox"
                checked={needsContractFund}
                onChange={(e) => setNeedsContractFund(e.target.checked)}
                className="mt-1 h-4 w-4 accent-gold-500"
              />
              <span className="text-sm text-slate-600">
                <span className="font-semibold text-navy-900">
                  Участие в конкурсах и закупках
                </span>
                <br />
                Нужен фонд обеспечения договорных обязательств (КФ ОДО)
              </span>
            </label>
            {needsContractFund && (
              <div className="mt-3">
                <label className={labelCls} htmlFor="calc-fund">
                  Совокупный объём обязательств по контрактам
                </label>
                <div className="relative">
                  <input
                    id="calc-fund"
                    inputMode="numeric"
                    value={fundAmount ? fundAmount.toLocaleString("ru-RU") : ""}
                    onChange={(e) =>
                      setFundAmount(Number(e.target.value.replace(/\D/g, "")) || 0)
                    }
                    className={cn(fieldCls, "pr-9")}
                  />
                  <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
                    ₽
                  </span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Результат */}
      <div className="mt-6 rounded-2xl bg-navy-900 p-5 text-white">
        <div className="flex items-end justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-wider text-slate-400">
              Разовый платёж при вступлении
            </p>
            <p className="mt-1 font-display text-3xl font-extrabold text-white">
              {formatCurrency(result.oneTimeTotal)}
            </p>
          </div>
          <span className="rounded-lg bg-white/10 px-2.5 py-1 text-xs font-semibold text-gold-300">
            {result.vvLevel}-й уровень
          </span>
        </div>
        <p className="mt-2 text-sm text-slate-300">
          + членский взнос {formatCurrency(result.yearlyTotal)} / год
        </p>

        {full && (
          <ul className="mt-4 space-y-2 border-t border-white/10 pt-4 text-sm">
            {result.lines.map((line, i) => (
              <li key={i} className="flex items-start justify-between gap-3">
                <span className="text-slate-300">
                  {line.label}
                  {line.note && (
                    <span className="block text-xs text-slate-500">{line.note}</span>
                  )}
                </span>
                <span className="shrink-0 font-semibold text-white">
                  {line.amount > 0 ? formatCurrency(line.amount) : "—"}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <Button
        variant="gold"
        size="lg"
        className="mt-4 w-full"
        onClick={() => setModalOpen(true)}
      >
        Получить точный расчёт
        <Icon name="ArrowRight" className="h-4 w-4" />
      </Button>
      <p className="mt-2 text-center text-xs text-slate-400">
        Ориентировочный расчёт. Точную стоимость подтвердит менеджер.
      </p>

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Точный расчёт стоимости"
        description="Оставьте контакты — пришлём детальный расчёт и перечень документов."
      >
        <LeadForm
          type="CALCULATOR"
          source={`calculator-${variant}`}
          submitLabel="Получить расчёт"
          fields={["company"]}
          payload={payload}
        />
      </Modal>
    </div>
  );
}
