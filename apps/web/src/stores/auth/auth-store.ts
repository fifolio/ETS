import { create } from "zustand";

import { loadSession } from "@/services/auth/load-session";
import { logIn } from "@/services/auth/log-in";
import { logOut } from "@/services/auth/log-out";
import { signUp } from "@/services/auth/sign-up";
import type { AuthStore } from "@/types/auth/auth-store";

export const useAuthStore = create<AuthStore>()((set) => ({
    user: null,
    loading: true,

    loadSession: async () => set({ user: await loadSession(), loading: false }),
    refresh: async () => set({ user: await loadSession() }),
    signUp: async (input) => set({ user: await signUp(input) }),
    logIn: async (input) => set({ user: await logIn(input) }),
    logOut: async () => {
        await logOut();
        set({ user: null });
    },
}));