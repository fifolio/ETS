import { create } from "zustand";

import type { BillingStore } from "@/types/billing-store";

/** Every billing section reloads when `version` changes (a payment was confirmed, or a cancellation). */
export const useBillingStore = create<BillingStore>()((set) => ({
  version: 0,
  bump: () => set((state) => ({ version: state.version + 1 })),
}));