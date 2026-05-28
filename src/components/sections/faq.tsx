"use client";

import { useState } from "react";
import { Section, SectionHeading } from "@/components/ui/section";
import { Icon } from "@/lib/icons";
import { faq as defaultFaq } from "@/lib/site";
import { cn } from "@/lib/utils";

export function Faq({
  items = defaultFaq,
  withHeading = true,
}: {
  items?: readonly { q: string; a: string }[];
  withHeading?: boolean;
}) {
  const [open, setOpen] = useState<number | null>(0);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: items.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a },
    })),
  };

  return (
    <Section tone="white" id="faq" containerSize="narrow">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      {withHeading && (
        <SectionHeading
          eyebrow="Вопросы и ответы"
          title="Частые вопросы о вступлении в СРО"
        />
      )}
      <div className="mt-10 divide-y divide-slate-200 rounded-2xl border border-slate-200 bg-white">
        {items.map((f, i) => {
          const isOpen = open === i;
          return (
            <div key={i}>
              <button
                type="button"
                onClick={() => setOpen(isOpen ? null : i)}
                className="flex w-full items-center justify-between gap-4 px-5 py-5 text-left"
                aria-expanded={isOpen}
              >
                <span className="font-semibold text-navy-900">{f.q}</span>
                <span
                  className={cn(
                    "inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-slate-100 text-navy-700 transition-transform duration-300",
                    isOpen && "rotate-180 bg-gold-100 text-gold-700",
                  )}
                >
                  <Icon name="ChevronDown" className="h-4 w-4" strokeWidth={2} />
                </span>
              </button>
              <div
                className={cn(
                  "grid transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]",
                  isOpen ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0",
                )}
              >
                <div className="overflow-hidden">
                  <p className="px-5 pb-5 leading-relaxed text-slate-600">{f.a}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </Section>
  );
}
