import { AccountSection } from "@/components/settings/account-section";
import { DeleteAccountSection } from "@/components/settings/delete-account-section";
import { ExtensionsSection } from "@/components/settings/extensions-section";
import { PasswordSection } from "@/components/settings/password-section";

export default function SettingsPage() {
  return (
    <main>
      <h1>Settings</h1>
      <AccountSection />
      <PasswordSection />
      <ExtensionsSection />
      <DeleteAccountSection />
    </main>
  );
}