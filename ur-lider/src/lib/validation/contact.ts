import { z } from "zod";

/**
 * Validation layer (shared between client and server).
 * The schema is the single source of truth for the contact lead DTO.
 */
export const contactSchema = z.object({
  name: z
    .string()
    .trim()
    .min(2, "Укажите имя")
    .max(80, "Слишком длинное имя"),
  phone: z
    .string()
    .trim()
    .min(10, "Укажите корректный телефон")
    .max(20, "Слишком длинный номер")
    .regex(/^[+()\d\s-]+$/, "Телефон содержит недопустимые символы"),
  email: z.email("Некорректный email").max(120).optional().or(z.literal("")),
  topic: z
    .string()
    .trim()
    .max(80)
    .optional()
    .or(z.literal("")),
  message: z
    .string()
    .trim()
    .max(2000, "Сообщение слишком длинное")
    .optional()
    .or(z.literal("")),
  // Honeypot: must stay empty (bots fill it in).
  company: z.string().max(0).optional().or(z.literal("")),
  consent: z.literal(true, {
    error: "Необходимо согласие на обработку данных",
  }),
});

export type ContactInput = z.infer<typeof contactSchema>;

/** Field-level error map returned to the client. */
export type ContactErrors = Partial<Record<keyof ContactInput, string>>;
