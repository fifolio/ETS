import type { FeedbackInput } from "./feedback";

export interface FeedbackState {
    eligible: boolean;
    submitted: boolean;
    dismissed: boolean;
}

export interface FeedbackActions {
    check: () => Promise<void>;
    submit: (input: FeedbackInput) => Promise<void>;
    dismiss: () => void;
    clear: () => void;
}

export type FeedbackStore = FeedbackState & FeedbackActions;