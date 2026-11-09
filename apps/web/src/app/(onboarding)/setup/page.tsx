import { SetupWizard } from "@/components/onboarding/setup-wizard";

export const instant = false;

export default function SetupPage() {
    return (
        <main>
            <h1>Set up your account</h1>
            <SetupWizard />
        </main>
    );
}