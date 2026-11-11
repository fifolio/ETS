import { create } from "zustand";

import { clearApiToken } from "@/lib/api/clear-api-token";
import { loadSession } from "@/services/auth/load-session";
import { logIn } from "@/services/auth/log-in";
import { logOut } from "@/services/auth/log-out";
import { signUp } from "@/services/auth/sign-up";
import { useCvStore } from "@/stores/cv/cv-store";
import { useExtensionsStore } from "@/stores/extension/extensions-store";
import { useFeedbackStore } from "@/stores/feedback/feedback-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";
import type { AuthStore } from "@/types/auth-store";

export const useAuthStore = create<AuthStore>()((set, get) => ({
    user: null,
    loading: true,

    loadSession: async () => set({ user: await loadSession(), loading: false }),
    refresh: async () => set({ user: await loadSession() }),
    signUp: async (input) => set({ user: await signUp(input) }),
    logIn: async (input) => set({ user: await logIn(input) }),
    logOut: async () => {
        await logOut();
        get().signOutLocally();
    },
    // Forget the user in this browser without calling Appwrite (for example after deleting the account).
    signOutLocally: () => {
        clearApiToken();
        useCvStore.getState().clear();
        useOnboardingStore.getState().clear();
        useFeedbackStore.getState().clear();
        useExtensionsStore.getState().clear();
        set({ user: null });
    },
}));