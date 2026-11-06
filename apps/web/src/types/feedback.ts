export interface FeedbackEligibility {
    eligible: boolean;
    trial_over: boolean;
    enough_scans: boolean;
    already_submitted: boolean;
}

export interface FeedbackInput {
    quote: string;
    internal_suggestions: string;
    consent: boolean;
}

export interface PublicTestimonial {
    id: string;
    quote: string;
    display_name: string;
    role: string | null;
    hours_saved: number;
    scans: number;
}

export interface TestimonialCardProps {
    testimonial: PublicTestimonial;
}

export interface TestimonialListProps {
    testimonials: PublicTestimonial[];
}