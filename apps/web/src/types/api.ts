export interface CachedToken {
  token: string;
  expiresAt: number;
}

export interface ApiErrorBody {
  detail?: unknown;
  problems?: string[];
}