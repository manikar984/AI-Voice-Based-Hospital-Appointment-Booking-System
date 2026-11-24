console.log("AppointmentsPage Loaded");
console.log({ Plus });
import {
  Search,
  Plus,
  Eye,
  Pencil,
  Trash2,
} from "lucide-react";
import { useEffect, useState } from "react";
import { DOCTOR_SPECIALIZATIONS } from "@/constants/doctorSpecializations";
import {
  getAppointments,
  createAppointment,
  updateAppointment,
  deleteAppointment,
  getAvailableSlots,
} from "@/services/appointmentService";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import CreateAppointmentDialog from "@/components/CreateAppointmentDialog";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
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

function AppointmentsPage() {
  const [appointments, setAppointments] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [doctorFilter, setDoctorFilter] = useState("all");
  const [dateFilter, setDateFilter] = useState("");
  const [selectedAppointment, setSelectedAppointment] = useState<any>(null);
  const [editOpen, setEditOpen] = useState(false);
  const [availableSlots, setAvailableSlots] = useState<string[]>([]);
  const [editForm, setEditForm] = useState({
    name: "",
    phone: "",
    doctor: "",
    date: "",
    time: "",
  });
  const [open, setOpen] = useState(false);
  useEffect(() => {

    loadAppointments();

  }, []);

  const [createOpen, setCreateOpen] = useState(false);
  useEffect(() => {

    const shouldOpen =
      sessionStorage.getItem("openCreateAppointment");

    if (shouldOpen === "true") {

      setCreateOpen(true);

      sessionStorage.removeItem(
        "openCreateAppointment"
      );

    }

  }, []);
  const [createForm, setCreateForm] = useState({
    name: "",
    phone: "",
    doctor: "",
    date: "",
    time: "",
  });

  const loadAppointments = async () => {
    try {
      const data = await getAppointments();

      console.log(data);

      setAppointments(data);
    } catch (error) {
      console.error("Failed to load appointments:", error);
    }
  };

  const loadAvailableSlots = async (
    doctor: string,
    date: string
  ) => {

    if (!doctor || !date) {

      setAvailableSlots([]);

      return;

    }

    try {

      const slots = await getAvailableSlots(
        doctor,
        date
      );

      console.log("Available slots:", slots);

      setAvailableSlots(slots);

    } catch (error) {

      console.error(error);

      setAvailableSlots([]);

    }

  };

  const handleDelete = async (
    bookingId: string
  ) => {

    const confirmed = window.confirm(
      "Are you sure you want to delete this appointment?"
    );

    if (!confirmed) return;

    try {

      await deleteAppointment(bookingId);

      await loadAppointments();

    } catch (error) {

      console.error(error);

      alert("Failed to delete appointment.");

    }

  };

  const handleEdit = (appointment: any) => {

    setSelectedAppointment(appointment);

    setEditForm({
      name: appointment.name,
      phone: appointment.phone,
      doctor: appointment.doctor,
      date: appointment.date,
      time: appointment.time,
    });

    setEditOpen(true);

  };

  const handleSaveEdit = async () => {

    if (!selectedAppointment) return;

    try {

      await updateAppointment(
        selectedAppointment.booking_id,
        editForm
      );

      setEditOpen(false);

      await loadAppointments();

    } catch (error) {

      console.error(error);

      alert("Failed to update appointment.");

    }

  };

  const handleCreateAppointment = async () => {

    try {

      await createAppointment(createForm);

      setCreateOpen(false);

      resetCreateForm();

      await loadAppointments();

    } 
    catch (error: any) {

      console.error(error);

      console.log(error.response);

      console.log(JSON.stringify(error.response?.data, null, 2));

      alert("Failed to create appointment.");

    }

  };

  const resetCreateForm = () => {

  setCreateForm({
    name: "",
    phone: "",
    doctor: "",
    date: "",
    time: "",
  });

};



console.log("availableSlots state:", availableSlots);

  const filteredAppointments = appointments
    .filter((appointment) => {
      const search = searchTerm.toLowerCase();

      const matchesSearch =
        appointment.booking_id.toLowerCase().includes(search) ||
        appointment.name.toLowerCase().includes(search) ||
        appointment.phone.toLowerCase().includes(search) ||
        appointment.doctor.toLowerCase().includes(search);

      const matchesStatus =
        statusFilter === "all" ||
        appointment.status === statusFilter;

      const matchesDoctor =
        doctorFilter === "all" ||
        appointment.doctor === doctorFilter;

      const matchesDate =
        dateFilter === "" ||
        appointment.date === dateFilter;

      return (
        matchesSearch &&
        matchesStatus &&
        matchesDoctor &&
        matchesDate
      );
    })
    .sort((a, b) => {
      if (
        a.status === "scheduled" &&
        b.status === "completed"
      ) {
        return -1;
      }

      if (
        a.status === "completed" &&
        b.status === "scheduled"
      ) {
        return 1;
      }

      if (a.status === "scheduled") {
        const dateComparison =
          new Date(a.date).getTime() -
          new Date(b.date).getTime();

        if (dateComparison !== 0) {
          return dateComparison;
        }

        return a.time.localeCompare(b.time);
      }

      return (
        new Date(b.date).getTime() -
        new Date(a.date).getTime()
      );
    });

  return (
    <div className="space-y-6">

      <div className="flex items-center justify-between">

        <div>
          <h1 className="text-3xl font-bold">Appointments</h1>
          <p className="text-gray-500">
            Manage all hospital appointments
          </p>
        </div>

        <Button
          onClick={() => setCreateOpen(true)}
        >
          <Plus className="w-4 h-4 mr-2" />
          New Appointment
        </Button>

      </div>

      <Card className="p-4">
  <div className="flex gap-4">

    <div className="relative flex-1">

      <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />

      <Input
        placeholder="Search by Booking ID, Name, Phone or Doctor..."
        className="pl-10"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />

    </div>

    <Select
      value={statusFilter}
      onValueChange={(value) =>
        setStatusFilter(value ?? "all")
      }
    >
      <SelectTrigger className="w-48">
        <SelectValue placeholder="All Status" />
      </SelectTrigger>

      <SelectContent>
        <SelectItem value="all">All Status</SelectItem>
        <SelectItem value="scheduled">Scheduled</SelectItem>
        <SelectItem value="completed">Completed</SelectItem>
      </SelectContent>

    </Select>
    <Select
      value={doctorFilter}
      onValueChange={(value) =>
        setDoctorFilter(value ?? "all")
      }
    >
      <SelectTrigger className="w-48">
        <SelectValue placeholder="All Doctors" />
      </SelectTrigger>

      <SelectContent>
        <SelectItem value="all">All Doctors</SelectItem>
        <SelectItem value="neurologist">Neurologist</SelectItem>
        <SelectItem value="dentist">Dentist</SelectItem>
        <SelectItem value="physician">Physician</SelectItem>
      </SelectContent>

    </Select>

    <div className="w-48">
      <Input
        type="date"
        value={dateFilter}
        onChange={(e) =>
          setDateFilter(e.target.value)
        }
      />
    </div>

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

              <TableRow key={appointment.booking_id}>

                <TableCell>{appointment.booking_id}</TableCell>

                <TableCell>{appointment.name}</TableCell>

                <TableCell>{appointment.phone}</TableCell>

                <TableCell>{appointment.doctor}</TableCell>

                <TableCell>{appointment.date}</TableCell>

                <TableCell>{appointment.time}</TableCell>

                <TableCell>

                  <Badge
                    className={
                      appointment.status === "scheduled"
                        ? "bg-green-100 text-green-700"
                        : appointment.status === "completed"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-red-100 text-red-700"
                    }
                  >
                    {appointment.status.charAt(0).toUpperCase() +
                      appointment.status.slice(1)}
                  </Badge>

                </TableCell>

                <TableCell>

                  <div className="flex gap-2">

                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => {
                        setSelectedAppointment(appointment);
                        setOpen(true);
                      }}
                    >
                      <Eye className="h-4 w-4" />
                    </Button>

                    <Button
                      variant="outline"
                      size="icon"
                      disabled={appointment.status === "completed"}
                      onClick={() => handleEdit(appointment)}
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>

                    <Button
                      variant="destructive"
                      size="icon"
                      disabled={appointment.status === "completed"}
                      onClick={() =>
                        handleDelete(appointment.booking_id)
                      }
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>

                  </div>

                </TableCell>

              </TableRow>

            ))}

          </TableBody>

        </Table>

      </Card>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>

      

          <DialogHeader>
            <DialogTitle>
              Appointment Details
            </DialogTitle>
          </DialogHeader>

          {selectedAppointment && (

            <div className="space-y-3">

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

            </div>

          )}

        </DialogContent>
        ...
