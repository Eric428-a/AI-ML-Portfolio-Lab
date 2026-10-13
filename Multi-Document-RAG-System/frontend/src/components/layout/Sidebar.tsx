import { NavLink, useLocation } from "react-router-dom";
import {
  Activity,
  BookOpen,
  ChevronLeft,
  FileText,
  FolderOpen,
  LayoutDashboard,
  MessageSquareText,
  PanelLeftClose,
  Settings,
  Sparkles,
} from "lucide-react";

import { useAppStore } from "../../store/appStore";

const navigation = [
  {
    title: "Workspace",
    items: [
      {
        label: "Overview",
        path: "/",
        icon: LayoutDashboard,
      },
      {
        label: "AI Chat",
        path: "/chat",
        icon: MessageSquareText,
      },
      {
        label: "Documents",
        path: "/documents",
        icon: FileText,
      },
      {
        label: "Knowledge bases",
        path: "/collections",
        icon: FolderOpen,
      },
    ],
  },
  {
    title: "Manage",
    items: [
      {
        label: "Activity",
        path: "/activity",
        icon: Activity,
      },
      {
        label: "Settings",
        path: "/settings",
        icon: Settings,
      },
    ],
  },
];

export default function Sidebar() {
  const collapsed = useAppStore(
    (state) => state.sidebarCollapsed,
  );
  const toggleSidebar = useAppStore(
    (state) => state.toggleSidebar,
  );
  const location = useLocation();

  return (
    <aside
      className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`}
    >
      <div className="sidebar-brand">
        <NavLink to="/" className="brand-lockup">
          <span className="brand-mark">
            <BookOpen size={21} strokeWidth={2.2} />
          </span>

          {!collapsed && (
            <span className="brand-name">
              <strong>DocuMind</strong>
              <small>INTELLIGENCE</small>
            </span>
          )}
        </NavLink>

        <button
          type="button"
          className="sidebar-toggle icon-button"
          onClick={toggleSidebar}
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? (
            <PanelLeftClose size={18} />
          ) : (
            <ChevronLeft size={18} />
          )}
        </button>
      </div>

      <div className="workspace-switcher">
        <div className="workspace-avatar">D</div>

        {!collapsed && (
          <div className="workspace-info">
            <strong>Personal workspace</strong>
            <span>Knowledge workspace</span>
          </div>
        )}
      </div>

      <nav className="sidebar-navigation">
        {navigation.map((group) => (
          <div className="nav-group" key={group.title}>
            {!collapsed && (
              <p className="nav-group-title">{group.title}</p>
            )}

            {group.items.map((item) => {
              const Icon = item.icon;

              const isActive =
                item.path === "/"
                  ? location.pathname === "/"
                  : location.pathname === item.path ||
                    location.pathname.startsWith(`${item.path}/`);

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  title={collapsed ? item.label : undefined}
                  className={`nav-link ${isActive ? "nav-link-active" : ""}`}
                  aria-current={isActive ? "page" : undefined}
                >
                  <Icon size={19} strokeWidth={1.8} />
                  {!collapsed && <span>{item.label}</span>}
                  {!collapsed && item.path === "/chat" && (
                    <span className="nav-new-badge">AI</span>
                  )}
                </NavLink>
              );
            })}
          </div>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="sidebar-upgrade">
          <div className="upgrade-icon">
            <Sparkles size={18} />
          </div>

          {!collapsed && (
            <div>
              <strong>Research smarter</strong>
              <p>Get answers across your files.</p>
              <NavLink to="/chat" className="upgrade-link">
                Start researching
              </NavLink>
            </div>
          )}
        </div>

        <div className="sidebar-profile">
          <div className="profile-avatar">U</div>
          {!collapsed && (
            <div className="profile-info">
              <strong>Workspace user</strong>
              <span>Local workspace</span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}