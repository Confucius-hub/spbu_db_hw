# Юридическая компания «Лидер» — production-grade сайт

Полный редизайн сайта юридической компании: современный UX/UI, чистая
компонентная архитектура, типобезопасный backend для заявок.

Стек: **Next.js 16 (App Router) · React 19 · TypeScript · Tailwind CSS v4 · Zod**.

## Запуск (macOS)

Требуется Node.js 20+ (проект разрабатывался на Node 22).

```bash
cd ur-lider
npm install        # установка зависимостей
npm run dev        # http://localhost:3000 — режим разработки
```

Прод-сборка и запуск:

```bash
npm run build      # оптимизированная сборка
npm run start      # запуск собранного приложения
npm run lint       # проверка ESLint
```

## Структура

```
src/
├── app/                      # роутинг (App Router)
│   ├── layout.tsx            # шрифты, метаданные, оболочка (Navbar/Footer)
│   ├── page.tsx              # главная (сборка секций)
│   ├── globals.css           # дизайн-токены (Tailwind v4 @theme) + база
│   ├── practices/
│   │   ├── page.tsx          # список практик
│   │   └── [slug]/page.tsx   # практика (SSG + generateMetadata)
│   ├── cases/ about/ pricing/ contacts/ privacy/   # страницы
│   ├── api/contact/route.ts  # backend: приём заявок
│   ├── sitemap.ts robots.ts not-found.tsx
│
├── components/
│   ├── ui/                   # примитивы дизайн-системы
│   │   ├── Container Section Button Badge SectionHeading
│   │   ├── PageHeader PracticeIcon Reveal
│   ├── layout/               # Navbar (мега-меню + моб. меню), Footer, Logo
│   └── sections/             # блоки: Hero, Stats, PracticeAreas, WhyUs,
│                             #        Process, Cases, Testimonials, CtaBand,
│                             #        ContactForm, Faq
│
└── lib/                      # доменный слой (без UI)
    ├── site.ts               # бренд, контакты, навигация
    ├── practices.ts cases.ts # контент-модели
    ├── validation/contact.ts # zod-схема (источник правды для DTO)
    ├── services/contact-service.ts  # бизнес-логика заявок + провайдер
    └── utils.ts
```

## Архитектура

**Frontend.** Server Components по умолчанию; `"use client"` только там, где
нужен интерактив (Navbar, ContactForm, Reveal). Дизайн-система построена на
токенах в `@theme` — цвета/шрифты задаются один раз и переиспользуются как
Tailwind-утилиты (`bg-ink`, `text-accent`, `font-serif`).

**Backend.** Заявки проходят через слои:
`route handler (HTTP) → zod (валидация) → service (бизнес-логика) → provider (доставка)`.
Слои разделены: HTTP-обработчик не знает о доставке, сервис — о транспорте.
Встроены rate-limit и honeypot. Для продакшена замените `ConsoleLeadProvider`
в `lib/services/contact-service.ts` на отправку в email/CRM.

## Что настроить под клиента

- Контакты и бренд — `src/lib/site.ts`
- Практики и услуги — `src/lib/practices.ts`
- Кейсы — `src/lib/cases.ts`
- Доставка заявок (email/CRM) — `src/lib/services/contact-service.ts`
