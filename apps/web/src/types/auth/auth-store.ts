import type { AppUser, LogInInput, SignUpInput } from "./auth";

export interface AuthState {
  user: AppUser | null;
  loading: boolean;
}

export interface AuthActions {
  loadSession: () => Promise<void>;
  refresh: () => Promise<void>;
  signUp: (input: SignUpInput) => Promise<void>;
  logIn: (input: LogInInput) => Promise<void>;
  logOut: () => Promise<void>;
}

export type AuthStore = AuthState & AuthActions;