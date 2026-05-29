import { Container } from "@/components/ui/container";
import { Skeleton } from "@/components/ui/skeleton";

export default function ArticleLoading() {
  return (
    <article>
      <header className="border-b border-slate-200 bg-white">
        <Container size="narrow" className="py-8 sm:py-12">
          <Skeleton className="h-4 w-48" />
          <div className="mt-6 flex gap-3">
            <Skeleton className="h-6 w-28 rounded-full" />
            <Skeleton className="h-6 w-24" />
          </div>
          <Skeleton className="mt-4 h-9 w-full" />
          <Skeleton className="mt-2 h-9 w-2/3" />
          <Skeleton className="mt-4 h-5 w-full" />
        </Container>
      </header>
      <Container size="narrow" className="py-8">
        <Skeleton className="aspect-[16/8] rounded-2xl" />
        <div className="mt-8 space-y-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <Skeleton key={i} className={i % 4 === 0 ? "h-4 w-1/2" : "h-4 w-full"} />
          ))}
        </div>
      </Container>
    </article>
  );
}
