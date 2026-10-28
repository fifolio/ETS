import React from "react";
import type { Metadata } from "next";
import { siteMetadata } from "@/lib/metadata";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = siteMetadata;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav>
          <Link href="/">ETS</Link> | {" "}
          <Link href="/dashboard">Dashboard</Link> | {" "}
          <Link href="/history">Jobs history</Link> | {" "}
          <Link href="/profile">Profile</Link> | {" "}
          <Link href="/settings">Settings</Link> | {" "}
          <Link href="/login">Log in</Link> | {" "}
          <Link href="/signup">Sign up</Link>
        </nav>
        <hr />
        {children}
      </body>
    </html>
  )
}