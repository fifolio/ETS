import { Suspense } from "react";
import { SiteTotalsSection } from "@/components/stats/site-totals-section";
import { TestimonialList } from "@/components/testimonials/testimonial-list";
import { getSiteTotals } from "@/services/stats/get-site-totals";
import { getPublicTestimonials } from "@/services/testimonials/get-public-testimonials";

async function HomePageContent() {
  const [testimonials, totals] = await Promise.all([getPublicTestimonials(), getSiteTotals()]);

  return (
    <>
      {totals && <SiteTotalsSection totals={totals} />}
      <TestimonialList testimonials={testimonials} />
    </>
  );
}

export default function HomePage() {
  return (
    <main>
      <h1>ETS: Employment Targeting System</h1>
      <p>Smash or pass: know in seconds if a job post is worth your time.</p>
      <Suspense fallback={null}>
        <HomePageContent />
      </Suspense>
    </main>
  );
}