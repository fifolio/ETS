import "./globals.css";
import type { Metadata } from "next";
import { siteMetadata } from "@/lib/metadata";
import { AuthInitializer } from "@/components/auth/auth-initializer";
import { Nav } from "@/components/nav/nav";
import type { ChildrenProps } from "@/types/common";


export const metadata: Metadata = siteMetadata;

export default function RootLayout({ children }: ChildrenProps) {
  return (
    <html lang="en">
      <body>
        <AuthInitializer />
        <Nav />
        <hr />
        {children}
      </body>
    </html>
  )
}