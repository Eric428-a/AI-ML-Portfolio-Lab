import { LoaderCircle } from "lucide-react";

interface LoaderProps {
  label?: string;
  fullPage?: boolean;
  size?: number;
}

export default function Loader({
  label = "Loading...",
  fullPage = false,
  size = 22,
}: LoaderProps) {
  return (
    <div
      className={[
        "loader-container",
        fullPage ? "loader-full-page" : "",
      ]
        .filter(Boolean)
        .join(" ")}
      role="status"
      aria-live="polite"
    >
      <LoaderCircle size={size} className="spin loader-icon" />
      <span>{label}</span>
    </div>
  );
}