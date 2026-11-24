import API from "./api";

export const getPatients = async () => {

  const response = await API.get("/patients");

  return response.data;

};