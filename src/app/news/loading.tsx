import { Container } from "@/components/ui/container";
import { NewsCardSkeleton, Skeleton } from "@/components/ui/skeleton";

export default function NewsLoading() {
  return (
    <>
      <div className="bg-navy-900 py-12 sm:py-14">
        <Container>
          <Skeleton className="h-4 w-40 bg-white/10" />
          <Skeleton className="mt-5 h-10 w-80 max-w-full bg-white/10" />
          <Skeleton className="mt-4 h-5 w-full max-w-xl bg-white/10" />
        </Container>
      </div>
      <section className="bg-slate-50 py-12 sm:py-16">
        <Container>
          <div className="flex flex-wrap gap-2">
            {Array.from({ length: 5 }).map((_, i) => (
              <Skeleton key={i} className="h-9 w-24 rounded-full" />
            ))}
          </div>
          <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <NewsCardSkeleton key={i} />
            ))}
          </div>
        </Container>
      </section>
    </>
  );
}
