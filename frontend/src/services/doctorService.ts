import API from "./api";
const API_URL = "http://127.0.0.1:8000";

export async function getDoctors() {

    const response = await fetch(
        `${API_URL}/doctors`
    );

    if (!response.ok) {

        throw new Error(
            "Failed to fetch doctors."
        );

    }

    return await response.json();

}


export async function addDoctor(
    doctor: any
) {

    const response = await fetch(
        `${API_URL}/doctors`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(doctor),
        }
    );

    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.error || data.detail || "Failed to add doctor."
        );

    }

    return data;

}
export async function updateDoctor(
    doctorId: number,
    doctor: any
) {

    const response = await fetch(
        `${API_URL}/doctors/${doctorId}`,
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(doctor),
        }
    );

    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.error || data.detail || "Failed to update doctor."
        );

    }

    return data;

}

export async function deleteDoctor(
    doctorId: number
) {

    const response = await fetch(
        `${API_URL}/doctors/${doctorId}`,
        {
            method: "DELETE",
        }
    );

    const data = await response.json();

    if (!response.ok) {

        throw new Error(
            data.error || data.detail || "Failed to delete doctor."
        );

    }

    return data;

}

export async function reactivateDoctor(
  doctorId: number
) {

  const response = await fetch(
    `${API_URL}/doctors/reactivate/${doctorId}`,
    {
      method: "PUT",
    }
  );

  const data = await response.json();

  if (!response.ok) {

    throw new Error(
      data.error || data.detail || "Failed to reactivate doctor."
    );

  }

  return data;

}

export async function getDoctorAttendance(
  attendanceDate: string
) {

  const response = await fetch(
    `${API_URL}/attendance/${attendanceDate}`
  );

  if (!response.ok) {

    throw new Error(
      "Failed to fetch attendance."
    );

  }

  return await response.json();

}

export async function saveDoctorAttendance(
  attendance: any
) {

  const response = await fetch(
    `${API_URL}/attendance`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(attendance),
    }
  );

  const data = await response.json();

  if (!response.ok) {

    throw new Error(
      data.detail || "Failed to save attendance."
    );

  }

  return data;

}