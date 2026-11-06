import type { TestimonialListProps } from "@/types/feedback";

import { TestimonialCard } from "./testimonial-card";

export function TestimonialList({ testimonials }: TestimonialListProps) {
    if (testimonials.length === 0) {
        return null;
    }
    return (
        <section>
            <h2>What early users say</h2>
            {testimonials.map((testimonial) => (
                <TestimonialCard key={testimonial.id} testimonial={testimonial} />
            ))}
        </section>
    );
}