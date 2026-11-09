import { Suspense } from "react";

import { TestimonialList } from "@/components/testimonials/testimonial-list";
import { getPublicTestimonials } from "@/services/testimonials/get-public-testimonials";

async function PublicTestimonialsSection() {
  const testimonials = await getPublicTestimonials();

  return <TestimonialList testimonials={testimonials} />;
}

export default function HomePage() {
  return (
    <main>
      <h1>ETS: Employment Targeting System</h1>
      <p>Smash or pass: know in seconds if a job post is worth your time.</p>
      <Suspense fallback={null}>
        <PublicTestimonialsSection />
      </Suspense>
    </main>
  );
}