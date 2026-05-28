import { Container } from "@/components/ui/container";
import { Icon } from "@/lib/icons";
import { site } from "@/lib/site";

export function TrustBar() {
  return (
    <div className="border-b border-slate-200 bg-white">
      <Container>
        <div className="flex flex-col items-start gap-5 py-6 lg:flex-row lg:items-center lg:justify-between lg:gap-8">
          <div className="flex items-center gap-4">
            <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-navy-50 text-navy-700">
              <Icon name="Landmark" className="h-6 w-6" />
            </span>
            <div>
              <p className="text-sm font-semibold text-navy-900">
                Состоим в реестре НОСТРОЙ
              </p>
              <p className="text-sm text-slate-500">
                Национальное объединение строителей
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-x-8 gap-y-3">
            <div>
              <p className="text-xs uppercase tracking-wider text-slate-400">
                Регистрационный номер
              </p>
              <p className="font-semibold text-navy-900">{site.registryNumber}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-wider text-slate-400">Дата регистрации</p>
              <p className="font-semibold text-navy-900">{site.registryDate}</p>
            </div>
            <a
              href={site.nostroyUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-xl border border-navy-200 px-4 py-2.5 text-sm font-semibold text-navy-800 transition-colors hover:border-gold-300 hover:bg-gold-50"
            >
              Проверить в реестре
              <Icon name="ExternalLink" className="h-4 w-4" />
            </a>
          </div>
        </div>
      </Container>
    </div>
  );
}
