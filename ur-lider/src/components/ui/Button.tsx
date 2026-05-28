import Link from "next/link";
import { cn } from "@/lib/utils";

type Variant = "primary" | "accent" | "outline" | "ghost" | "onDark";
type Size = "md" | "lg";

const base =
  "inline-flex items-center justify-center gap-2 rounded-full font-semibold transition-[background-color,color,border-color,transform] duration-200 ease-out active:translate-y-px disabled:pointer-events-none disabled:opacity-60 whitespace-nowrap";

const variants: Record<Variant, string> = {
  primary: "bg-ink text-white hover:bg-ink-2",
  accent: "bg-accent text-white hover:bg-accent-strong",
  outline:
    "border border-line-strong bg-transparent text-ink hover:border-ink hover:bg-white",
  ghost: "bg-transparent text-ink hover:bg-paper-2",
  onDark: "bg-white text-ink hover:bg-paper",
};

const sizes: Record<Size, string> = {
  md: "h-11 px-5 text-sm",
  lg: "h-13 px-7 text-[15px] sm:h-14 sm:px-8",
};

type CommonProps = {
  variant?: Variant;
  size?: Size;
  className?: string;
  children: React.ReactNode;
};

type ButtonAsLink = CommonProps & {
  href: string;
} & Omit<React.ComponentProps<typeof Link>, "href" | "className" | "children">;

type ButtonAsButton = CommonProps & {
  href?: undefined;
} & Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, "className" | "children">;

export function Button(props: ButtonAsLink | ButtonAsButton) {
  const { variant = "primary", size = "md", className, children } = props;
  const classes = cn(base, variants[variant], sizes[size], className);

  if (props.href !== undefined) {
    const { variant: _v, size: _s, className: _c, children: _ch, href, ...rest } =
      props;
    void _v; void _s; void _c; void _ch;
    return (
      <Link href={href} className={classes} {...rest}>
        {children}
      </Link>
    );
  }

  const { variant: _v, size: _s, className: _c, children: _ch, href: _h, ...rest } =
    props;
  void _v; void _s; void _c; void _ch; void _h;
  return (
    <button className={classes} {...rest}>
      {children}
    </button>
  );
}
