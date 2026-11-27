import { notFound } from "next/navigation";

export default function DevErrorPage() {
  if (
    process.env.NODE_ENV !== "development" ||
    process.env.NEXT_PUBLIC_DEV_TOOLS !== "true"
  ) {
    notFound();
  }
  throw new Error("Test error from /dev-error");
}
