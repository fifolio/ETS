"use client";

import { useFeedbackCheck } from "@/hooks/use-feedback-check";

import { FeedbackModal } from "./feedback-modal";

export function FeedbackInitializer() {
    useFeedbackCheck();
    return <FeedbackModal />;
}