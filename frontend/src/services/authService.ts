import API from "./api";

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  role: string;
}

export const login = async (
  credentials: LoginRequest
): Promise<LoginResponse> => {

  const response = await API.post<LoginResponse>(
    "/auth/login",
    credentials
  );

  localStorage.setItem(
    "access_token",
    response.data.access_token
  );

  localStorage.setItem(
    "user_role",
    response.data.role
  );

  return response.data;
};

export const logout = () => {

  localStorage.removeItem("access_token");
  localStorage.removeItem("user_role");

};

export const getToken = () => {

  return localStorage.getItem("access_token");

};

export const getUserRole = () => {

  return localStorage.getItem("user_role");

};

export const isAuthenticated = () => {

  return !!localStorage.getItem("access_token");

};