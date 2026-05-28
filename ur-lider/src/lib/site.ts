/**
 * Single source of truth for company-wide content:
 * brand, contacts, navigation. Imported by layout, navbar, footer.
 */

export const site = {
  name: "Лидер",
  legalName: 'Юридическая компания «Лидер»',
  tagline: "Юридическая защита бизнеса и частных клиентов",
  description:
    "Юридическая компания «Лидер» — сопровождение бизнеса, банкротство, налоговые и арбитражные споры, сделки с недвижимостью. 14 лет практики, более 3 200 выигранных дел.",
  url: "https://ur-lider.ru",
  email: "info@ur-lider.ru",
  phone: "+7 (495) 120-45-67",
  phoneHref: "+74951204567",
  address: "Москва, Пресненская наб., 8, стр. 1, БЦ «Город Столиц»",
  workingHours: "Пн–Пт, 09:00–20:00",
  inn: "7701234567",
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

/** Primary navigation. Practices use a mega-menu (children). */
export const nav: NavItem[] = [
  {
    label: "Практики",
    href: "/practices",
    children: [
      {
        label: "Сопровождение бизнеса",
        href: "/practices/business",
        description: "Договоры, корпоративные споры, due diligence",
      },
      {
        label: "Банкротство",
        href: "/practices/bankruptcy",
        description: "Физлиц и компаний, защита от кредиторов",
      },
      {
        label: "Налоговые споры",
        href: "/practices/tax",
        description: "Проверки, доначисления, возврат переплат",
      },
      {
        label: "Арбитраж и суды",
        href: "/practices/litigation",
        description: "Представительство в судах всех инстанций",
      },
      {
        label: "Недвижимость",
        href: "/practices/real-estate",
        description: "Сделки, оспаривание, земельные вопросы",
      },
      {
        label: "Частным клиентам",
        href: "/practices/private",
        description: "Семейные, наследственные, трудовые дела",
      },
    ],
  },
  { label: "Кейсы", href: "/cases" },
  { label: "О компании", href: "/about" },
  { label: "Стоимость", href: "/pricing" },
  { label: "Контакты", href: "/contacts" },
];
