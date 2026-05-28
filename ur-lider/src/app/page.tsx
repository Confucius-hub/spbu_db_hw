import { Hero } from "@/components/sections/Hero";
import { Stats } from "@/components/sections/Stats";
import { PracticeAreas } from "@/components/sections/PracticeAreas";
import { WhyUs } from "@/components/sections/WhyUs";
import { Process } from "@/components/sections/Process";
import { ImageBand } from "@/components/sections/ImageBand";
import { CasesPreview } from "@/components/sections/CasesPreview";
import { Testimonials } from "@/components/sections/Testimonials";
import { CtaBand } from "@/components/sections/CtaBand";

export default function HomePage() {
  return (
    <>
      <Hero />
      <Stats />
      <PracticeAreas />
      <WhyUs />
      <Process />
      <ImageBand />
      <CasesPreview />
      <Testimonials />
      <CtaBand />
    </>
  );
}
