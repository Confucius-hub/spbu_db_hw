import { Container } from "@/components/ui/container";
import { Button } from "@/components/ui/button";
import { mainNav } from "@/lib/site";
import { Icon } from "@/lib/icons";
import Link from "next/link";

export default function NotFound() {
  return (
    <section className="relative overflow-hidden bg-navy-950 text-white">
      <div className="absolute inset-0 bg-grid opacity-40" aria-hidden />
      <Container className="relative">
        <div className="flex min-h-[70vh] flex-col items-center justify-center py-20 text-center">
          <p className="font-display text-7xl font-extrabold text-gold-gradient sm:text-8xl">404</p>
          <h1 className="mt-4 text-2xl font-bold text-white sm:text-3xl">Страница не найдена</h1>
          <p className="mt-3 max-w-md text-slate-300">
            Возможно, страница была перемещена или удалена. Вернитесь на главную или перейдите в один
            из разделов.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <Button href="/" variant="gold" size="lg">
              <Icon name="ArrowRight" className="h-4 w-4 rotate-180" />
              На главную
            </Button>
            <Button href="/news" variant="white" size="lg">
              К новостям
            </Button>
          </div>
          <div className="mt-10 flex flex-wrap justify-center gap-x-5 gap-y-2 text-sm">
            {mainNav.map((n) => (
              <Link key={n.href} href={n.href} className="text-slate-400 transition-colors hover:text-gold-300">
                {n.label}
              </Link>
            ))}
          </div>
        </div>
      </Container>
    </section>
  );
}
