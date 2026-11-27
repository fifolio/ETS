export interface TimeSavedConfig {
  minutes_per_scan: number;
  credits_per_scan: number;
}

export interface TimeSavedResponse {
  time_saved: TimeSavedConfig;
}

export interface TimeSavedLineProps {
  credits: number;
  perMonth?: boolean;
}