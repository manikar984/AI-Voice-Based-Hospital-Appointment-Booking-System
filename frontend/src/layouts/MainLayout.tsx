import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

function MainLayout() {
  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Right Side */}
      <div className="ml-64 flex-1 flex flex-col">

        {/* Top Navbar */}
        <Navbar />

        {/* Page Content */}
        <main className="flex-1 p-6 bg-slate-100">
          <Outlet />
        </main>

      </div>
    </div>
  );
}

export default MainLayout;