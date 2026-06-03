/**
 * Реальные банковские реквизиты СРО «СССС» — со страницы /requisites исходного сайта.
 * Содержание не выдумано: номера счетов, БИК, банки — как в источнике.
 */

import { site } from "./site";

export type BankAccount = {
  title: string;
  kind: "main" | "kf-vv" | "kf-odo";
  account: string;
  bank: string;
  bic: string;
  ks: string;
};

export const accounts: BankAccount[] = [
  {
    title: "Расчётный счёт",
    kind: "main",
    account: "40703810012010787709",
    bank: 'Филиал «Корпоративный» ПАО «Совкомбанк», г. Москва',
    bic: "044525360",
    ks: "30101810445250000360",
  },
  {
    title: "Специальный счёт КФ возмещения вреда (КФ ВВ)",
    kind: "kf-vv",
    account: "40703810112020787709",
    bank: 'Филиал «Корпоративный» ПАО «Совкомбанк», г. Москва',
    bic: "044525360",
    ks: "30101810445250000360",
  },
  {
    title: "Специальный счёт КФ обеспечения договорных обязательств (КФ ОДО)",
    kind: "kf-odo",
    account: "40703810212030787709",
    bank: 'Филиал «Корпоративный» ПАО «Совкомбанк», г. Москва',
    bic: "044525360",
    ks: "30101810445250000360",
  },
  {
    title: "Дополнительный расчётный счёт",
    kind: "main",
    account: "40703810232000000579",
    bank: 'Филиал «Санкт-Петербургский» АО «Альфа-Банк»',
    bic: "044030786",
    ks: "30101810600000000786",
  },
];

export const legalEntity = {
  name: site.legalName,
  shortName: `СРО Ассоциация «${site.name}»`,
  address: site.address,
  inn: site.inn,
  ogrn: site.ogrn,
  kpp: site.kpp,
  registry: site.registryNumber,
  registryDate: site.registryDate,
  phone: site.phone,
  email: site.email,
};
