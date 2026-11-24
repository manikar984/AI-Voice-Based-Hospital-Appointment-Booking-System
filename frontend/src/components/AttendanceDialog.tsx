import { useEffect, useState } from "react";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";

import {
  saveDoctorAttendance,
} from "@/services/doctorService";

interface AttendanceDialogProps {

  open: boolean;

  onOpenChange: (open: boolean) => void;

  doctor: any;

  onSaved: () => void;

}

export default function AttendanceDialog({

  open,

  onOpenChange,

  doctor,

  onSaved,

}: AttendanceDialogProps) {

  const today = new Date().toISOString().split("T")[0];

  const [status, setStatus] = useState("Present");

    useEffect(() => {

    if (open) {

      setStatus(doctor?.attendance_status ?? "Present");

    }

  }, [open, doctor]);

  async function handleSave() {

    try {

      await saveDoctorAttendance({

        doctor_id: doctor.doctor_id,

        attendance_date: today,

        attendance_status: status,

      });

      onSaved();

      onOpenChange(false);

    } catch (error: any) {

      alert(error.message);

    }

  }

  return (

    <Dialog
      open={open}
      onOpenChange={onOpenChange}
    >

      <DialogContent>

        <DialogHeader>

          <DialogTitle>

            Doctor Attendance

          </DialogTitle>

        </DialogHeader>

        <p>

          Doctor:
          <b> {doctor?.name}</b>

        </p>

        <select

          value={status}

          onChange={(e) =>
            setStatus(e.target.value)
          }

          className="w-full border rounded p-2"

        >

          <option value="Present">

            Present

          </option>

          <option value="Leave">

            Leave

          </option>

          <option value="Absent">

            Absent

          </option>

        </select>

        <DialogFooter>

          <Button
            onClick={handleSave}
          >

            Save Attendance

          </Button>

        </DialogFooter>

      </DialogContent>

    </Dialog>

  );

}