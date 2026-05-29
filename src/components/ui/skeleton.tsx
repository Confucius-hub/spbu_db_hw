import { cn } from "@/lib/utils";

/** Плейсхолдер-заглушка с мягкой пульсацией для состояний загрузки. */
export function Skeleton({ className }: { className?: string }) {
  return <div className={cn("animate-pulse rounded-lg bg-slate-200/70", className)} />;
}

/** Карточка-скелетон в стиле NewsCard. */
export function NewsCardSkeleton() {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-soft">
      <Skeleton className="aspect-[16/9] rounded-none" />
      <div className="space-y-3 p-5">
        <Skeleton className="h-3 w-32" />
        <Skeleton className="h-5 w-full" />
        <Skeleton className="h-5 w-3/4" />
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-5/6" />
      </div>
    </div>
  );
}