</Dialog>

<Dialog
  open={editOpen}
  onOpenChange={setEditOpen}
>
  <DialogContent>

    <DialogHeader>
      <DialogTitle>Edit Appointment</DialogTitle>
    </DialogHeader>

    <div className="space-y-4">


      <div>
        <Label>Doctor</Label>

        <Select
          value={editForm.doctor}
          onValueChange={(value) => {

            const updatedForm = {
              ...editForm,
              doctor: value ?? "",
            };

            setEditForm(updatedForm);

            loadAvailableSlots(
              updatedForm.doctor,
              updatedForm.date
            );

          }}
        >
          <SelectTrigger>
            <SelectValue placeholder="Select Doctor" />
          </SelectTrigger>

          <SelectContent>

            {DOCTOR_SPECIALIZATIONS.map((item) => (

              <SelectItem
                key={item}
                value={item}
              >
                {item}
              </SelectItem>

            ))}

          </SelectContent>
        </Select>

      </div>

      <div>
        <Label>Date</Label>
        <Input
          value={editForm.date}
          onChange={(e) =>
            setEditForm({
              ...editForm,
              date: e.target.value,
            })
          }
        />
      </div>

      <div>
        <Label>Time</Label>

        <Select
          value={editForm.time}
          onValueChange={(value) =>
            setEditForm({
              ...editForm,
              time: value ?? "",
            })
          }
        >

          <SelectTrigger>
            <SelectValue placeholder="Click to choose a time" />
          </SelectTrigger>

          <SelectContent>

            {availableSlots.length > 0 ? (

              availableSlots.map((slot) => (

                <SelectItem
                  key={slot}
                  value={slot}
                >
                  {slot}
                </SelectItem>

              ))

            ) : (

              <SelectItem
                value="no-slots"
                disabled
              >
                No Available Slots
              </SelectItem>

            )}

          </SelectContent>

        </Select>

      </div>

      <div>
        <Label>Name</Label>
        <Input
          value={editForm.name}
          onChange={(e) =>
            setEditForm({
              ...editForm,
              name: e.target.value,
            })
          }
        />
      </div>

      <div>
        <Label>Phone</Label>
        <Input
          value={editForm.phone}
          onChange={(e) =>
            setEditForm({
              ...editForm,
              phone: e.target.value,
            })
          }
        />
      </div>

      <Button
        className="w-full"
        onClick={handleSaveEdit}
      >
        Save Changes
      </Button>

    </div>

  </DialogContent>
