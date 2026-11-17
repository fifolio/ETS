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

export function validateResetPassword(password: string, confirmation: string): string | null {
  if (password.length < MIN_PASSWORD_LENGTH) {
    return `The password must have at least ${MIN_PASSWORD_LENGTH} characters.`;
  }
  if (password !== confirmation) {
    return "The two passwords don't match.";
  }
  return null;
}