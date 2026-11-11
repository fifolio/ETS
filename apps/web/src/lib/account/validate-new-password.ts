import { MIN_PASSWORD_LENGTH } from "@/constants/password";

/** Returns a message for the first problem found, or null when the change can be sent. */
export function validateNewPassword(
    oldPassword: string,
    newPassword: string,
    confirmation: string,
): string | null {
    if (!oldPassword) {
        return "Enter your current password.";
    }
    if (newPassword.length < MIN_PASSWORD_LENGTH) {
        return `The new password must have at least ${MIN_PASSWORD_LENGTH} characters.`;
    }
    if (newPassword !== confirmation) {
        return "The two new passwords don't match.";
    }
    if (newPassword === oldPassword) {
        return "The new password must be different from the current one.";
    }
    return null;
}