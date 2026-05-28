import { Container } from "@/components/ui/Container";
import { Reveal } from "@/components/ui/Reveal";

const stats = [
  { value: "14 лет", label: "непрерывной практики" },
  { value: "3 200+", label: "выигранных дел" },
  { value: "5,4 млрд ₽", label: "взыскано для клиентов" },
  { value: "92%", label: "дел в пользу доверителя" },
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
