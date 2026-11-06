import type { TestimonialCardProps } from "@/types/feedback";

export function TestimonialCard({ testimonial }: TestimonialCardProps) {
    const { quote, display_name, role, hours_saved, scans } = testimonial;

    return (
        <figure>
            <blockquote>{quote}</blockquote>
            <figcaption>
                {display_name}
                {role ? `, ${role}` : ""}
            </figcaption>
            {hours_saved > 0 && (
                <p>
                    {hours_saved} hours saved across {scans} scans
                </p>
            )}
        </figure>
    );
}