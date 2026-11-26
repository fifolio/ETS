import { Suspense } from "react";

import { AccountSection } from "@/components/settings/account-section";
import { AppearanceSection } from "@/components/settings/appearance-section";
import { CreditHistorySection } from "@/components/settings/credit-history-section";
import { CreditsSection } from "@/components/settings/credits-section";
import { CurrencySection } from "@/components/settings/currency-section";
import { DeleteAccountSection } from "@/components/settings/delete-account-section";
import { ExtensionsSection } from "@/components/settings/extensions-section";
import { JobBoardsSection } from "@/components/settings/job-boards-section";
import { LanguageSection } from "@/components/settings/language-section";
import { PasswordSection } from "@/components/settings/password-section";
import { PaymentHistorySection } from "@/components/settings/payment-history-section";
import { PaymentResultBanner } from "@/components/settings/payment-result-banner";
import { SubscriptionSection } from "@/components/settings/subscription-section";
import { SuggestJobBoardSection } from "@/components/settings/suggest-job-board-section";

export const instant = false;

export default function SettingsPage() {
  return (
    <main>
      <h1>Settings</h1>
      <Suspense>
        <PaymentResultBanner />
      </Suspense>
      <hr />
      <AccountSection />
      <hr />
      <CreditsSection />
      <hr />
      <CreditHistorySection />
      <hr />
      <SubscriptionSection />
      <hr />
      <PaymentHistorySection />
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
