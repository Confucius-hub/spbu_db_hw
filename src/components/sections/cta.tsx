import { Container } from "@/components/ui/container";
import { Button } from "@/components/ui/button";
import { CallbackButton } from "@/components/forms/callback-modal";
import { Photo } from "@/components/ui/photo";
import { Icon } from "@/lib/icons";
import { site, media } from "@/lib/site";

export function Cta({
  title = "Получите расчёт стоимости вступления в СРО",
  text = "Оставьте заявку — рассчитаем стоимость под ваши договоры и подготовим перечень документов. Бесплатно и без обязательств.",
}: {
  title?: string;
  text?: string;
}) {
  return (
    <section className="bg-white py-16 sm:py-20">
      <Container>
        <div className="relative overflow-hidden rounded-3xl bg-navy-900 px-6 py-12 text-center sm:px-12 sm:py-16">
          <Photo
            src={media.construction}
            className="absolute inset-0"
            imgClassName="opacity-15 object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-navy-900 via-navy-900/90 to-navy-900/75" aria-hidden />
          <div className="absolute inset-0 bg-grid opacity-30" aria-hidden />
          <div
            className="absolute -right-20 -top-20 h-72 w-72 rounded-full bg-gold-500/15 blur-3xl"
            aria-hidden
          />
          <div className="relative mx-auto max-w-2xl">
            <h2 className="font-display text-3xl font-extrabold text-white sm:text-4xl">{title}</h2>
            <p className="mx-auto mt-4 max-w-xl text-lg text-slate-300">{text}</p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <Button href="/membership#calculator" variant="gold" size="lg">
                <Icon name="Calculator" className="h-5 w-5" />
                Рассчитать стоимость
              </Button>
              <CallbackButton variant="white" label="Бесплатная консультация" />
            </div>
            <div className="mt-6 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-slate-400">
              <a href={site.phoneHref} className="inline-flex items-center gap-2 hover:text-gold-300">
                <Icon name="Phone" className="h-4 w-4 text-gold-400" />
                {site.phone}
              </a>
              <span className="inline-flex items-center gap-2">
                <Icon name="Clock" className="h-4 w-4 text-gold-400" />
                {site.workHours}
              </span>
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
