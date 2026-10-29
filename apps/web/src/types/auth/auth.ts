import type { Models } from "appwrite";

export type AppUser = Models.User<Models.Preferences>;

export type VerificationStatus = "working" | "done" | "failed";

export interface SignUpInput {
  name: string;
  email: string;
  password: string;
}

export interface LogInInput {
  email: string;
  password: string;
}

export interface ConfirmVerificationInput {
  userId: string;
  secret: string;
}