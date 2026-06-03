"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Icon } from "@/lib/icons";
import { cn } from "@/lib/utils";
import { accounts, legalEntity } from "@/lib/requisites";

function CopyRow({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  const [copied, setCopied] = useState(false);
  async function copy() {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    } catch {
      /* noop */
    }
  }
  return (
    <div className="group grid items-start gap-2 px-5 py-3.5 transition-colors hover:bg-gold-50/40 sm:grid-cols-[10rem_1fr_auto] sm:gap-4">
      <dt className="text-sm text-slate-500">{label}</dt>
      <dd
        className={cn(
          "break-all text-navy-900",
          mono ? "font-mono text-[0.92rem]" : "font-medium",
        )}
      >
        {value}
      </dd>
      <button
        type="button"
        onClick={copy}
        title="Скопировать"
        className="hidden h-7 w-7 shrink-0 items-center justify-center rounded-md text-slate-400 transition-colors hover:bg-slate-100 hover:text-navy-700 sm:inline-flex"
        aria-label={`Скопировать ${label}`}
      >
        <Icon name={copied ? "Check" : "ExternalLink"} className="h-3.5 w-3.5" strokeWidth={2} />
      </button>
    </div>
  );
}

function AccountCard({ acc }: { acc: (typeof accounts)[number] }) {
  const accentByKind: Record<(typeof accounts)[number]["kind"], string> = {
    main: "from-navy-800 to-navy-900",
    "kf-vv": "from-gold-700 to-gold-900",
    "kf-odo": "from-navy-700 to-navy-800",
  };
  return (
    <Card className="overflow-hidden">
      <div className={cn("bg-gradient-to-br p-5 text-white", accentByKind[acc.kind])}>
        <p className="text-xs font-semibold uppercase tracking-wider text-gold-300">
          Банковский счёт
        </p>
        <p className="mt-1.5 text-base font-bold leading-snug">{acc.title}</p>
      </div>
      <dl className="divide-y divide-slate-100">
        <CopyRow label="Номер счёта" value={acc.account} mono />
        <CopyRow label="Банк" value={acc.bank} />
        <CopyRow label="БИК" value={acc.bic} mono />
        <CopyRow label="Корр. счёт" value={acc.ks} mono />
      </dl>
    </Card>
  );
}

export function RequisitesFull() {
  return (
    <div className="space-y-8">
      {/* Юр. лицо */}
      <Card className="overflow-hidden">
        <div className="border-b border-slate-100 bg-slate-50/60 px-5 py-3">
          <p className="text-sm font-semibold text-navy-900">Юридическое лицо</p>
        </div>
        <dl className="divide-y divide-slate-100">
          <CopyRow label="Полное наименование" value={legalEntity.name} />
          <CopyRow label="Сокращённое" value={legalEntity.shortName} />
          <CopyRow label="ИНН" value={legalEntity.inn} mono />
          <CopyRow label="ОГРН" value={legalEntity.ogrn} mono />
          <CopyRow label="КПП" value={legalEntity.kpp} mono />
          <CopyRow label="Юр. адрес" value={legalEntity.address} />
          <CopyRow label="Реестр НОСТРОЙ" value={`${legalEntity.registry} от ${legalEntity.registryDate}`} mono />
          <CopyRow label="Телефон" value={legalEntity.phone} />
          <CopyRow label="E-mail" value={legalEntity.email} />
        </dl>
      </Card>

      {/* Банковские счета */}
      <div>
        <h3 className="mb-4 inline-flex items-center gap-3 text-sm font-semibold uppercase tracking-[0.14em] text-gold-700">
          <span className="h-px w-6 bg-gold-400/70" />
          Банковские счета
          <span className="text-xs font-normal normal-case tracking-normal text-slate-400">
            · {accounts.length}
          </span>
        </h3>
        <div className="grid gap-5 md:grid-cols-2">
          {accounts.map((a, i) => (
            <AccountCard key={i} acc={a} />
          ))}
        </div>
      </div>
    </div>
  );
}
