"use client";

import { useState } from "react";
import { Icon } from "@/lib/icons";
import { site } from "@/lib/site";

export function ShareButtons({ slug, title }: { slug: string; title: string }) {
  const [copied, setCopied] = useState(false);
  const url = `${site.url}/news/${slug}`;

  async function copy() {
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      /* noop */
    }
  }

  const tg = `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
  const vk = `https://vk.com/share.php?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`;

  const btn =
    "inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 text-navy-700 transition-colors hover:border-gold-300 hover:bg-gold-50";

  return (
    <div className="flex items-center gap-2">
      <span className="mr-1 text-sm font-medium text-slate-500">Поделиться:</span>
      <a href={tg} target="_blank" rel="noopener noreferrer" className={btn} aria-label="Telegram">
        <Icon name="Send" className="h-4 w-4" />
      </a>
      <a href={vk} target="_blank" rel="noopener noreferrer" className={btn} aria-label="ВКонтакте">
        <Icon name="Users" className="h-4 w-4" />
      </a>
      <button type="button" onClick={copy} className={btn} aria-label="Скопировать ссылку">
        <Icon name={copied ? "Check" : "ExternalLink"} className="h-4 w-4" />
      </button>
      {copied && <span className="text-sm text-emerald-600">Скопировано</span>}
    </div>
  );
}
