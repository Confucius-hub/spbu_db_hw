import type { MetadataRoute } from "next";
import { site } from "@/lib/site";
import { practices } from "@/lib/practices";

export default function sitemap(): MetadataRoute.Sitemap {
  const routes = ["", "/practices", "/cases", "/about", "/pricing", "/contacts"];
  const now = new Date();

  const staticPages = routes.map((path) => ({
    url: `${site.url}${path}`,
    lastModified: now,
    changeFrequency: "monthly" as const,
    priority: path === "" ? 1 : 0.8,
  }));

  const practicePages = practices.map((p) => ({
    url: `${site.url}/practices/${p.slug}`,
    lastModified: now,
    changeFrequency: "monthly" as const,
    priority: 0.7,
  }));

  return [...staticPages, ...practicePages];
}