</Dialog>

<Dialog
  open={createOpen}
  onOpenChange={(open) => {

    setCreateOpen(open);

    if (!open) {
      resetCreateForm();
    }

  }}
>
  <DialogContent>

    <DialogHeader>
      <DialogTitle>
        New Appointment
      </DialogTitle>
    </DialogHeader>

    <div className="space-y-4">

      <div>
        <Label>Name</Label>
        <Input
          value={createForm.name}
          onChange={(e) =>
            setCreateForm({
              ...createForm,
              name: e.target.value,
            })
          }
        />
      </div>

      <div>
        <Label>Phone</Label>
        <Input
          value={createForm.phone}
          onChange={(e) =>
            setCreateForm({
              ...createForm,
              phone: e.target.value,
            })
          }
        />
      </div>

      <div>
        <Label>Doctor</Label>

        <Select
          value={createForm.doctor}
          onValueChange={(value) => {

            const updatedForm = {
              ...createForm,
              doctor: value ?? "",
            };

            setCreateForm(updatedForm);

            loadAvailableSlots(
              updatedForm.doctor,
              updatedForm.date
            );

          }}
        >
          <SelectTrigger>
            <SelectValue placeholder="Select Doctor" />
          </SelectTrigger>

          <SelectContent>

            {DOCTOR_SPECIALIZATIONS.map((item) => (

              <SelectItem
                key={item}
                value={item}
              >
                {item}
              </SelectItem>

            ))}

          </SelectContent>
        </Select>

      </div>

      <div>
        <Label>Date</Label>
        <Input
          type="date"
          value={createForm.date}
          onChange={(e) => {

            const updatedForm = {
              ...createForm,
              date: e.target.value,
            };

            setCreateForm(updatedForm);

            loadAvailableSlots(
              updatedForm.doctor,
              updatedForm.date
            );

          }}
        />
      </div>

      <div>
        <Label>Time</Label>

        <Select
          value={createForm.time}
          onValueChange={(value) =>
            setCreateForm({
              ...createForm,
              time: value ?? "",
            })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Select Available Slot" />
          </SelectTrigger>

          <SelectContent>
            {availableSlots.length > 0 ? (
              availableSlots.map((slot) => (
                <SelectItem
                  key={slot}
                  value={slot}
                >
                  {slot}
                </SelectItem>
              ))
            ) : (
              <SelectItem
                value="no-slots"
                disabled
              >
                No Available Slots
              </SelectItem>
            )}
          </SelectContent>
        </Select>

      </div>

      <Button
        className="w-full"
        onClick={handleCreateAppointment}
      >
        Create Appointment
      </Button>

    </div>

  </DialogContent>
</Dialog>

    <CreateAppointmentDialog
      open={createOpen}
      onOpenChange={setCreateOpen}
/>
</div>
);
}

export default AppointmentsPage;