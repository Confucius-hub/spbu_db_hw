import {
  Briefcase,
  Scale,
  ReceiptText,
  Gavel,
  Building2,
  Users,
  type LucideIcon,
} from "lucide-react";
import type { PracticeIcon as IconName } from "@/lib/practices";

const map: Record<IconName, LucideIcon> = {
  briefcase: Briefcase,
  scale: Scale,
  receipt: ReceiptText,
  gavel: Gavel,
  building: Building2,
  users: Users,
};

export function PracticeIcon({
  name,
  className,
}: {
  name: IconName;
  className?: string;
}) {
  const Icon = map[name];
  return <Icon className={className} strokeWidth={1.6} aria-hidden />;
}
