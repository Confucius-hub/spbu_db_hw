import { cn } from "@/lib/utils";

/**
 * Фирменная архитектурная графика: силуэт городской застройки со строительным
 * краном (тема строительства / Северной столицы). Вектор — грузится мгновенно,
 * масштабируется, в фирменных цветах. Используется как тематический слой в hero,
 * шапках страниц и обложках новостей. Перекрашивается через text-* (currentColor).
 */
export function Cityscape({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 1200 240"
      preserveAspectRatio="xMidYMax slice"
      className={cn("text-gold-400", className)}
      fill="none"
      aria-hidden
    >
      <g stroke="currentColor" strokeWidth="2" strokeLinejoin="round" opacity="0.9">
        {/* Левая группа зданий */}
        <rect x="40" y="150" width="70" height="90" />
        <rect x="52" y="162" width="12" height="12" />
        <rect x="74" y="162" width="12" height="12" />
        <rect x="52" y="186" width="12" height="12" />
        <rect x="74" y="186" width="12" height="12" />

        <rect x="120" y="110" width="56" height="130" />
        <rect x="132" y="124" width="32" height="10" />
        <rect x="132" y="144" width="32" height="10" />
        <rect x="132" y="164" width="32" height="10" />
        <rect x="132" y="184" width="32" height="10" />

        {/* Башня со шпилем (акцент — «Северная столица») */}
        <path d="M210 240 V70 h44 V240" />
        <path d="M232 70 V40" />
        <path d="M210 70 l22 -30 l22 30" />
        <line x1="218" y1="92" x2="246" y2="92" />
        <line x1="218" y1="116" x2="246" y2="116" />
        <line x1="218" y1="140" x2="246" y2="140" />
        <line x1="218" y1="164" x2="246" y2="164" />

        {/* Здание с сеткой окон */}
        <rect x="300" y="130" width="90" height="110" />
        <line x1="330" y1="130" x2="330" y2="240" />
        <line x1="360" y1="130" x2="360" y2="240" />
        <line x1="300" y1="160" x2="390" y2="160" />
        <line x1="300" y1="190" x2="390" y2="190" />
        <line x1="300" y1="220" x2="390" y2="220" />
      </g>

      {/* Строительный кран (золотой акцент) */}
      <g stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
        <path d="M520 240 V70" />
        <path d="M505 240 L520 226 L535 240" />
        <path d="M470 70 L660 70" />
        <path d="M520 70 L470 70 L520 96 Z" />
        <path d="M520 52 L520 70" />
        <path d="M520 52 L640 70" />
        <line x1="615" y1="70" x2="615" y2="92" />
        <line x1="560" y1="70" x2="560" y2="84" />
        {/* противовес и крюк */}
        <rect x="468" y="64" width="14" height="12" />
        <path d="M615 92 l-6 8 h12 z" />
      </g>

      {/* Правая группа высоток */}
      <g stroke="currentColor" strokeWidth="2" strokeLinejoin="round" opacity="0.9">
        <rect x="700" y="120" width="64" height="120" />
        <line x1="700" y1="150" x2="764" y2="150" />
        <line x1="700" y1="180" x2="764" y2="180" />
        <line x1="700" y1="210" x2="764" y2="210" />
        <line x1="732" y1="120" x2="732" y2="240" />

        <rect x="790" y="90" width="50" height="150" />
        <line x1="790" y1="120" x2="840" y2="120" />
        <line x1="790" y1="150" x2="840" y2="150" />
        <line x1="790" y1="180" x2="840" y2="180" />
        <line x1="790" y1="210" x2="840" y2="210" />

        <rect x="866" y="140" width="80" height="100" />
        <rect x="880" y="154" width="14" height="14" />
        <rect x="904" y="154" width="14" height="14" />
        <rect x="928" y="154" width="14" height="14" />
        <rect x="880" y="186" width="14" height="14" />
        <rect x="904" y="186" width="14" height="14" />
        <rect x="928" y="186" width="14" height="14" />

        <rect x="980" y="110" width="58" height="130" />
        <line x1="980" y1="140" x2="1038" y2="140" />
        <line x1="980" y1="170" x2="1038" y2="170" />
        <line x1="980" y1="200" x2="1038" y2="200" />
        <line x1="1009" y1="110" x2="1009" y2="240" />

        <rect x="1064" y="160" width="96" height="80" />
        <line x1="1096" y1="160" x2="1096" y2="240" />
        <line x1="1128" y1="160" x2="1128" y2="240" />
        <line x1="1064" y1="190" x2="1160" y2="190" />
      </g>
    </svg>
  );
}
