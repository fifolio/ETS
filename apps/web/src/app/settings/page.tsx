import { AccountSection } from "@/components/settings/account-section";
import { DeleteAccountSection } from "@/components/settings/delete-account-section";
import { ExtensionsSection } from "@/components/settings/extensions-section";
import { JobBoardsSection } from "@/components/settings/job-boards-section";
import { PasswordSection } from "@/components/settings/password-section";
import { SubscriptionSection } from "@/components/settings/subscription-section";

export default function SettingsPage() {
  return (
    <main>
      <h1>Settings</h1>
      <AccountSection />
      <SubscriptionSection />
      <JobBoardsSection />
      <PasswordSection />
      <ExtensionsSection />
      <DeleteAccountSection />
    </main>
  );
}