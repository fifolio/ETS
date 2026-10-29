import { AccountDetails } from "@/components/profile/account-details";
import { ApiCheckButton } from "@/components/profile/api-check-button";

export default function ProfilePage() {
    return (
        <main>
            <h1>Profile</h1>
            <AccountDetails />
            <h2>Temporary: API check</h2>
            <ApiCheckButton />
        </main>
    );
}