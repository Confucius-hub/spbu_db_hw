"use client";

import { useEffect } from "react";
import { cn } from "@/lib/utils";
import { Icon } from "@/lib/icons";

export function Modal({
  open,
  onClose,
  title,
  description,
  children,
}: {
  open: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-end justify-center p-0 sm:items-center sm:p-4">
      <div
        className="absolute inset-0 bg-navy-950/50 backdrop-blur-sm animate-rise"
        onClick={onClose}
        aria-hidden
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className={cn(
          "relative w-full max-w-md rounded-t-3xl bg-white p-6 shadow-lift sm:rounded-3xl sm:p-7",
          "animate-rise",
        )}
      >
        <button
          type="button"
          onClick={onClose}
          className="absolute right-4 top-4 inline-flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-slate-100 hover:text-navy-800"
          aria-label="Закрыть"
        >
          <Icon name="X" className="h-5 w-5" strokeWidth={2} />
        </button>
        {title && <h3 className="pr-8 text-xl font-bold text-navy-900">{title}</h3>}
        {description && <p className="mt-1.5 text-sm text-slate-500">{description}</p>}
        <div className="mt-5">{children}</div>
      </div>
    </div>
  );
}
