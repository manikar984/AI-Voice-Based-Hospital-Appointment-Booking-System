import {
  LayoutDashboard,
  CalendarDays,
  Users,
  Stethoscope,
  Bot,
  BarChart3,
  Settings,
} from "lucide-react";

import { NavLink } from "react-router-dom";

function Sidebar() {
  const menuItems = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      name: "Appointments",
      path: "/appointments",
      icon: CalendarDays,
    },
    {
      name: "Patients",
      path: "/patients",
      icon: Users,
    },
    {
      name: "Doctors",
      path: "/doctors",
      icon: Stethoscope,
    },
    {
      name: "AI Voice Agent",
      path: "/ai-agent",
      icon: Bot,
    },

    {
      name: "Analytics",
      path: "/analytics",
      icon: BarChart3,
    },
    {
      name: "Settings",
      path: "/settings",
      icon: Settings,
    },
  ];

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-slate-900 text-white flex flex-col">

      <div className="p-6 border-b border-slate-800">

        <h1 className="text-2xl font-bold">
          AI Hospital
        </h1>

        <p className="text-sm text-slate-400 mt-1">
          Reception Platform
        </p>

      </div>

      <nav className="flex-1 p-4">

        <div className="space-y-2">

          {menuItems.map((item) => {

            const Icon = item.icon;

            return (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-lg px-4 py-3 transition ${
                    isActive
                      ? "bg-blue-600 text-white"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`
                }
              >
                <Icon size={20} />

                <span>{item.name}</span>

              </NavLink>
            );
          })}

        </div>

      </nav>

    </aside>
  );
}

export default Sidebar;