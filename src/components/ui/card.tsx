import { cn } from "@/lib/utils";

/** Базовая поверхность-карточка с опциональным hover-подъёмом. */
export function Card({
  children,
  className,
  hover = false,
}: {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-slate-200/80 bg-white shadow-soft",
        hover &&
          "transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)] hover:-translate-y-1 hover:border-gold-200 hover:shadow-lift",
        className,
      )}
    >
      {children}
    </div>
  );
}
