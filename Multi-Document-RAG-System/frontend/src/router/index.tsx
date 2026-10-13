import {
    createBrowserRouter,
    Navigate,
  } from "react-router-dom";
  
  import DashboardLayout from "../components/layout/DashboardLayout";
  
  import Dashboard from "../pages/Dashboard";
  import Documents from "../pages/Documents";
  import Chat from "../pages/Chat";
  import Collections from "../pages/Collections";
  import Activity from "../pages/Activity";
  import Settings from "../pages/Settings";
  import Login from "../pages/Login";
  
  export const router = createBrowserRouter([
    {
      path: "/",
      element: <DashboardLayout />,
      children: [
        {
          index: true,
          element: <Dashboard />,
        },
        {
          path: "documents",
          element: <Documents />,
        },
        {
          path: "chat",
          element: <Chat />,
        },
        {
          path: "chat/:conversationId",
          element: <Chat />,
        },
        {
          path: "collections",
          element: <Collections />,
        },
        {
          path: "activity",
          element: <Activity />,
        },
        {
          path: "settings",
          element: <Settings />,
        },
      ],
    },
    {
      path: "/login",
      element: <Login />,
    },
    {
      path: "*",
      element: <Navigate to="/" replace />,
    },
  ]);