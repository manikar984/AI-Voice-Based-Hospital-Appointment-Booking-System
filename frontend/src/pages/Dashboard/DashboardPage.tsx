import {
  CalendarDays,
  Plus,
  Users,
  Stethoscope,
  Bot,
} from "lucide-react";

import { useEffect, useState } from "react";

import { getAppointments } from "@/services/appointmentService";
import { getDashboardStats } from "@/services/dashboardService";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

function DashboardPage() {

  const [appointments, setAppointments] = useState<any[]>([]);

  const upcomingAppointments = [...appointments]
    .filter(
      (appointment) =>
        appointment.status === "scheduled"
    )
    .sort(
      (a, b) =>
        new Date(`${a.date} ${a.time}`).getTime() -
        new Date(`${b.date} ${b.time}`).getTime()
    )
    .slice(0, 5);

  const [dashboardStats, setDashboardStats] = useState<any>(null);

  useEffect(() => {
    loadAppointments();
    loadDashboardStats();
  }, []);
  const navigate = useNavigate();
  const loadAppointments = async () => {
    try {
      const data = await getAppointments();
      setAppointments(data);
    } catch (error) {
      console.error("Failed to load appointments:", error);
    }
  };

  const loadDashboardStats = async () => {
  try {
    const data = await getDashboardStats();

    setDashboardStats(data);
  } catch (error) {
    console.error("Failed to load dashboard statistics:", error);
  }
};


  const stats = [
    {
      title: "Total Appointments",
      value: dashboardStats?.totalAppointments ?? 0,
      icon: CalendarDays,
    },
    {
      title: "Today's Appointments",
      value: dashboardStats?.todayAppointments ?? 0,
      icon: CalendarDays,
    },
    {
      title: "Scheduled",
      value: dashboardStats?.scheduledAppointments ?? 0,
      icon: CalendarDays,
    },
    {
      title: "Completed",
      value: dashboardStats?.completedAppointments ?? 0,
      icon: CalendarDays,
    },
    {
      title: "Doctors",
      value: dashboardStats?.totalDoctors ?? 0,
      icon: Stethoscope,
    },
    {
      title: "Patients",
      value: dashboardStats?.totalPatients ?? 0,
      icon: Users,
    },
  ];


  const recentActivities = appointments
    .slice()
    .sort(
      (a, b) =>
        Number(b.booking_id.replace("APPT", "")) -
        Number(a.booking_id.replace("APPT", ""))
    )
    .slice(0, 5);

  return (
    <div className="space-y-8">

      <div>

        <h1 className="text-3xl font-bold">
          Dashboard
        </h1>

        <p className="text-muted-foreground mt-2">
          Welcome back! Today you have{" "}
          <span className="font-semibold">
            {dashboardStats?.todayAppointments ?? 0}
          </span>{" "}
          appointment(s),{" "}
          <span className="font-semibold">
            {dashboardStats?.scheduledAppointments ?? 0}
          </span>{" "}
          scheduled appointment(s), and{" "}
          <span className="font-semibold">
            {dashboardStats?.completedAppointments ?? 0}
          </span>{" "}
          completed appointment(s).
        </p>

        <p className="text-gray-500 mt-2">
          Welcome back, Admin 👋
        </p>

      </div>
      

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

        {stats.map((item) => {

          const Icon = item.icon;

          return (

            <Card
              key={item.title}
              className="p-6"
            >

              <div className="flex items-center justify-between">

                <div>

                  <p className="text-gray-500">
                    {item.title}
                  </p>

                  <h2 className="text-3xl font-bold mt-2">
                    {item.value}
                  </h2>

                </div>

                <Icon
                  size={36}
                  className="text-blue-600"
                />

              </div>

            </Card>

          );

        })}

      </div>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">
          System Overview
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">
              Hospital Status
            </p>
            <p
              className={`text-lg font-semibold ${
                dashboardStats?.hospitalStatus === "Operational"
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {dashboardStats?.hospitalStatus ?? "Unknown"}
            </p>
          </div>

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">
              AI Voice Agent
            </p>
            <p
              className={`text-lg font-semibold ${
                dashboardStats?.aiAgentStatus === "Online"
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {dashboardStats?.aiAgentStatus ?? "Unknown"}
            </p>
          </div>

          <div className="rounded-lg border p-4">
            <p className="text-sm text-gray-500">
              Database
            </p>
            <p
              className={`text-lg font-semibold ${
                dashboardStats?.databaseStatus === "Connected"
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {dashboardStats?.databaseStatus ?? "Unknown"}
            </p>
          </div>

        </div>
      </Card>

      <Card className="p-6">

        <h2 className="text-xl font-semibold mb-4">
          Quick Actions
        </h2>

        <div className="grid grid-cols-4 gap-4">

          <Button
            className="h-14"
            onClick={() => {

              sessionStorage.setItem(
                "openCreateAppointment",
                "true"
              );

              navigate("/appointments");

            }}
          >
            <Plus className="mr-2 h-5 w-5" />
            New Appointment
          </Button>

          <Button
            variant="outline"
            className="h-14"
            onClick={() => navigate("/patients")}
          >
            <Users className="mr-2 h-5 w-5" />
            Patients
          </Button>

          <Button
            variant="outline"
            className="h-14"
            onClick={() => navigate("/doctors")}
          >
            <Stethoscope className="mr-2 h-5 w-5" />
            Doctors
          </Button>

          <Button
            variant="outline"
            className="h-14"
            onClick={() => navigate("/ai-agent")}
          >
            <Bot className="mr-2 h-5 w-5" />
            AI Voice Agent
          </Button>

        </div>

      </Card>

      <Card className="p-6">

        <div className="mb-4">

          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">
              Upcoming Appointments
            </h2>

            <span className="text-sm text-muted-foreground">
              {appointments.length} Total
            </span>
          </div>

        </div>

        <Table>

          <TableHeader>

            <TableRow>

              <TableHead>Booking ID</TableHead>

              <TableHead>Patient</TableHead>

              <TableHead>Doctor</TableHead>

              <TableHead>Time</TableHead>

              <TableHead>Status</TableHead>

            </TableRow>

          </TableHeader>

          <TableBody>

            {upcomingAppointments.length > 0 ? (

              upcomingAppointments.map((appointment) => (

                <TableRow key={appointment.booking_id}>

                  <TableCell>
                    {appointment.booking_id}
                  </TableCell>

                  <TableCell>
                    {appointment.name}
                  </TableCell>

                  <TableCell>
                    {appointment.doctor}
                  </TableCell>

                  <TableCell>
                    {appointment.time}
                  </TableCell>

                  <TableCell>

                    <Badge
                      className={
                        appointment.status === "completed"
                          ? "bg-green-100 text-green-700"
                          : appointment.status === "scheduled"
                          ? "bg-blue-100 text-blue-700"
                          : appointment.status === "cancelled"
                          ? "bg-red-100 text-red-700"
                          : "bg-yellow-100 text-yellow-700"
                      }
                    >
                      {appointment.status}
                    </Badge>

                  </TableCell>

                </TableRow>

              ))

            ) : (

              <TableRow>

                <TableCell
                  colSpan={5}
                  className="text-center text-gray-500 py-8"
                >
                  No upcoming appointments.
                </TableCell>

              </TableRow>

            )}

          </TableBody>

        </Table>

      </Card>



    <Card className="p-6">

      <div className="mb-4">

        <h2 className="text-xl font-semibold">
          Recent Appointments
        </h2>

      </div>

      <Table>

        <TableHeader>

          <TableRow>

            <TableHead>Booking ID</TableHead>

            <TableHead>Patient</TableHead>

            <TableHead>Doctor</TableHead>

            <TableHead>Date</TableHead>

            <TableHead>Time</TableHead>

            <TableHead>Status</TableHead>

          </TableRow>

        </TableHeader>

        <TableBody>

          {recentActivities.map((appointment) => (

            <TableRow key={appointment.booking_id}>

              <TableCell>
                {appointment.booking_id}
              </TableCell>

              <TableCell>
                {appointment.name}
              </TableCell>

              <TableCell>
                {appointment.doctor}
              </TableCell>

              <TableCell>
                {appointment.date}
              </TableCell>

              <TableCell>
                {appointment.time}
              </TableCell>

              <TableCell>

                <Badge
                  className={
                    appointment.status === "completed"
                      ? "bg-green-100 text-green-700"
                      : appointment.status === "scheduled"
                      ? "bg-blue-100 text-blue-700"
                      : appointment.status === "cancelled"
                      ? "bg-red-100 text-red-700"
                      : "bg-yellow-100 text-yellow-700"
                  }
                >
                  {appointment.status}
                </Badge>

              </TableCell>

            </TableRow>

          ))}

        </TableBody>

      </Table>

    </Card>
    </div>
  );

}

export default DashboardPage;