import { Plus } from "lucide-react";

/**
 * Accessible FAQ using native <details>/<summary> — no JS needed,
 * works without hydration and is fully keyboard-operable.
 */
export function Faq({ items }: { items: { q: string; a: string }[] }) {
  return (
    <div className="flex flex-col gap-3">
      {items.map((item, i) => (
        <details
          key={i}
          className="group rounded-2xl border border-line bg-white px-6 py-5 transition-colors open:border-line-strong"
        >
          <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-lg font-semibold text-ink [&::-webkit-details-marker]:hidden">
            {item.q}
            <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-accent-soft text-accent-strong transition-transform duration-300 group-open:rotate-45">
              <Plus className="h-4 w-4" aria-hidden />
            </span>
          </summary>
          <p className="mt-4 max-w-2xl text-[15px] leading-relaxed text-muted">
            {item.a}
          </p>
        </details>
      ))}
    </div>
  );
}
