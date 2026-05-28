import { cn } from "@/lib/utils";
import { Badge } from "./Badge";
import { Reveal } from "./Reveal";

export function SectionHeading({
  eyebrow,
  title,
  subtitle,
  align = "left",
  tone = "default",
  className,
}: {
  eyebrow?: string;
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  align?: "left" | "center";
  tone?: "default" | "onDark";
  className?: string;
}) {
  return (
    <div
      className={cn(
        "flex flex-col gap-4",
        align === "center" ? "items-center text-center" : "items-start",
        className,
      )}
    >
      {eyebrow && (
        <Reveal>
          <Badge tone={tone === "onDark" ? "onDark" : "default"}>{eyebrow}</Badge>
        </Reveal>
      )}
      <Reveal delay={60}>
        <h2
          className={cn(
            "max-w-3xl text-3xl leading-[1.12] sm:text-4xl lg:text-[2.75rem]",
            tone === "onDark" ? "text-white" : "text-ink",
            align === "center" && "mx-auto",
          )}
        >
          {title}
        </h2>
      </Reveal>
      {subtitle && (
        <Reveal delay={120}>
          <p
            className={cn(
              "max-w-2xl text-lg leading-relaxed",
              tone === "onDark" ? "text-white/70" : "text-muted",
              align === "center" && "mx-auto",
            )}
          >
            {subtitle}
          </p>
        </Reveal>
      )}
    </div>
  );
}
