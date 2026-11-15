import { AccountSection } from "@/components/settings/account-section";
import { AppearanceSection } from "@/components/settings/appearance-section";
import { DeleteAccountSection } from "@/components/settings/delete-account-section";
import { ExtensionsSection } from "@/components/settings/extensions-section";
import { JobBoardsSection } from "@/components/settings/job-boards-section";
import { LanguageSection } from "@/components/settings/language-section";
import { PasswordSection } from "@/components/settings/password-section";
import { SubscriptionSection } from "@/components/settings/subscription-section";
import { SuggestJobBoardSection } from "@/components/settings/suggest-job-board-section";

export default function SettingsPage() {
  return (
    <main>
      <h1>Settings</h1>
      <AccountSection />
      <SubscriptionSection />
      <JobBoardsSection />
      <SuggestJobBoardSection />
      <AppearanceSection />
      <LanguageSection />
      <PasswordSection />
      <ExtensionsSection />
      <DeleteAccountSection />
    </main>
  );
}