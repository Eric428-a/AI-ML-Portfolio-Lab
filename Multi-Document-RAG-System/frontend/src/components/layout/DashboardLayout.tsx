import {
    type ReactNode,
    useCallback,
    useEffect,
    useState,
  } from "react";
  import { Outlet, useNavigate } from "react-router-dom";
  import { Search, FileText, MessageSquareText, Settings } from "lucide-react";
  
  import Sidebar from "./Sidebar";
  import Navbar from "./Navbar";
  import Modal from "../common/Modal";
  import { useAppStore } from "../../store/appStore";
  
  interface DashboardLayoutProps {
    children?: ReactNode;
  }
  
  export default function DashboardLayout({
    children,
  }: DashboardLayoutProps) {
    const [searchOpen, setSearchOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");
    const navigate = useNavigate();
    const collapsed = useAppStore(
      (state) => state.sidebarCollapsed,
    );
  
    const openSearch = useCallback(() => {
      setSearchOpen(true);
    }, []);
  
    useEffect(() => {
      const handleKeyDown = (event: KeyboardEvent) => {
        if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
          event.preventDefault();
          openSearch();
        }
      };
  
      window.addEventListener("keydown", handleKeyDown);
  
      return () =>
        window.removeEventListener("keydown", handleKeyDown);
    }, [openSearch]);
  
    const destinations = [
      {
        label: "Overview",
        path: "/",
        keywords: "dashboard home analytics",
        icon: Search,
      },
      {
        label: "AI Chat",
        path: "/chat",
        keywords: "ask question assistant conversation",
        icon: MessageSquareText,
      },
      {
        label: "Documents",
        path: "/documents",
        keywords: "files upload pdf docx",
        icon: FileText,
      },
      {
        label: "Knowledge bases",
        path: "/collections",
        keywords: "collections library sources",
        icon: FileText,
      },
      {
        label: "Settings",
        path: "/settings",
        keywords: "configuration preferences api",
        icon: Settings,
      },
    ];
  
    const filteredDestinations = destinations.filter((item) =>
      `${item.label} ${item.keywords}`
        .toLowerCase()
        .includes(searchQuery.toLowerCase().trim()),
    );
  
    function selectDestination(path: string) {
      navigate(path);
      setSearchOpen(false);
      setSearchQuery("");
    }
  
    return (
      <div className="app-shell">
        <Sidebar />
  
        <div
          className={`app-main ${collapsed ? "app-main-expanded" : ""}`}
        >
          <Navbar onSearch={openSearch} />
  
          <main className="page-content">
            {children ?? <Outlet />}
          </main>
        </div>
  
        <Modal
          open={searchOpen}
          title="Search workspace"
          description="Jump to a page in your workspace."
          onClose={() => {
            setSearchOpen(false);
            setSearchQuery("");
          }}
        >
          <div className="workspace-search-input">
            <Search size={18} />
            <input
              autoFocus
              value={searchQuery}
              onChange={(event) =>
                setSearchQuery(event.target.value)
              }
              placeholder="Search pages..."
              aria-label="Search pages"
            />
          </div>
  
          <div className="search-destinations">
            {filteredDestinations.map((item) => {
              const Icon = item.icon;
  
              return (
                <button
                  key={item.path}
                  type="button"
                  className="search-destination"
                  onClick={() => selectDestination(item.path)}
                >
                  <span className="search-destination-icon">
                    <Icon size={18} />
                  </span>
                  <span>{item.label}</span>
                  <span className="search-destination-enter">
                    Enter ↵
                  </span>
                </button>
              );
            })}
  
            {filteredDestinations.length === 0 && (
              <p className="search-no-results">
                No pages match your search.
              </p>
            )}
          </div>
        </Modal>
      </div>
    );
  }