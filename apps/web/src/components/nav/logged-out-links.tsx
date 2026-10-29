import Link from "next/link";

export function LoggedOutLinks() {
    return (
        <>
            <Link href="/">ETS</Link> | <Link href="/login">Log in</Link> |{" "}
            <Link href="/signup">Sign up</Link>
        </>
    );
}