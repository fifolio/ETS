import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import type { PublicTestimonial } from "@/types/feedback";

/** Approved testimonials for the landing page. Returns an empty list if anything goes wrong. */
export async function getPublicTestimonials(limit = 12): Promise<PublicTestimonial[]> {
    try {
        const response = await fetch(`${getApiBaseUrl()}/testimonials?limit=${limit}`, {
            next: { revalidate: 300 },
        });
        return response.ok ? await response.json() : [];
    } catch {
        return [];
    }
}