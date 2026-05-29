"use client";

import { useEffect, useState } from "react";
import { Icon } from "@/lib/icons";
import { cn } from "@/lib/utils";

/** Кнопка «наверх» — появляется после прокрутки, плавный скролл к началу. */
export function ScrollToTop() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 600);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <button
      type="button"
      aria-label="Наверх"
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      className={cn(
        "fixed bottom-6 right-6 z-40 inline-flex h-12 w-12 items-center justify-center rounded-full bg-navy-800 text-white shadow-lift transition-all duration-300 ease-[cubic-bezier(0.22,1,0.36,1)] hover:bg-navy-700 hover:shadow-gold",
        visible ? "translate-y-0 opacity-100" : "pointer-events-none translate-y-4 opacity-0",
      )}
    >
      <Icon name="ChevronDown" className="h-5 w-5 rotate-180" strokeWidth={2.5} />
    </button>
  );
}
