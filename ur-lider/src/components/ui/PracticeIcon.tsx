import {
  HardHat,
  PencilRuler,
  Mountain,
  BadgeCheck,
  FileCheck2,
  Repeat,
  type LucideIcon,
} from "lucide-react";
import type { PracticeIcon as IconName } from "@/lib/practices";

const map: Record<IconName, LucideIcon> = {
  builders: HardHat,
  designers: PencilRuler,
  surveyors: Mountain,
  nrs: BadgeCheck,
  extract: FileCheck2,
  transfer: Repeat,
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
