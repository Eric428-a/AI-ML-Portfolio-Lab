import { useLocation, useNavigate } from "react-router-dom";
import {
  Bell,
  ChevronRight,
  Command,
  FilePlus2,
  MessageSquareText,
  Search,
} from "lucide-react";

import Button from "../common/Button";

const pageNames: Record<string, string> = {
  "/": "Overview",
  "/chat": "AI Chat",
  "/documents": "Documents",
  "/collections": "Knowledge bases",
  "/activity": "Activity",
  "/settings": "Settings",
  "/login": "Sign in",
};

interface NavbarProps {
  onSearch?: () => void;
}

export default function Navbar({ onSearch }: NavbarProps) {
  const location = useLocation();
  const navigate = useNavigate();

  const pageTitle =
    pageNames[location.pathname] ??
    (location.pathname.startsWith("/chat/")
      ? "Conversation"
      : "Workspace");

  return (
    <header className="topbar">
      <div className="topbar-left">
        <div className="breadcrumbs">
          <span className="breadcrumb-root">Workspace</span>
          <ChevronRight size={14} />
          <span className="breadcrumb-current">{pageTitle}</span>
        </div>
      </div>

      <div className="topbar-actions">
        <button
          type="button"
          className="search-trigger"
          onClick={onSearch}
          aria-label="Search workspace"
        >
          <Search size={16} />
          <span>Search</span>
          <kbd>
            <Command size={11} /> K
          </kbd>
        </button>

        <div className="topbar-divider" />

        <button
          type="button"
          className="icon-button notification-button"
          aria-label="Notifications"
          title="Notifications"
          onClick={() =>
            window.alert("No new notifications.")
          }
        >
          <Bell size={18} />
        </button>

        <Button
          variant="secondary"
          icon={<FilePlus2 size={16} />}
          onClick={() => navigate("/documents")}
        >
          Upload files
        </Button>

        <Button
          icon={<MessageSquareText size={16} />}
          onClick={() => navigate("/chat")}
        >
          New chat
        </Button>
      </div>
    </header>
  );
}