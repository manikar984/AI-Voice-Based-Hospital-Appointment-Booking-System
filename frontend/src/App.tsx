import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import AIAgentPage from "./pages/AIAgent/AIAgentPage";
import AnalyticsPage from "./pages/Analytics/AnalyticsPage";
import LoginPage from "./pages/Login/LoginPage";
import DashboardPage from "./pages/Dashboard/DashboardPage";
import AppointmentsPage from "./pages/Appointments/AppointmentsPage";
import PatientsPage from "./pages/Patients/PatientsPage";
import DoctorsPage from "./pages/Doctors/DoctorsPage";
import SettingsPage from "./pages/Settings/SettingsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public Route */}
        <Route
          path="/"
          element={<LoginPage />}
        />

        {/* Protected Routes */}
        <Route element={<MainLayout />}>

          <Route
            path="/ai-agent"
            element={<AIAgentPage />}
          />

          <Route
            path="/analytics"
            element={<AnalyticsPage />}
          />

          <Route
            path="/dashboard"
            element={<DashboardPage />}
          />

          <Route
            path="/appointments"
            element={<AppointmentsPage />}
          />

          <Route
            path="/patients"
            element={<PatientsPage />}
          />

          <Route
            path="/doctors"
            element={<DoctorsPage />}
          />

          <Route
            path="/settings"
            element={<SettingsPage />}
          />

        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;