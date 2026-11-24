import API from "./api";

export const getAnalyticsStats = async () => {
  const response = await API.get("/dashboard/analytics");
  return response.data;
};

export const getDoctorAnalytics = async () => {
  const response = await API.get("/dashboard/doctor-analytics");
  return response.data;
};