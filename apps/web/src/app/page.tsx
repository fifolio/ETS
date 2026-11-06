import { TestimonialList } from "@/components/testimonials/testimonial-list";
import { getPublicTestimonials } from "@/services/testimonials/get-public-testimonials";

export default async function HomePage() {
  const testimonials = await getPublicTestimonials();

  return (
    <main>
      <h1>ETS: Employment Targeting System</h1>
      <p>Smash or pass: know in seconds if a job post is worth your time.</p>
      <TestimonialList testimonials={testimonials} />
    </main>
  );
}