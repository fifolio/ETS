export interface SuggestionInput {
    name: string;
    url: string;
    example_url: string | null;
    country: string | null;
    notes: string | null;
}

export interface SuggestionReceipt {
    status: string;
    remaining_today: number;
}