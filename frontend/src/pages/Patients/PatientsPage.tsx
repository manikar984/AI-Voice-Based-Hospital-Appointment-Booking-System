import { Search, Eye } from "lucide-react";
import { useEffect, useState } from "react";
import { getAppointments } from "@/services/appointmentService";

import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

function PatientsPage() {

  const [appointments, setAppointments] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");

  const [selectedAppointment, setSelectedAppointment] =
    useState<any>(null);

  const [open, setOpen] = useState(false);

  useEffect(() => {

    loadAppointments();

  }, []);

  const loadAppointments = async () => {

    try {

      const data = await getAppointments();

      setAppointments(data);

    } catch (error) {

      console.error(error);

    }

  };

  const filteredAppointments = appointments.filter(
    (appointment) => {

      const search =
        searchTerm.toLowerCase();

      return (

        appointment.booking_id
          .toLowerCase()
          .includes(search) ||

        appointment.name
          .toLowerCase()
          .includes(search) ||

        appointment.phone
          .toLowerCase()
          .includes(search) ||

        appointment.doctor
          .toLowerCase()
          .includes(search)

      );

    }
  );

  const getPatientStatistics = (
    phone: string
  ) => {

    const patientAppointments =
      appointments.filter(
        (appointment) =>
          appointment.phone === phone
      );

    return {

      total:
        patientAppointments.length,

      scheduled:
        patientAppointments.filter(
          (appointment) =>
            appointment.status ===
            "scheduled"
        ).length,

      completed:
        patientAppointments.filter(
          (appointment) =>
            appointment.status ===
            "completed"
        ).length,

      history:
        patientAppointments,

    };

  };

  return (

    <div className="space-y-6">

  <div>

    <h1 className="text-3xl font-bold">
      Patients
    </h1>

    <p className="text-gray-500">
      View patient appointments
    </p>

  </div>

  <Card className="p-4">

    <div className="relative max-w-sm">

      <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />

      <Input
        placeholder="Search by Booking ID, Name, Phone or Doctor..."
        className="pl-10"
        value={searchTerm}
        onChange={(e) =>
          setSearchTerm(e.target.value)
        }
      />

    </div>

  </Card>

  <Card className="p-6">

    <Table>

      <TableHeader>

        <TableRow>

          <TableHead>Booking ID</TableHead>
          <TableHead>Patient</TableHead>
          <TableHead>Phone</TableHead>
          <TableHead>Doctor</TableHead>
          <TableHead>Date</TableHead>
          <TableHead>Time</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Actions</TableHead>

        </TableRow>

      </TableHeader>

      <TableBody>

        {filteredAppointments.map((appointment) => (

          <TableRow
            key={appointment.booking_id}
          >

            <TableCell>
              {appointment.booking_id}
            </TableCell>

            <TableCell>
              {appointment.name}
            </TableCell>

            <TableCell>
              {appointment.phone}
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
                  appointment.status === "scheduled"
                    ? "bg-green-100 text-green-700"
                    : "bg-blue-100 text-blue-700"
                }
              >
                {appointment.status}
              </Badge>

            </TableCell>

            <TableCell>

              <Button
                variant="outline"
                size="icon"
                onClick={() => {

                  setSelectedAppointment(
                    appointment
                  );

                  setOpen(true);

                }}
              >
                <Eye className="h-4 w-4" />
              </Button>

            </TableCell>

          </TableRow>

        ))}

      </TableBody>

    </Table>

  </Card>
        <Dialog
        open={open}
        onOpenChange={setOpen}
      >
        <DialogContent>

          <DialogHeader>
            <DialogTitle>
              Patient Details
            </DialogTitle>
          </DialogHeader>

          {selectedAppointment && (() => {

            const stats = getPatientStatistics(
              selectedAppointment.phone
            );

            return (

              <div className="space-y-4">

                <div>

                  <h3 className="font-semibold text-lg">
                    Patient Information
                  </h3>

                </div>

                <p>
                  <strong>Booking ID:</strong>{" "}
                  {selectedAppointment.booking_id}
                </p>

                <p>
                  <strong>Patient:</strong>{" "}
                  {selectedAppointment.name}
                </p>

                <p>
                  <strong>Phone:</strong>{" "}
                  {selectedAppointment.phone}
                </p>

                <p>
                  <strong>Doctor:</strong>{" "}
                  {selectedAppointment.doctor}
                </p>

                <p>
                  <strong>Date:</strong>{" "}
                  {selectedAppointment.date}
                </p>

                <p>
                  <strong>Time:</strong>{" "}
                  {selectedAppointment.time}
                </p>

                <p>
                  <strong>Status:</strong>{" "}
                  {selectedAppointment.status}
                </p>

                <hr />

                <div>

                  <h3 className="font-semibold text-lg">
                    Statistics
                  </h3>

                </div>

                <p>
                  <strong>Total Appointments:</strong>{" "}
                  {stats.total}
                </p>

                <p>
                  <strong>Scheduled:</strong>{" "}
                  {stats.scheduled}
                </p>

                <p>
                  <strong>Completed:</strong>{" "}
                  {stats.completed}
                </p>

                <hr />

                <div>

                  <h3 className="font-semibold text-lg">
                    Appointment History
                  </h3>

                </div>

                <Table>

                  <TableHeader>

                    <TableRow>

                      <TableHead>Booking ID</TableHead>
                      <TableHead>Doctor</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Time</TableHead>
                      <TableHead>Status</TableHead>

                    </TableRow>

                  </TableHeader>

                  <TableBody>

                    {stats.history.map((appointment: any) => (

                      <TableRow key={appointment.booking_id}>

                        <TableCell>
                          {appointment.booking_id}
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
                          <Badge>
                            {appointment.status}
                          </Badge>
                        </TableCell>

                      </TableRow>

                    ))}

                  </TableBody>

                </Table>


              </div>

            );

          })()}

        </DialogContent>

      </Dialog>

    </div>

  );

}

export default PatientsPage;