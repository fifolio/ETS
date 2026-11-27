export type CheckoutProduct = "nextmove" | "urgent" | "topup";

export interface CheckoutSession {
    provider: string;
    environment: string;
    checkout_id: string;
    plan_id: string;
    checkout_url: string;
    amount_cents: number; 
    credits: number;
}

export interface CheckoutPanelProps {
    product: CheckoutProduct;
    amountUsd?: number;
}

export interface WhopCheckoutProps {
    session: CheckoutSession;
    returnUrl: string;
}