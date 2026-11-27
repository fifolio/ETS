"use client";

import Link from "next/link";

import type { ErrorMessageProps } from "@/types/error-page";

export function ErrorMessage({
  title,
  message,
  reference,
  onRetry,
}: ErrorMessageProps) {
  return (
    <main>
      <h1>{title}</h1>
      <p>{message}</p>
      {reference && <p>{reference}</p>}
      <p>
        {onRetry && (
          <button type="button" onClick={onRetry}>
            Try again
          </button>
        )}{" "}
        <Link href="/">Go to the home page</Link>{" "}
      </p>
    </main>
  );
}
