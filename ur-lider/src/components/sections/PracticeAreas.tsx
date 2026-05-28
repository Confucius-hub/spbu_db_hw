import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { Section } from "@/components/ui/Section";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Reveal } from "@/components/ui/Reveal";
import { PracticeIcon } from "@/components/ui/PracticeIcon";
import { practices } from "@/lib/practices";
import { cn } from "@/lib/utils";

export function PracticeAreas() {
  return (
    <Section tone="paper" id="practices">
      <SectionHeading
        eyebrow="Допуски и услуги СРО"
        title="Допуск СРО для любого вида работ"
        subtitle="Строители, проектировщики, изыскатели, специалисты НРС и выписки — оформляем под ключ в надёжных СРО Санкт-Петербурга."
      />

      <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {practices.map((p, i) => (
          <Reveal key={p.slug} delay={(i % 3) * 70}>
            <Link
              href={`/practices/${p.slug}`}
              className={cn(
                "group flex h-full flex-col rounded-2xl border border-line bg-white p-7",
                "transition-[transform,box-shadow,border-color] duration-300 ease-out",
                "hover:-translate-y-1 hover:border-line-strong hover:shadow-[var(--shadow-lift)]",
              )}
            >
              <div className="flex items-center justify-between">
                <span className="grid h-12 w-12 place-items-center rounded-xl bg-accent-soft text-accent-strong transition-colors group-hover:bg-accent group-hover:text-white">
                  <PracticeIcon name={p.icon} className="h-6 w-6" />
                </span>
                <ArrowUpRight className="h-5 w-5 text-faint transition-all duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:text-accent" />
              </div>
              <h3 className="mt-6 text-xl text-ink">{p.title}</h3>
              <p className="mt-2.5 flex-1 text-[15px] leading-relaxed text-muted">
                {p.short}
              </p>
              <span className="mt-5 text-[13px] font-semibold uppercase tracking-wider text-accent-strong">
                {p.audience}
              </span>
            </Link>
          </Reveal>
        ))}
      </div>
    </Section>
  );
}
