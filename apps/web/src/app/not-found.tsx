import { ErrorMessage } from "@/components/error/error-message";

export default function NotFound() {
  return (
    <ErrorMessage
      title="Page not found"
      message="This page doesn't exist, or the address is wrong. Check the link and try again."
    />
  );
}
