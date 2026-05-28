"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Modal } from "@/components/ui/modal";
import { LeadForm } from "@/components/forms/lead-form";
import { Icon } from "@/lib/icons";
import { cn } from "@/lib/utils";

/** Кнопка «Заказать звонок», открывающая модальное окно с формой. */
export function CallbackButton({
  className,
  variant = "outline",
  label = "Заказать звонок",
}: {
  className?: string;
  variant?: "outline" | "gold" | "primary" | "white";
  label?: string;
}) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <Button variant={variant} onClick={() => setOpen(true)} className={className}>
        <Icon name="Phone" className="h-4 w-4" />
        {label}
      </Button>
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Заказать обратный звонок"
        description="Оставьте контакты — перезвоним в течение 15 минут в рабочее время."
      >
        <LeadForm type="CALLBACK" source="callback-modal" submitLabel="Жду звонка" />
      </Modal>
    </>
  );
}

/** Вариант-ссылка (для подвала/текста). */
export function CallbackLink({ className }: { className?: string }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className={cn("underline underline-offset-4 transition-colors hover:text-gold-400", className)}
      >
        Заказать звонок
      </button>
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Заказать обратный звонок"
        description="Оставьте контакты — перезвоним в течение 15 минут в рабочее время."
      >
        <LeadForm type="CALLBACK" source="callback-link" submitLabel="Жду звонка" />
      </Modal>
    </>
  );
}
