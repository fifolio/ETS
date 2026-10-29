import Link from "next/link";

import type { LoggedInLinksProps } from "@/types/nav";

import { LogOutButton } from "./log-out-button";

export function LoggedInLinks({ name }: LoggedInLinksProps) {
    return (
        <>
            <Link href="/">ETS</Link> | <Link href="/dashboard">Dashboard</Link> |{" "}
            <Link href="/history">Jobs history</Link> | <Link href="/profile">Profile</Link> |{" "}
            <Link href="/settings">Settings</Link> | {name} <LogOutButton />
        </>
    );
}