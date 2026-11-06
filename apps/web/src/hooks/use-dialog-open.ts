import { useEffect, useRef } from "react";

/** Opens and closes a native <dialog> element to match the `open` flag. */
export function useDialogOpen(open: boolean) {
    const ref = useRef<HTMLDialogElement>(null);

    useEffect(() => {
        const dialog = ref.current;
        if (!dialog) {
            return;
        }
        if (open && !dialog.open) {
            dialog.showModal();
        }
        if (!open && dialog.open) {
            dialog.close();
        }
    }, [open]);

    return ref;
}