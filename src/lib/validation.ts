import { z } from "zod";

const phoneRegex = /^[\d\s()+\-]{7,20}$/;

export const leadSchema = z.object({
  type: z.enum(["CALLBACK", "CONSULTATION", "APPLICATION", "CALCULATOR"]),
  name: z.string().trim().min(2, "Укажите имя").max(120),
  phone: z
    .string()
    .trim()
    .regex(phoneRegex, "Укажите корректный телефон")
    .max(20),
  email: z.string().trim().email("Некорректный e-mail").max(160).optional().or(z.literal("")),
  company: z.string().trim().max(200).optional().or(z.literal("")),
  message: z.string().trim().max(2000).optional().or(z.literal("")),
  source: z.string().trim().max(120).optional(),
  payload: z.record(z.string(), z.unknown()).optional(),
});

export type LeadInput = z.infer<typeof leadSchema>;

export const calculatorSchema = z.object({
  contractAmount: z.number().min(0).max(100_000_000_000),
  needsOpo: z.boolean(),
  specialists: z.number().int().min(0).max(1000),
  needsContractFund: z.boolean().optional().default(false),
  contractFundAmount: z.number().min(0).max(100_000_000_000).optional().default(0),
});

export type CalculatorInput = z.infer<typeof calculatorSchema>;

export const articleSchema = z.object({
  title: z.string().trim().min(4, "Слишком короткий заголовок").max(200),
  slug: z.string().trim().min(2).max(120).regex(/^[a-z0-9-]+$/, "Только латиница, цифры и дефис"),
  excerpt: z.string().trim().min(10, "Добавьте краткое описание").max(400),
  content: z.string().trim().min(20, "Добавьте текст статьи"),
  categoryId: z.string().min(1, "Выберите рубрику"),
  author: z.string().trim().max(120).optional(),
  tags: z.array(z.string().trim().min(1)).max(12).optional().default([]),
  featured: z.boolean().optional().default(false),
  published: z.boolean().optional().default(true),
  seoTitle: z.string().trim().max(200).optional().or(z.literal("")),
  seoDescription: z.string().trim().max(400).optional().or(z.literal("")),
});

export type ArticleInput = z.infer<typeof articleSchema>;
