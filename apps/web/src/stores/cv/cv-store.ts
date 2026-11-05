import { create } from "zustand";

import { deleteCv } from "@/services/cv/delete-cv";
import { getCvInfo } from "@/services/cv/get-cv-info";
import { uploadCv } from "@/services/cv/upload-cv";
import type { CvStore } from "@/types/cv/cv-store";
import { useOnboardingStore } from "@/stores/onboarding/onboarding-store";


export const useCvStore = create<CvStore>()((set) => ({
    info: null,
    loaded: false,

    load: async () => set({ info: await getCvInfo(), loaded: true }),
    upload: async (file) => {
        set({ info: await uploadCv(file) });
        await useOnboardingStore.getState().load();
    },
    remove: async () => {
        await deleteCv();
        set({ info: null });
        await useOnboardingStore.getState().load();
    },
    clear: () => set({ info: null, loaded: false }),
}));