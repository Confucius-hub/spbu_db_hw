"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Icon } from "@/lib/icons";

export function ArticleDeleteButton({ id, title }: { id: string; title: string }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  async function remove() {
    if (!confirm(`Удалить статью «${title}»? Действие необратимо.`)) return;
    setLoading(true);
    const res = await fetch(`/api/admin/articles/${id}`, { method: "DELETE" });
    if (res.ok) router.refresh();
    else setLoading(false);
  }

  return (
    <button
      onClick={remove}
      disabled={loading}
      className="inline-flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-red-50 hover:text-red-600 disabled:opacity-50"
      aria-label="Удалить"
      title="Удалить"
    >
      <Icon name="Trash2" className="h-4 w-4" />
    </button>
  );
}
