"use client";

import { useEffect } from "react";

import { ErrorMessage } from "@/components/error/error-message";
import { formatErrorReference } from "@/lib/errors/format-error-reference";
import type { ErrorPageProps } from "@/types/error-page";

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <ErrorMessage
      title="Something went wrong"
      message="This page hit an unexpected problem. Try again, and if it keeps happening, contact support."
      reference={formatErrorReference(error.digest)}
      onRetry={reset}
    />
  );
}
