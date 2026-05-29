import { Hero } from "@/components/home/hero";
import { TrustBar } from "@/components/sections/trust-bar";
import { Advantages } from "@/components/sections/advantages";
import { Stats } from "@/components/sections/stats";
import { Services } from "@/components/sections/services";
import { Steps } from "@/components/sections/steps";
import { NewsTeaser } from "@/components/sections/news-teaser";
import { Faq } from "@/components/sections/faq";
import { Cta } from "@/components/sections/cta";

export const dynamic = "force-dynamic";

export default function HomePage() {
  return (
    <>
      <Hero />
      <TrustBar />
      <Advantages />
      <Services />
      <Stats />
      <Steps />
      <NewsTeaser />
      <Faq />
      <Cta />
    </>
  );
}
