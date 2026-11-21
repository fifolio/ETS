import { AccountSection } from "@/components/settings/account-section";
import { AppearanceSection } from "@/components/settings/appearance-section";
import { CreditsSection } from "@/components/settings/credits-section";
import { CurrencySection } from "@/components/settings/currency-section";
import { DeleteAccountSection } from "@/components/settings/delete-account-section";
import { ExtensionsSection } from "@/components/settings/extensions-section";
import { JobBoardsSection } from "@/components/settings/job-boards-section";
import { LanguageSection } from "@/components/settings/language-section";
import { PasswordSection } from "@/components/settings/password-section";
import { SubscriptionSection } from "@/components/settings/subscription-section";
import { SuggestJobBoardSection } from "@/components/settings/suggest-job-board-section";

export const instant = false;

export default function SettingsPage() {
  return (
    <main>
      <h1>Settings</h1>
      <hr />
      <AccountSection />
      <hr />
      <CreditsSection />
      <hr />
      <SubscriptionSection />
      <hr />
      <JobBoardsSection />
      <hr />
      <SuggestJobBoardSection />
      <hr />
      <AppearanceSection />
      <hr />
      <LanguageSection />
      <hr />
      <CurrencySection />
      <hr />
      <PasswordSection />
      <hr />
      <ExtensionsSection />
      <hr />
      <DeleteAccountSection />
    </main>
  );
}
