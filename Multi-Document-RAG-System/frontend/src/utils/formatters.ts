export function formatFileSize(bytes: number): string {
    if (!Number.isFinite(bytes) || bytes < 0) {
      return "Unknown size";
    }
  
    if (bytes === 0) {
      return "0 B";
    }
  
    const units = ["B", "KB", "MB", "GB", "TB"];
    const index = Math.min(
      Math.floor(Math.log(bytes) / Math.log(1024)),
      units.length - 1,
    );
  
    const size = bytes / 1024 ** index;
  
    return `${size >= 10 || index === 0 ? size.toFixed(0) : size.toFixed(1)} ${units[index]}`;
  }
  
  export function formatDate(
    value: string,
    options: Intl.DateTimeFormatOptions = {
      month: "short",
      day: "numeric",
      year: "numeric",
    },
  ): string {
    const date = new Date(value);
  
    if (Number.isNaN(date.getTime())) {
      return "Unknown date";
    }
  
    return new Intl.DateTimeFormat(undefined, options).format(date);
  }
  
  export function formatRelativeDate(value: string): string {
    const date = new Date(value);
    const timestamp = date.getTime();
  
    if (Number.isNaN(timestamp)) {
      return "Unknown date";
    }
  
    const elapsed = Date.now() - timestamp;
    const minutes = Math.floor(elapsed / 60_000);
    const hours = Math.floor(elapsed / 3_600_000);
    const days = Math.floor(elapsed / 86_400_000);
  
    if (minutes < 1) return "Just now";
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days === 1) return "Yesterday";
    if (days < 7) return `${days} days ago`;
  
    return formatDate(value);
  }
  
  export function getFileExtension(filename: string): string {
    const index = filename.lastIndexOf(".");
  
    return index >= 0
      ? filename.slice(index + 1).toUpperCase()
      : "FILE";
  }
  
  export function truncate(
    value: string,
    maxLength = 80,
  ): string {
    if (value.length <= maxLength) {
      return value;
    }
  
    return `${value.slice(0, maxLength - 3).trimEnd()}...`;
  }
  
  export function titleFromQuestion(question: string): string {
    return truncate(question.trim(), 55) || "New conversation";
  }
  
  export function formatNumber(value: number): string {
    return new Intl.NumberFormat().format(value);
  }
  
  export function getInitials(value: string): string {
    return value
      .trim()
      .split(/\s+/)
      .slice(0, 2)
      .map((part) => part.charAt(0).toUpperCase())
      .join("");
  }