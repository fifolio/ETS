import { CvSection } from "@/components/cv/cv-section";
import { AccountDetails } from "@/components/profile/account-details";
import { ProfileForm } from "@/components/profile/profile-form";

export default function ProfilePage() {
    return (
        <main>
            <h1>Profile</h1>
            <AccountDetails />
            <ProfileForm />
            <CvSection />
        </main>
    );
}