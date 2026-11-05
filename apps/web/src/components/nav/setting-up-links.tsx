import type { LoggedInLinksProps } from "@/types/nav";

import { LogOutButton } from "./log-out-button";

export function SettingUpLinks({ name }: LoggedInLinksProps) {
    return (
        <>
            ETS | {name} <LogOutButton />
        </>
    );
}