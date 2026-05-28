import { cn } from "@/lib/utils";
import { Container } from "./Container";

type Tone = "paper" | "white" | "paper-2" | "ink";

const toneClass: Record<Tone, string> = {
  paper: "bg-paper text-graphite",
  white: "bg-white text-graphite",
  "paper-2": "bg-paper-2 text-graphite",
  ink: "bg-ink text-white",
};

export function Section({
  tone = "paper",
  className,
  containerClassName,
  children,
  id,
}: {
  tone?: Tone;
  className?: string;
  containerClassName?: string;
  children: React.ReactNode;
  id?: string;
}) {
  return (
    <section
      id={id}
      className={cn("py-20 sm:py-24 lg:py-28", toneClass[tone], className)}
    >
      <Container className={containerClassName}>{children}</Container>
    </section>
  );
}
