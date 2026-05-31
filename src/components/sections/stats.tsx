import { Section } from "@/components/ui/section";
import { Photo } from "@/components/ui/photo";
import { stats, media } from "@/lib/site";

export function Stats() {
  return (
    <Section tone="navy" className="relative overflow-hidden">
      {/* Фоновое фото с сильным затемнением — добавляет визуальной фактуры */}
      <Photo
        src={media.construction}
        className="absolute inset-0"
        imgClassName="opacity-15 object-cover"
      />
      <div className="absolute inset-0 bg-gradient-to-b from-navy-900 via-navy-900/92 to-navy-900" aria-hidden />
      <div className="absolute inset-0 bg-grid opacity-25" aria-hidden />
      <div className="relative">
        <div className="mx-auto max-w-2xl text-center">
          <div className="mb-3 inline-flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.14em] text-gold-400">
            <span className="h-px w-6 bg-gold-400/70" />
            Коротко о главном
            <span className="h-px w-6 bg-gold-400/70" />
          </div>
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Надёжность, подтверждённая статусом
          </h2>
        </div>

        <dl className="mx-auto mt-12 grid max-w-5xl grid-cols-2 gap-x-6 gap-y-10 lg:grid-cols-4">
          {stats.map((s) => (
            <div key={s.label} className="px-2 text-center">
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
