import type { Metadata } from "next";
import { site } from "./site";

/** Базовые метаданные сайта (используются в RootLayout). */
export const baseMetadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: `${site.name} — ${site.tagline}`,
    template: `%s — ${site.name}`,
  },
  description: site.description,
  applicationName: site.fullName,
  keywords: [
    "СРО строителей",
    "вступление в СРО",
    "СРО Санкт-Петербург",
    "НРС",
    "допуск СРО",
    "НОСТРОЙ",
    "компенсационный фонд",
    "саморегулируемая организация",
  ],
  authors: [{ name: site.fullName }],
  openGraph: {
    type: "website",
    locale: "ru_RU",
    siteName: site.fullName,
    title: `${site.name} — ${site.tagline}`,
    description: site.description,
    url: site.url,
  },
  twitter: {
    card: "summary_large_image",
    title: `${site.name} — ${site.tagline}`,
    description: site.description,
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large" },
  },
  alternates: { canonical: "/" },
};

/** Помощник для метаданных конкретной страницы. */
export function pageMetadata({
  title,
  description,
  path,
  image,
}: {
  title: string;
  description?: string;
  path: string;
  image?: string;
}): Metadata {
  return {
    title,
    description: description ?? site.description,
    alternates: { canonical: path },
    openGraph: {
      title: `${title} — ${site.name}`,
      description: description ?? site.description,
      url: `${site.url}${path}`,
      ...(image ? { images: [{ url: image }] } : {}),
    },
  };
}

/** JSON-LD: организация (для главной). */
export function organizationJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: site.legalName,
    alternateName: site.name,
    url: site.url,
    telephone: site.phone,
    email: site.email,
    foundingDate: String(site.founded),
    address: {
      "@type": "PostalAddress",
      streetAddress: site.address,
      addressLocality: "Санкт-Петербург",
      addressCountry: "RU",
    },
    identifier: site.registryNumber,
    areaServed: "RU",
  };
}
