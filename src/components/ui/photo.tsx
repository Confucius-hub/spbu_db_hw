"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

/**
 * Декоративное фото с безопасным фолбэком: если изображение не загрузилось,
 * элемент скрывается и остаётся фон-градиент родителя. Используем обычный <img>,
 * чтобы не зависеть от конфигурации доменов next/image.
 */
export function Photo({
  src,
  alt = "",
  className,
  imgClassName,
}: {
  src: string;
  alt?: string;
  className?: string;
  imgClassName?: string;
}) {
  const [failed, setFailed] = useState(false);
  if (failed) return null;

  return (
    <div className={cn("overflow-hidden", className)} aria-hidden={alt === ""}>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={src}
        alt={alt}
        loading="lazy"
        decoding="async"
        onError={() => setFailed(true)}
        className={cn("h-full w-full object-cover", imgClassName)}
      />
    </div>
  );
}
