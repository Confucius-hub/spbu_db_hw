import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <Container className="flex min-h-[60vh] flex-col items-center justify-center py-24 text-center">
      <span className="font-serif text-7xl font-semibold text-accent">404</span>
      <h1 className="mt-4 text-3xl text-ink">Страница не найдена</h1>
      <p className="mt-3 max-w-md text-muted">
        Возможно, страница была перемещена или удалена. Вернитесь на главную или
        перейдите к нашим практикам.
      </p>
      <div className="mt-8 flex flex-col gap-3 sm:flex-row">
        <Button href="/" variant="primary">
          На главную
        </Button>
        <Button href="/practices" variant="outline">
          Практики
        </Button>
      </div>
    </Container>
  );
}
