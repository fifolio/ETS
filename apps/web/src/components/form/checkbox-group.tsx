import type { CheckboxGroupProps } from "@/types/form";

export function CheckboxGroup<T extends string>({
    name,
    legend,
    options,
    selected,
}: CheckboxGroupProps<T>) {
    return (
        <fieldset>
            <legend>{legend}</legend>
            {options.map(({ value, label }) => (
                <label key={value}>
                    <input
                        type="checkbox"
                        name={name}
                        value={value}
                        defaultChecked={selected.includes(value)}
                    />{" "}
                    {label}{" "}
                </label>
            ))}
        </fieldset>
    );
}