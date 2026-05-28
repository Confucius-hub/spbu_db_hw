import { Phone } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Reveal } from "@/components/ui/Reveal";
import { site } from "@/lib/site";

export function CtaBand({
  title = "Обсудим вашу ситуацию?",
  subtitle = "Первая консультация — бесплатно. Расскажем о перспективах и предложим план действий.",
}: {
  title?: string;
  subtitle?: string;
}) {
  return (
    <section className="bg-paper">
      <Container className="py-6">
        <Reveal>
          <div className="relative overflow-hidden rounded-3xl bg-ink px-6 py-14 text-center sm:px-12 lg:py-20">
            <div aria-hidden className="absolute inset-0 bg-grid-dark opacity-50" />
            <div
              aria-hidden
              className="absolute left-1/2 top-0 h-72 w-72 -translate-x-1/2 rounded-full opacity-50 blur-3xl"
              style={{
                background:
                  "radial-gradient(circle, rgba(168,124,79,0.4), transparent 65%)",
              }}
            />
            <div className="relative mx-auto max-w-2xl">
              <h2 className="text-3xl text-white sm:text-4xl lg:text-[2.75rem]">
                {title}
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-white/70">
                {subtitle}
              </p>
              <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
                <Button href="/contacts" variant="accent" size="lg">
                  Записаться на консультацию
                </Button>
                <Button
                  href={`tel:${site.phoneHref}`}
                  variant="onDark"
                  size="lg"
                >
                  <Phone className="h-4 w-4" aria-hidden />
                  {site.phone}
                </Button>
              </div>
            </div>
          </div>
        </Reveal>
      </Container>
    </section>
  );
}
