import type { OptionItem, WorkArrangement } from "@/types/profile";

export const WORK_ARRANGEMENTS: OptionItem<WorkArrangement>[] = [
    { value: "remote", label: "Remote" },
    { value: "hybrid", label: "Hybrid" },
    { value: "onsite", label: "On-site" },
];