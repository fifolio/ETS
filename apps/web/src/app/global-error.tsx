"use client";

import { formatErrorReference } from "@/lib/errors/format-error-reference";
import type { ErrorPageProps } from "@/types/error-page";
import Link from "next/link";

export default function GlobalError({ error, reset }: ErrorPageProps) {
  const reference = formatErrorReference(error.digest);

  return (
    <html lang="en">
      <body>
        <main>
          <h1>Something went wrong</h1>
          <p>
            ETS hit an unexpected problem. Try again, and if it keeps happening,
            contact support.
          </p>
          {reference && <p>{reference}</p>}
          <p>
            <button type="button" onClick={reset}>
              Try again
            </button>{" "}
            <Link href="/">Go to the home page</Link>
          </p>
        </main>
      </body>
    </html>
  );
}
