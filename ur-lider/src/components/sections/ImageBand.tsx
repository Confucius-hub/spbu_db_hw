import { Container } from "@/components/ui/Container";
import { Reveal } from "@/components/ui/Reveal";

/**
 * Full-width photographic band with a short statement.
 * One restrained image — adds life without visual noise.
 */
export function ImageBand() {
  return (
    <section className="bg-paper">
      <Container className="py-6">
        <Reveal>
          <div className="relative overflow-hidden rounded-3xl">
            <div
              aria-hidden
              className="absolute inset-0 bg-cover bg-center"
              style={{
                backgroundImage:
                  "url('https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=2000&auto=format&fit=crop')",
              }}
            />
            <div
              aria-hidden
              className="absolute inset-0 bg-gradient-to-r from-ink/90 via-ink/70 to-ink/30"
            />
            <div className="relative px-6 py-20 sm:px-12 lg:px-16 lg:py-28">
              <p className="text-sm font-semibold uppercase tracking-[0.16em] text-accent">
                Наш подход
              </p>
              <blockquote className="mt-4 max-w-2xl text-2xl font-medium leading-snug text-white sm:text-3xl lg:text-4xl">
                Вы получаете готовый допуск СРО, а всю работу с документами
                и реестром мы берём на себя.
              </blockquote>
            </div>
          </div>
        </Reveal>
      </Container>
    </section>
  );
}
