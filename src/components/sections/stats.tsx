import { Section } from "@/components/ui/section";
import { stats } from "@/lib/site";

export function Stats() {
  return (
    <Section tone="navy" className="relative overflow-hidden">
      <div className="absolute inset-0 bg-grid opacity-40" aria-hidden />
      <div className="relative">
        <div className="mx-auto max-w-2xl text-center">
          <div className="mb-3 inline-flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.14em] text-gold-400">
            <span className="h-px w-6 bg-gold-400/70" />
            Мы в цифрах
            <span className="h-px w-6 bg-gold-400/70" />
          </div>
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            15 лет надёжной работы в цифрах
          </h2>
        </div>

        <dl className="mt-12 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-3 lg:grid-cols-5">
          {stats.map((s) => (
            <div key={s.label} className="text-center">
              <dt className="font-display text-4xl font-extrabold text-gold-gradient lg:text-5xl">
                {s.value}
              </dt>
              <dd className="mt-2 text-sm font-medium text-slate-200">{s.label}</dd>
              <dd className="mt-0.5 text-xs text-slate-400">{s.sub}</dd>
            </div>
          ))}
        </dl>
      </div>
    </Section>
  );
}
