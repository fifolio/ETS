import { RequireAuth } from "@/components/auth/require-auth";
import type { ChildrenProps } from "@/types/common";

export default function OnboardingLayout({ children }: ChildrenProps) {
    return <RequireAuth>{children}</RequireAuth>;
}