import type { OptionItem, SeniorityLevel } from "@/types/profile";

export const SENIORITY_LEVELS: OptionItem<SeniorityLevel>[] = [
    { value: "intern", label: "Intern" },
    { value: "junior", label: "Junior" },
    { value: "mid", label: "Mid-level" },
    { value: "senior", label: "Senior" },
    { value: "lead", label: "Lead or above" },
];