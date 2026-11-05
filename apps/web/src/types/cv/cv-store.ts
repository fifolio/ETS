import type { CvInfo } from "./cv";

export interface CvState {
    info: CvInfo | null;
    loaded: boolean;
}

export interface CvActions {
    load: () => Promise<void>;
    upload: (file: File) => Promise<void>;
    remove: () => Promise<void>;
    clear: () => void;
}

export type CvStore = CvState & CvActions;