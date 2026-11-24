import {
  Bell,
  Search,
  Moon,
  UserCircle,
} from "lucide-react";

function Navbar() {
  return (
    <header className="h-16 bg-white border-b flex items-center justify-between px-6">

      {/* Left Side */}
      <div className="flex items-center gap-3">

        <Search
          size={20}
          className="text-gray-500"
        />

        <input
          type="text"
          placeholder="Search..."
          className="border rounded-lg px-3 py-2 w-72 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

      </div>

      {/* Right Side */}
      <div className="flex items-center gap-6">

        <Bell
          size={22}
          className="cursor-pointer text-gray-600"
        />

        <Moon
          size={22}
          className="cursor-pointer text-gray-600"
        />

        <div className="flex items-center gap-2">

          <UserCircle
            size={34}
            className="text-blue-600"
          />

          <div>

            <p className="font-semibold">
              Admin
            </p>

            <p className="text-xs text-gray-500">
              Hospital Reception
            </p>

          </div>

        </div>

      </div>

    </header>
  );
}

export default Navbar;