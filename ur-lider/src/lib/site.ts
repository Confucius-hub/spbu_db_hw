/**
 * Single source of truth for company-wide content:
 * brand, contacts, navigation. Imported by layout, navbar, footer.
 */

export const site = {
  name: "ЮРЛИДЕР",
  legalName: 'Юридическая компания «ЮРЛИДЕР»',
  tagline: "Вступление в СРО в Санкт-Петербурге за 24 часа",
  description:
    "ЮРЛИДЕР — оформление допусков СРО в Санкт-Петербурге с 2010 года: строители, проектировщики, изыскатели. Вступление за 24 часа, первый год без ежемесячных взносов, бесплатная подготовка документов, оплата только компенсационного фонда.",
  url: "https://ur-lider.ru",
  email: "info@ur-lider.ru",
  // TODO: заменить на реальные контакты компании.
  phone: "+7 (812) 425-30-90",
  phoneHref: "+78124253090",
  address: "Санкт-Петербург, Лиговский пр., 92, офис 4",
  workingHours: "Пн–Пт, 09:00–19:00",
  inn: "7840000000",
} as const;

export type NavChild = {
  label: string;
  href: string;
  description?: string;
};

export type NavItem = {
  label: string;
  href: string;
  children?: NavChild[];
};

/** Primary navigation. SRO admissions use a mega-menu (children). */
export const nav: NavItem[] = [
  {
    label: "Допуски СРО",
    href: "/practices",
    children: [
      {
        label: "СРО строителей",
        href: "/practices/builders",
        description: "Допуск на строительство и капремонт",
      },
      {
        label: "СРО проектировщиков",
        href: "/practices/designers",
        description: "Допуск на проектные работы",
      },
      {
        label: "СРО изыскателей",
        href: "/practices/surveyors",
        description: "Допуск на инженерные изыскания",
      },
      {
        label: "Специалисты НРС",
        href: "/practices/nrs",
        description: "Внесение в Национальный реестр",
      },
      {
        label: "Выписки из реестра",
        href: "/practices/extract",
        description: "Электронная выписка за 1 день",
      },
      {
        label: "Смена и переход СРО",
        href: "/practices/transfer",
        description: "Перевод компфонда без простоя",
      },
    ],
  },
  { label: "Кейсы", href: "/cases" },
  { label: "О компании", href: "/about" },
  { label: "Стоимость", href: "/pricing" },
  { label: "Контакты", href: "/contacts" },
];
