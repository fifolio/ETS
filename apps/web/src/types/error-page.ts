export interface ErrorPageProps {
    error: Error & { digest?: string };
    reset: () => void;
}

export interface ErrorMessageProps {
    title: string;
    message: string;
    reference?: string;
    onRetry?: () => void;
}