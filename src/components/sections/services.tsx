import Link from "next/link";
import { Section, SectionHeading } from "@/components/ui/section";
import { Icon, type IconName } from "@/lib/icons";
import { services } from "@/lib/site";
import { cn } from "@/lib/utils";

export function Services() {
  return (
    <Section tone="white">
      <SectionHeading
        eyebrow="Услуги"
        title="Полный спектр услуг саморегулирования"
        description="От первого вступления до сопровождения действующих членов СРО."
      />
      <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {services.map((s) => (
          <Link
            key={s.slug}
            href={s.href}
            className={cn(
              "group relative flex flex-col overflow-hidden rounded-2xl border border-slate-200/80 bg-white p-6 shadow-soft",
              "transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)] hover:-translate-y-1 hover:border-gold-200 hover:shadow-lift",
            )}
          >
            <span className="absolute right-5 top-5 text-slate-300 transition-all duration-300 group-hover:translate-x-0.5 group-hover:text-gold-500">
              <Icon name="ArrowUpRight" className="h-5 w-5" />
            </span>
            <span className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-navy-800 text-gold-400 transition-colors group-hover:bg-navy-900">
              <Icon name={s.icon as IconName} className="h-7 w-7" />
            </span>
            <h3 className="mt-5 text-lg font-bold text-navy-900">{s.title}</h3>
            <p className="mt-2 text-[0.95rem] leading-relaxed text-slate-600">{s.text}</p>
          </Link>
        ))}
      </div>
    </Section>
  );
}
