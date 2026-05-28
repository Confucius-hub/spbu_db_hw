import type { Metadata } from "next";
import { isAdmin } from "@/lib/auth";
import { AdminLogin } from "@/components/admin/admin-login";
import { AdminShell } from "@/components/admin/admin-shell";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Админ-панель",
  robots: { index: false, follow: false },
};

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const authed = await isAdmin();
  if (!authed) return <AdminLogin />;
  return <AdminShell>{children}</AdminShell>;
}
