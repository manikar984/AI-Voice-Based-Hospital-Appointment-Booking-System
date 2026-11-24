import {
  Search,
  Pencil,
  Trash2,
  CalendarCheck,
} from "lucide-react";
import { useEffect, useState } from "react";
import AttendanceDialog from "@/components/AttendanceDialog";
import {
  getDoctors,
  addDoctor,
  updateDoctor,
  deleteDoctor,
  reactivateDoctor,
} from "@/services/doctorService";
import EditDoctorDialog from "@/components/EditDoctorDialog";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import AddDoctorDialog from "@/components/AddDoctorDialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

function DoctorsPage() {

  const [doctors, setDoctors] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [openAddDoctor, setOpenAddDoctor] = useState(false);
  const [openEditDoctor, setOpenEditDoctor] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState<any>(null);
  const [openAttendanceDialog, setOpenAttendanceDialog] = useState(false);

  useEffect(() => {

    loadDoctors();

  }, []);

  const loadDoctors = async () => {

    try {

      const data = await getDoctors();

      setDoctors(data);

    } catch (error) {

      console.error(error);

    }

  };

  const handleDeleteDoctor = async (
    doctor: any
  ) => {

    const confirmed = window.confirm(
      `Deactivate ${doctor.name}?`
    );

    if (!confirmed) return;

    try {

      await deleteDoctor(
        doctor.doctor_id
      );

      alert("Doctor deactivated successfully.");

      loadDoctors();

    } catch (error: any) {

      alert(error.message);

    }

  };

  async function handleReactivateDoctor(
    doctor: any
  ) {

    try {

      await reactivateDoctor(
        doctor.doctor_id
      );

      await loadDoctors();

    } catch (error: any) {

      alert(error.message);

    }

  }

  const filteredDoctors = doctors.filter(
    (doctor) => {

      const search =
        searchTerm.toLowerCase();

      return (

        doctor.name
          .toLowerCase()
          .includes(search)

        ||

        doctor.specialization
          .toLowerCase()
          .includes(search)

        ||

        doctor.phone
          .toLowerCase()
          .includes(search)

      );

    }
  );

  const activeDoctors = doctors.filter(
    (doctor) => doctor.status === "Active"
  );

  const inactiveDoctors = doctors.filter(
    (doctor) => doctor.status === "Inactive"
  );

  return (

<div className="space-y-6">

  <div className="flex items-center justify-between">

    <div>

      <h1 className="text-3xl font-bold">
        Doctors
      </h1>

      <p className="text-gray-500">
        Manage doctors
      </p>

    </div>

    <Button
      onClick={() => setOpenAddDoctor(true)}
    >
      Add Doctor
    </Button>

  </div>

  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

    <Card className="p-4">
      <p className="text-sm text-gray-500">
        Active Doctors
      </p>

      <h2 className="text-3xl font-bold text-green-600">
        {activeDoctors.length}
      </h2>
    </Card>

    <Card className="p-4">
      <p className="text-sm text-gray-500">
        Inactive Doctors
      </p>

      <h2 className="text-3xl font-bold text-red-600">
        {inactiveDoctors.length}
      </h2>
    </Card>

    <Card className="p-4">
      <p className="text-sm text-gray-500">
        Total Doctors
      </p>

      <h2 className="text-3xl font-bold text-blue-600">
        {doctors.length}
      </h2>
    </Card>

  </div>

  <Card className="p-4">

    <div className="relative max-w-sm">

      <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />

      <Input
        placeholder="Search by Name, Specialization or Phone..."
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

          <TableHead>Doctor ID</TableHead>
          <TableHead>Name</TableHead>
          <TableHead>Specialization</TableHead>
          <TableHead>Phone</TableHead>
          <TableHead>Email</TableHead>
          <TableHead>Experience</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Attendance</TableHead>
          <TableHead className="text-center">Actions</TableHead>

        </TableRow>

      </TableHeader>

      <TableBody>

        {filteredDoctors.map((doctor) => (

          <TableRow
            key={doctor.doctor_id}
            className={
              doctor.status === "Inactive"
                ? "opacity-60 bg-gray-50"
                : ""
            }
          >

            <TableCell className="font-medium">
              {`DOC${doctor.doctor_id.toString().padStart(4, "0")}`}
            </TableCell>

            <TableCell>
              {doctor.name}
            </TableCell>

            <TableCell>
              {doctor.specialization}
            </TableCell>

            <TableCell>
              {doctor.phone}
            </TableCell>

            <TableCell>
              {doctor.email}
            </TableCell>

            <TableCell>
              {doctor.experience} Years
            </TableCell>

            <TableCell>

              <Badge
                className={
                  doctor.status === "Active"
                    ? "bg-green-100 text-green-700"
                    : "bg-red-100 text-red-700"
                }
              >
                {doctor.status}
              </Badge>

            </TableCell>

            <TableCell>

              <Badge
                className={
                  doctor.attendance_status === "Present"
                    ? "bg-green-100 text-green-700"
                    : doctor.attendance_status === "Absent"
                    ? "bg-red-100 text-red-700"
                    : doctor.attendance_status === "Leave"
                    ? "bg-yellow-100 text-yellow-700"
                    : "bg-gray-100 text-gray-700"
                }
              >
                {doctor.attendance_status ?? "Not Marked"}
              </Badge>

            </TableCell>

            <TableCell className="text-center">

              <div className="flex justify-center gap-2">

                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => {
                    setSelectedDoctor(doctor);
                    setOpenEditDoctor(true);
                  }}
                >
                  <Pencil className="h-4 w-4" />
                </Button>

                <Button
                  variant="outline"
                  size="icon"
                  disabled={doctor.status !== "Active"}
                  title={
                    doctor.status === "Active"
                      ? "Mark Attendance"
                      : "Attendance unavailable for inactive doctors"
                  }
                  onClick={() => {
                    setSelectedDoctor(doctor);
                    setOpenAttendanceDialog(true);
                  }}
                >
                  <CalendarCheck className="h-4 w-4" />
                </Button>

                {doctor.status === "Active" ? (

                  <Button
                    variant="secondary"
                    size="icon"
                    title="Deactivate Doctor"
                    onClick={() => handleDeleteDoctor(doctor)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>

                ) : (

                  <Button
                    variant="secondary"
                    size="icon"
                    title="Reactivate Doctor"
                    onClick={() => handleReactivateDoctor(doctor)}
                  >
                    🔄
                  </Button>

                )}

              </div>

            </TableCell>

          </TableRow>

        ))}

      </TableBody>

    </Table>

  </Card>

  <EditDoctorDialog
      open={openEditDoctor}
      onOpenChange={setOpenEditDoctor}
      doctor={selectedDoctor}
      onDoctorUpdated={loadDoctors}
  />

  <AttendanceDialog
      open={openAttendanceDialog}
      onOpenChange={setOpenAttendanceDialog}
      doctor={selectedDoctor}
      onSaved={() => {
          loadDoctors();
      }}
  />

  <AddDoctorDialog
    open={openAddDoctor}
    onOpenChange={setOpenAddDoctor}
    onDoctorAdded={loadDoctors}
  />
    </div>

  );

}

export default DoctorsPage;