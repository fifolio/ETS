import { RequireAuth } from "@/components/auth/require-auth";
import type { ChildrenProps } from "@/types/common";

export default function AppLayout({ children }: ChildrenProps) {
    return <RequireAuth>{children}</RequireAuth>;
}