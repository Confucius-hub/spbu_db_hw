import { cn } from "@/lib/utils";

/** Ограничивает ширину контента и задаёт единые горизонтальные отступы. */
export function Container({
  className,
  children,
  size = "default",
}: {
  className?: string;
  children: React.ReactNode;
  size?: "default" | "narrow" | "wide";
}) {
  return (
    <div
      className={cn(
        "mx-auto w-full px-5 sm:px-6 lg:px-8",
        size === "default" && "max-w-7xl",
        size === "narrow" && "max-w-3xl",
        size === "wide" && "max-w-[88rem]",
        className,
      )}
    >
      {children}
    </div>
  );
}
