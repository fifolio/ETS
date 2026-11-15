import "./globals.css";
import type { Metadata } from "next";
import { siteMetadata } from "@/lib/metadata";
import { AuthInitializer } from "@/components/auth/auth-initializer";
import { Nav } from "@/components/nav/nav";
import type { ChildrenProps } from "@/types/common";
import { OnboardingInitializer } from "@/components/onboarding/onboarding-initializer";
import { FeedbackInitializer } from "@/components/feedback/feedback-initializer";
import { AppearanceApplier } from "@/components/appearance/appearance-applier";


export const metadata: Metadata = siteMetadata;

export default function RootLayout({ children }: ChildrenProps) {
  return (
    <html lang="en">
      <body>
        <AuthInitializer />
        <AppearanceApplier />
        <OnboardingInitializer />
        <FeedbackInitializer />
        <Nav />
        <hr />
        {children}
      </body>
    </html>
  )
}