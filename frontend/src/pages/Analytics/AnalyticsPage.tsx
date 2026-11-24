import { Card } from "@/components/ui/card";
import { useEffect, useState } from "react";
import {
  getAnalyticsStats,
  getDoctorAnalytics,
} from "@/services/analyticsService";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

function AnalyticsPage() {

  const [analytics, setAnalytics] = useState<any>(null);

  const [doctorAnalytics, setDoctorAnalytics] = useState<any[]>([]);

  const trendData = [
    { day: "Mon", appointments: 5 },
    { day: "Tue", appointments: 8 },
    { day: "Wed", appointments: 6 },
    { day: "Thu", appointments: 10 },
    { day: "Fri", appointments: 7 },
    { day: "Sat", appointments: 3 },
    { day: "Sun", appointments: 1 },
  ];

  const statusData = [
    {
      name: "Completed",
      value: analytics?.completedAppointments ?? 0,
    },
    {
      name: "Scheduled",
      value: analytics?.scheduledAppointments ?? 0,
    },
    {
      name: "Cancelled",
      value: analytics?.cancelledAppointments ?? 0,
    },
  ];

  const COLORS = [
    "#22c55e",
    "#3b82f6",
    "#ef4444",
  ];

  const loadAnalytics = async () => {
    try {
      const data = await getAnalyticsStats();
      setAnalytics(data);
    } catch (error) {
      console.error("Failed to load analytics:", error);
    }
  };

  const loadDoctorAnalytics = async () => {
    try {
      const data = await getDoctorAnalytics();
      setDoctorAnalytics(data);
    } catch (error) {
      console.error("Failed to load doctor analytics:", error);
    }
  };

  useEffect(() => {
    loadAnalytics();  
    loadDoctorAnalytics();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="text-gray-500">
          View hospital appointment analytics and statistics.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <Card className="p-6">
          <h3 className="text-sm text-gray-500">
            Total Appointments
          </h3>

          <p className="mt-2 text-3xl font-bold">
            {analytics?.totalAppointments ?? 0}
          </p>
        </Card>

        <Card className="p-6">
          <h3 className="text-sm text-gray-500">
            Completed
          </h3>

          <p className="mt-2 text-3xl font-bold">
            {analytics?.completedAppointments ?? 0}
          </p>
        </Card>

        <Card className="p-6">
          <h3 className="text-sm text-gray-500">
            Scheduled
          </h3>

          <p className="mt-2 text-3xl font-bold">
            {analytics?.scheduledAppointments ?? 0}
          </p>
        </Card>

        <Card className="p-6">
          <h3 className="text-sm text-gray-500">
            Cancelled
          </h3>

          <p className="mt-2 text-3xl font-bold">
            {analytics?.cancelledAppointments ?? 0}
          </p>
        </Card>
      </div>
        <div className="grid gap-6 lg:grid-cols-2">
          <Card className="p-6 min-h-[350px]">
            <h2 className="text-xl font-semibold mb-4">
              Appointment Trends
            </h2>

            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="appointments"
                    stroke="#2563eb"
                    strokeWidth={3}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card className="p-6 min-h-[350px]">
            <h2 className="text-xl font-semibold mb-4">
              Appointment Status Distribution
            </h2>

            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={statusData}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={90}
                    label
                  >
                    {statusData.map((_, index) => (
                      <Cell
                        key={index}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>

                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card className="p-6 min-h-[320px]">
            <h2 className="text-xl font-semibold mb-4">
              Doctor Analytics
            </h2>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2">Doctor</th>
                    <th className="text-center">Total</th>
                    <th className="text-center">Completed</th>
                    <th className="text-center">Scheduled</th>
                  </tr>
                </thead>

                <tbody>
                  {doctorAnalytics.map((doctor) => (
                    <tr key={doctor.doctor} className="border-b">
                      <td className="py-2">{doctor.doctor}</td>
                      <td className="text-center">{doctor.total}</td>
                      <td className="text-center text-green-600">
                        {doctor.completed}
                      </td>
                      <td className="text-center text-blue-600">
                        {doctor.scheduled}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <Card className="p-6 min-h-[320px]">
            <h2 className="text-xl font-semibold mb-4">
              AI Analytics
            </h2>

            <div className="grid grid-cols-2 gap-4">

              <Card className="p-4">
                <p className="text-sm text-gray-500">AI Calls Today</p>
                <h3 className="text-2xl font-bold">0</h3>
              </Card>

              <Card className="p-4">
                <p className="text-sm text-gray-500">Bookings by AI</p>
                <h3 className="text-2xl font-bold">0</h3>
              </Card>

              <Card className="p-4">
                <p className="text-sm text-gray-500">Transferred Calls</p>
                <h3 className="text-2xl font-bold">0</h3>
              </Card>

              <Card className="p-4">
                <p className="text-sm text-gray-500">Average Call Time</p>
                <h3 className="text-2xl font-bold">0 min</h3>
              </Card>

            </div>
          </Card>
        </div>

        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">
            System Health
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div className="flex justify-between items-center border rounded-lg p-4">
              <span>Backend API</span>
              <span className="text-green-600 font-semibold">● Online</span>
            </div>

            <div className="flex justify-between items-center border rounded-lg p-4">
              <span>Database</span>
              <span className="text-green-600 font-semibold">● Connected</span>
            </div>

            <div className="flex justify-between items-center border rounded-lg p-4">
              <span>AI Voice Agent</span>
              <span className="text-red-600 font-semibold">● Offline</span>
            </div>

            <div className="flex justify-between items-center border rounded-lg p-4">
              <span>Hospital Status</span>
              <span className="text-green-600 font-semibold">● Operational</span>
            </div>

          </div>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card className="p-6 min-h-[320px]">
            <h2 className="text-xl font-semibold mb-4">
              Patient Analytics
            </h2>

            <div className="grid grid-cols-2 gap-4">

              <Card className="p-4">
                <p className="text-sm text-gray-500">Total Patients</p>
                <h3 className="text-2xl font-bold">
                  {analytics?.totalPatients ?? 0}
                </h3>
              </Card>

              <Card className="p-4">
                <p className="text-sm text-gray-500">Today's Appointments</p>
                <h3 className="text-2xl font-bold">
                  {analytics?.todayAppointments ?? 0}
                </h3>
              </Card>

            </div>
          </Card>

          <Card className="p-6 min-h-[320px]">
            <h2 className="text-xl font-semibold mb-4">
              Quick Insights
            </h2>

            <ul className="space-y-3">

              <li>
                ✅ {analytics?.completedAppointments ?? 0} appointments completed.
              </li>

              <li>
                📅 {analytics?.scheduledAppointments ?? 0} appointments scheduled.
              </li>

              <li>
                👨‍⚕️ {analytics?.totalDoctors ?? 0} doctors available.
              </li>

              <li>
                👥 {analytics?.totalPatients ?? 0} registered patients.
              </li>

              <li>
                📈 Completion Rate: {analytics?.completionRate ?? 0}%
              </li>

            </ul>
          </Card>
        </div>

      </div>

  );
}

export default AnalyticsPage;