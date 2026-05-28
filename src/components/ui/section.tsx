import { cn } from "@/lib/utils";
import { Container } from "./container";

type Tone = "white" | "muted" | "navy";

const tones: Record<Tone, string> = {
  white: "bg-white",
  muted: "bg-slate-50",
  navy: "bg-navy-900 text-slate-200",
};

/** Секция со стандартным вертикальным ритмом и фоновым тоном. */
export function Section({
  children,
  className,
  tone = "white",
  id,
  containerSize = "default",
  contained = true,
}: {
  children: React.ReactNode;
  className?: string;
  tone?: Tone;
  id?: string;
  containerSize?: "default" | "narrow" | "wide";
  contained?: boolean;
}) {
  return (
    <section id={id} className={cn("py-16 sm:py-20 lg:py-24", tones[tone], className)}>
      {contained ? <Container size={containerSize}>{children}</Container> : children}
    </section>
  );
}

/** Заголовок секции: надзаголовок + h2 + описание. */
export function SectionHeading({
  eyebrow,
  title,
  description,
  align = "center",
  tone = "light",
  className,
}: {
  eyebrow?: string;
  title: React.ReactNode;
  description?: React.ReactNode;
  align?: "center" | "left";
  tone?: "light" | "dark";
  className?: string;
}) {
  return (
    <div
      className={cn(
        "max-w-2xl",
        align === "center" && "mx-auto text-center",
        className,
      )}
    >
      {eyebrow && (
        <div
          className={cn(
            "mb-3 inline-flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.14em]",
            tone === "light" ? "text-gold-700" : "text-gold-400",
          )}
        >
          <span className="h-px w-6 bg-gold-400/70" />
          {eyebrow}
        </div>
      )}
      <h2
        className={cn(
          "text-3xl sm:text-4xl lg:text-[2.6rem] lg:leading-[1.1]",
          tone === "dark" && "text-white",
        )}
      >
        {title}
      </h2>
      {description && (
        <p
          className={cn(
            "mt-4 text-lg leading-relaxed",
            tone === "light" ? "text-slate-600" : "text-slate-300",
          )}
        >
          {description}
        </p>
      )}
    </div>
  );
}
