import { Container } from "@/components/ui/container";
import { Breadcrumbs, type Crumb } from "@/components/layout/breadcrumbs";
import { Photo } from "@/components/ui/photo";
import { media } from "@/lib/site";

/** Шапка внутренней страницы: тёмная полоса с фото-фоном, крошками и заголовком. */
export function PageHeader({
  title,
  description,
  breadcrumbs,
  eyebrow,
  children,
  image = media.construction,
}: {
  title: string;
  description?: string;
  breadcrumbs: Crumb[];
  eyebrow?: string;
  children?: React.ReactNode;
  /** Фоновое фото. По умолчанию — стройплощадка. Передайте свой URL/путь, чтобы заменить. */
  image?: string;
}) {
  return (
    <section className="relative overflow-hidden bg-navy-900 text-white">
      {/* Фото-фон с фолбэком на градиент */}
      {image && (
        <Photo
          src={image}
          className="absolute inset-0"
          imgClassName="opacity-25 [mask-image:linear-gradient(to_right,black,transparent_88%)]"
        />
      )}
      <div
        className="absolute inset-0 bg-gradient-to-r from-navy-900 via-navy-900/85 to-navy-900/70"
        aria-hidden
      />
      <div className="absolute inset-0 bg-grid opacity-25" aria-hidden />
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
