import type { OptionItem } from "./profile";

export interface CheckboxGroupProps<T extends string> {
    name: string;
    legend: string;
    options: OptionItem<T>[];
    selected: T[];
}