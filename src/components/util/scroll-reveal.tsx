"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

/**
 * Мягкое появление секций при скролле.
 * Принцип безопасности: «вооружаем» (скрываем) только элементы, которые при
 * загрузке находятся НИЖЕ первого экрана. Уже видимые секции не трогаем, поэтому
 * вспышки контента нет, а без JS / при reduced-motion всё остаётся видимым.
 */
export function ScrollReveal() {
  const pathname = usePathname();

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (!("IntersectionObserver" in window)) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const els = Array.from(document.querySelectorAll<HTMLElement>("[data-reveal]"));
    const io = new IntersectionObserver(
      (entries, obs) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add("reveal-in");
            obs.unobserve(entry.target);
          }
        }
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 },
    );

    const vh = window.innerHeight;
    for (const el of els) {
      // Вооружаем только то, что полностью ниже первого экрана
      if (el.getBoundingClientRect().top > vh * 0.92) {
        el.classList.add("reveal-armed");
        io.observe(el);
      }
    }

    return () => io.disconnect();
  }, [pathname]);

  return null;
}
