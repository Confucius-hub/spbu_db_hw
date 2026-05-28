import { Container } from "@/components/ui/Container";
import { Reveal } from "@/components/ui/Reveal";

const stats = [
  { value: "с 2010", label: "года оформляем допуски СРО" },
  { value: "24 часа", label: "до получения допуска" },
  { value: "1 500+", label: "оформленных допусков" },
  { value: "0 ₽", label: "за подготовку документов" },
];

export function Stats() {
  return (
    <section className="border-y border-line bg-white">
      <Container className="grid grid-cols-2 gap-x-6 gap-y-10 py-12 lg:grid-cols-4 lg:py-14">
        {stats.map((s, i) => (
          <Reveal key={s.label} delay={i * 60}>
            <div className="flex flex-col">
              <span className="font-serif text-3xl font-semibold text-ink sm:text-4xl">
                {s.value}
              </span>
              <span className="mt-1.5 text-sm text-muted">{s.label}</span>
            </div>
          </Reveal>
        ))}
      </Container>
    </section>
  );
}
