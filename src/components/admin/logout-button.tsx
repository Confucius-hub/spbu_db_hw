"use client";

import { useRouter } from "next/navigation";
import { Icon } from "@/lib/icons";

export function LogoutButton() {
  const router = useRouter();
  async function logout() {
    await fetch("/api/admin/logout", { method: "POST" });
    router.refresh();
  }
  return (
    <button
      onClick={logout}
      className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-white/10 hover:text-white"
    >
      <Icon name="LogOut" className="h-4 w-4" />
      Выйти
    </button>
  );
}
