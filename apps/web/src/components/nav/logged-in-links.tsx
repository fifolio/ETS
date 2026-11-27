import Link from "next/link";

import type { LoggedInLinksProps } from "@/types/nav";

import { LogOutButton } from "./log-out-button";

export function LoggedInLinks({ name }: LoggedInLinksProps) {
    return (
        <>
            <Link href="/">Dashboard</Link> |{" "}
            <Link href="/history">Jobs history</Link> | <Link href="/settings">Settings</Link> | {name}{" "}
            <LogOutButton />
        </>
    );
}