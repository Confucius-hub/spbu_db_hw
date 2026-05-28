import type { CalculatorInput } from "./validation";

/**
 * Расчёт ориентировочной стоимости вступления в СРО строителей.
 * Взносы в компенсационные фонды — по уровням ответственности
 * (ст. 55.16 Градостроительного кодекса РФ).
 */

export type Level = { level: number; max: number; label: string; fee: number };

// КФ возмещения вреда (КФ ВВ) — обязателен для всех
export const VV_LEVELS: Level[] = [
  { level: 1, max: 60_000_000, label: "до 60 млн ₽", fee: 100_000 },
  { level: 2, max: 500_000_000, label: "до 500 млн ₽", fee: 500_000 },
  { level: 3, max: 3_000_000_000, label: "до 3 млрд ₽", fee: 1_500_000 },
  { level: 4, max: 10_000_000_000, label: "до 10 млрд ₽", fee: 2_000_000 },
  { level: 5, max: Infinity, label: "10 млрд ₽ и более", fee: 5_000_000 },
];

// КФ обеспечения договорных обязательств (КФ ОДО) — для работы по конкурсам/контрактам
export const ODO_LEVELS: Level[] = [
  { level: 1, max: 60_000_000, label: "до 60 млн ₽", fee: 200_000 },
  { level: 2, max: 500_000_000, label: "до 500 млн ₽", fee: 2_500_000 },
  { level: 3, max: 3_000_000_000, label: "до 3 млрд ₽", fee: 4_500_000 },
  { level: 4, max: 10_000_000_000, label: "до 10 млрд ₽", fee: 7_000_000 },
  { level: 5, max: Infinity, label: "10 млрд ₽ и более", fee: 25_000_000 },
];

const ENTRY_FEE = 5_000; // вступительный взнос (ориентировочно)
const MEMBERSHIP_FEE_YEAR = 60_000; // членский взнос в год (ориентировочно)
const NRS_FEE_PER_SPECIALIST = 25_000; // внесение специалиста в НРС (услуга)
const MIN_SPECIALISTS = 2;

function pickLevel(levels: Level[], amount: number): Level {
  return levels.find((l) => amount <= l.max) ?? levels[levels.length - 1];
}

export type CalcLine = {
  label: string;
  amount: number;
  note?: string;
  recurring?: boolean;
};

export type CalcResult = {
  vvLevel: number;
  vvLevelLabel: string;
  odoLevel: number | null;
  oneTimeTotal: number; // разовые платежи при вступлении
  yearlyTotal: number; // ежегодные платежи
  nrsNeeded: number;
  lines: CalcLine[];
};

export function computeCalculator(input: CalculatorInput): CalcResult {
  const vv = pickLevel(VV_LEVELS, input.contractAmount);
  const lines: CalcLine[] = [];

  lines.push({
    label: `Взнос в КФ возмещения вреда (${vv.level}-й уровень)`,
    amount: vv.fee,
    note: vv.label,
  });

  let odo: Level | null = null;
  if (input.needsContractFund) {
    odo = pickLevel(ODO_LEVELS, input.contractFundAmount || input.contractAmount);
    lines.push({
      label: `Взнос в КФ договорных обязательств (${odo.level}-й уровень)`,
      amount: odo.fee,
      note: odo.label,
    });
  }

  if (input.needsOpo) {
    lines.push({
      label: "Допуск на особо опасные объекты (ОПО)",
      amount: 0,
      note: "Дополнительные требования к специалистам, без отдельного взноса",
    });
  }

  lines.push({ label: "Вступительный взнос", amount: ENTRY_FEE });

  const nrsNeeded = Math.max(0, MIN_SPECIALISTS - input.specialists);
  if (nrsNeeded > 0) {
    lines.push({
      label: `Внесение специалистов в НРС (${nrsNeeded})`,
      amount: nrsNeeded * NRS_FEE_PER_SPECIALIST,
      note: `Нужно минимум ${MIN_SPECIALISTS} специалиста, у вас ${input.specialists}`,
    });
  }

  lines.push({
    label: "Членский взнос",
    amount: MEMBERSHIP_FEE_YEAR,
    recurring: true,
    note: "в год",
  });

  const oneTimeTotal = lines
    .filter((l) => !l.recurring)
    .reduce((s, l) => s + l.amount, 0);
  const yearlyTotal = lines
    .filter((l) => l.recurring)
    .reduce((s, l) => s + l.amount, 0);

  return {
    vvLevel: vv.level,
    vvLevelLabel: vv.label,
    odoLevel: odo?.level ?? null,
    oneTimeTotal,
    yearlyTotal,
    nrsNeeded,
    lines,
  };
}
