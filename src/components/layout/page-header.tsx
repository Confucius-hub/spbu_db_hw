import { Container } from "@/components/ui/container";
import { Breadcrumbs, type Crumb } from "@/components/layout/breadcrumbs";

/** Шапка внутренней страницы: тёмная полоса с хлебными крошками и заголовком. */
export function PageHeader({
  title,
  description,
  breadcrumbs,
  eyebrow,
  children,
}: {
  title: string;
  description?: string;
  breadcrumbs: Crumb[];
  eyebrow?: string;
  children?: React.ReactNode;
}) {
  return (
    <section className="relative overflow-hidden bg-navy-900 text-white">
      <div className="absolute inset-0 bg-grid opacity-40" aria-hidden />
      <div
        className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-gold-500/10 blur-3xl"
        aria-hidden
      />
      <Container className="relative">
        <div className="py-10 sm:py-14">
          <Breadcrumbs items={breadcrumbs} tone="dark" />
          {eyebrow && (
            <p className="mt-5 text-sm font-semibold uppercase tracking-[0.14em] text-gold-400">
              {eyebrow}
            </p>
          )}
          <h1 className="mt-3 max-w-3xl font-display text-3xl font-extrabold leading-tight text-white sm:text-4xl lg:text-[2.9rem]">
            {title}
          </h1>
          {description && (
            <p className="mt-4 max-w-2xl text-lg leading-relaxed text-slate-300">{description}</p>
          )}
          {children && <div className="mt-7">{children}</div>}
        </div>
      </Container>
    </section>
  );
}
