import API from "./api";

export const getAppointments = async () => {
  const response = await API.get("/appointments");
  return response.data;
};

export const getAvailableSlots = async (
  doctor: string,
  date: string
) => {

  const response = await API.get(
    `/availability/${doctor}/${date}`
  );

  return response.data.available_slots;

};

export const createAppointment = async (data: any) => {
  const response = await API.post("/appointments", data);
  return response.data;
};

export const updateAppointment = async (
  bookingId: string,
  data: any
) => {
  const response = await API.put(
    `/appointments/${bookingId}`,
    data
  );

  return response.data;
};

export const deleteAppointment = async (
  bookingId: string
) => {
  const response = await API.delete(
    `/appointments/${bookingId}`
  );

  return response.data;
};  