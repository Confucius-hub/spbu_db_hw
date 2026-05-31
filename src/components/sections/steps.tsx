import { Section, SectionHeading } from "@/components/ui/section";
import { Button } from "@/components/ui/button";
import { CallbackButton } from "@/components/forms/callback-modal";
import { joinSteps } from "@/lib/site";

export function Steps() {
  return (
    <Section tone="navy" id="steps" className="relative overflow-hidden">
      <div
        className="absolute -right-32 top-1/2 h-96 w-96 -translate-y-1/2 rounded-full bg-gold-600/10 blur-3xl"
        aria-hidden
      />
      <div className="relative">
        <SectionHeading
          tone="dark"
          eyebrow="Как вступить"
          title="Пять шагов до членства в СРО"
          description="Прозрачный процесс с фиксированными сроками. Большую часть работы берём на себя."
        />

        <ol className="mt-14 grid gap-8 sm:grid-cols-2 lg:grid-cols-5">
          {joinSteps.map((step, i) => (
            <li key={i} className="relative">
              <div className="flex items-center gap-3">
                <span className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gold-500 font-display text-lg font-extrabold text-navy-950">
                  {i + 1}
                </span>
                {i < joinSteps.length - 1 && (
                  <span className="hidden h-px flex-1 bg-gradient-to-r from-gold-500/60 to-transparent lg:block" />
                )}
              </div>
              <h3 className="mt-4 text-base font-bold text-white">{step.title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-slate-300">{step.text}</p>
            </li>
          ))}
        </ol>

        <div className="mt-12 flex flex-wrap justify-center gap-3">
          <Button href="/membership" variant="gold" size="lg">
            Оставить заявку на вступление
          </Button>
          <CallbackButton variant="white" />
        </div>
      </div>
    </Section>
  );
}
