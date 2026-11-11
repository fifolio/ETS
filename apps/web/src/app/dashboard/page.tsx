import { CvSection } from "@/components/cv/cv-section";
import { AccountDetails } from "@/components/dashboard/account-details";
import { ProfileForm } from "@/components/profile/profile-form";

export default function DashboardPage() {
  return (
    <main>
      <h1>Dashboard</h1>
      <AccountDetails />
      <ProfileForm />
      <CvSection />
    </main>
  );
}