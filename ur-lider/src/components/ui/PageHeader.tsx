import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { Container } from "./Container";
import { Badge } from "./Badge";
import { Reveal } from "./Reveal";

type Crumb = { label: string; href?: string };

export function PageHeader({
  eyebrow,
  title,
  subtitle,
  crumbs,
}: {
  eyebrow?: string;
  title: string;
  subtitle?: string;
  crumbs?: Crumb[];
}) {
  return (
    <section className="border-b border-line bg-paper-2">
      <Container className="py-14 lg:py-20">
        {crumbs && crumbs.length > 0 && (
          <nav aria-label="Хлебные крошки" className="mb-6">
            <ol className="flex flex-wrap items-center gap-1.5 text-[13px] text-muted">
              {crumbs.map((c, i) => (
                <li key={`${c.label}-${i}`} className="flex items-center gap-1.5">
                  {c.href ? (
                    <Link href={c.href} className="hover:text-ink">
                      {c.label}
                    </Link>
                  ) : (
                    <span className="text-graphite">{c.label}</span>
                  )}
                  {i < crumbs.length - 1 && (
                    <ChevronRight className="h-3.5 w-3.5 text-faint" aria-hidden />
                  )}
                </li>
              ))}
            </ol>
          </nav>
        )}

        {eyebrow && (
          <Reveal>
            <Badge>{eyebrow}</Badge>
          </Reveal>
        )}
        <Reveal delay={60}>
          <h1 className="mt-5 max-w-3xl text-4xl leading-[1.08] text-ink sm:text-5xl">
            {title}
          </h1>
        </Reveal>
        {subtitle && (
          <Reveal delay={120}>
            <p className="mt-5 max-w-2xl text-lg leading-relaxed text-muted">
              {subtitle}
            </p>
          </Reveal>
        )}
      </Container>
    </section>
  );
}
