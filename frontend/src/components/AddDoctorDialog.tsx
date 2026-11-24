import { useEffect, useRef, useState } from "react";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { addDoctor } from "@/services/doctorService";
import { DOCTOR_SPECIALIZATIONS } from "@/constants/doctorSpecializations";

interface AddDoctorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onDoctorAdded: () => void;
}

function AddDoctorDialog({
  open,
  onOpenChange,
  onDoctorAdded,
}: AddDoctorDialogProps) {

  const [name, setName] = useState("");
  const [specialization, setSpecialization] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [experience, setExperience] = useState("");

  const [loading, setLoading] = useState(false);

  const nameRef = useRef<HTMLInputElement>(null);
  const phoneRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);
  const experienceRef = useRef<HTMLInputElement>(null);

  function resetForm() {
    setName("");
    setSpecialization("");
    setPhone("");
    setEmail("");
    setExperience("");
  }

  useEffect(() => {
    if (open) {
      setTimeout(() => {
        nameRef.current?.focus();
      }, 100);
    } else {
      resetForm();
    }
  }, [open]);

  async function handleSave() {

    if (
      !name.trim() ||
      !specialization ||
      !phone.trim() ||
      !email.trim()
    ) {
      alert("Please fill all required fields.");
      return;
    }

    try {

      setLoading(true);

      await addDoctor({

        name,
        specialization,
        phone,
        email,

        experience:
          experience === ""
            ? null
            : Number(experience),

      });

      resetForm();

      onOpenChange(false);

      onDoctorAdded();

    } catch (error: any) {

      alert(error.message);

    } finally {

      setLoading(false);

    }

  }

  function handleEnter(
    e: React.KeyboardEvent<HTMLInputElement>,
    next?: React.RefObject<HTMLInputElement | null>
  ) {

    if (e.key !== "Enter") return;

    e.preventDefault();

    if (next) {

      next.current?.focus();

    } else {

      handleSave();

    }

  }

  return (

    <Dialog
      open={open}
      onOpenChange={onOpenChange}
    >

      <DialogContent className="sm:max-w-lg">

        <DialogHeader>

          <DialogTitle>
            Add Doctor
          </DialogTitle>

        </DialogHeader>

        <div className="space-y-4">

          <div>

            <Label>Name</Label>

            <Input
              ref={nameRef}
              value={name}
              onChange={(e) => setName(e.target.value)}
              onKeyDown={(e) => handleEnter(e, phoneRef)}
            />

          </div>

          <div>

            <Label>Specialization</Label>

            <Select
              value={specialization}
              onValueChange={(value) => setSpecialization(value ?? "")}
            >

              <SelectTrigger>

                <SelectValue placeholder="Select Specialization" />

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

            <Label>Phone</Label>

            <Input
              ref={phoneRef}
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              onKeyDown={(e) => handleEnter(e, emailRef)}
            />

          </div>

          <div>

            <Label>Email</Label>

            <Input
              ref={emailRef}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => handleEnter(e, experienceRef)}
            />

          </div>

          <div>

            <Label>Experience (Years)</Label>

            <Input
              ref={experienceRef}
              type="number"
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              onKeyDown={(e) => handleEnter(e)}
            />

          </div>

        </div>

        <DialogFooter>

          <Button
            variant="outline"
            onClick={() => {

              resetForm();
              onOpenChange(false);

            }}
            disabled={loading}
          >
            Cancel
          </Button>

          <Button
            onClick={handleSave}
            disabled={loading}
          >
            {loading ? "Saving..." : "Save Doctor"}
          </Button>

        </DialogFooter>

      </DialogContent>

    </Dialog>

);

}

export default AddDoctorDialog;