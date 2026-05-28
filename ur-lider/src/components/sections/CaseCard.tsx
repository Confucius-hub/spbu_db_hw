import { Clock } from "lucide-react";
import type { CaseResult } from "@/lib/cases";

export function CaseCard({ item }: { item: CaseResult }) {
  return (
    <article className="flex h-full flex-col rounded-2xl border border-line bg-white p-7 transition-shadow duration-300 hover:shadow-[var(--shadow-card)]">
      <span className="text-[12px] font-semibold uppercase tracking-[0.14em] text-accent-strong">
        {item.area}
      </span>

      <div className="mt-5 flex items-baseline gap-2">
        <span className="font-serif text-3xl font-semibold text-ink">
          {item.metric}
        </span>
        <span className="text-sm text-muted">{item.metricLabel}</span>
      </div>

      <h3 className="mt-4 text-lg leading-snug text-ink">{item.title}</h3>
      <p className="mt-2.5 flex-1 text-[15px] leading-relaxed text-muted">
        {item.result}
      </p>

      <div className="mt-6 flex items-center gap-2 border-t border-line pt-4 text-[13px] text-faint">
        <Clock className="h-4 w-4" aria-hidden />
        Срок: {item.duration}
      </div>
    </article>
  );
}
