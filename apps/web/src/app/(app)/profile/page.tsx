import { CvSection } from "@/components/cv/cv-section";
import { AccountDetails } from "@/components/profile/account-details";
import { ProfileForm } from "@/components/profile/profile-form";
import { SetupChecklist } from "@/components/profile/setup-checklist";

export default function ProfilePage() {
    return (
        <main>
            <h1>Profile</h1>
            <SetupChecklist />
            <AccountDetails />
            <ProfileForm />
            <CvSection />
        </main>
    );
}