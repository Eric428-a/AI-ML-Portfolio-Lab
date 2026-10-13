import axios, {
    AxiosError,
    type InternalAxiosRequestConfig,
  } from "axios";
  import type { APIError } from "../types";
  
  const configuredBaseURL = import.meta.env.VITE_API_BASE_URL;
  
  export const apiClient = axios.create({
    baseURL:
      configuredBaseURL?.trim() ||
      "http://127.0.0.1:8000/api/v1",
    timeout: 120_000,
    headers: {
      Accept: "application/json",
    },
  });
  
  apiClient.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      const apiKey = import.meta.env.VITE_API_KEY?.trim();
  
      if (apiKey) {
        config.headers.set("X-API-Key", apiKey);
      }
  
      return config;
    },
  );
  
  export function getAPIErrorMessage(
    error: unknown,
    fallback = "Something went wrong. Please try again.",
  ): string {
    if (axios.isAxiosError<APIError>(error)) {
      const response = error.response?.data;
  
      if (typeof response?.detail === "string") {
        return response.detail;
      }
  
      if (typeof response?.error?.message === "string") {
        return response.error.message;
      }
  
      if (error.code === AxiosError.ERR_NETWORK) {
        return "Cannot connect to the backend. Check that the API is running.";
      }
  
      if (error.code === AxiosError.ECONNABORTED) {
        return "The request timed out. Please try again.";
      }
  
      if (error.response?.status === 413) {
        return "The uploaded file exceeds the server's size limit.";
      }
  
      if (error.response?.status === 415) {
        return "This file type is not supported.";
      }
  
      if (error.response?.status === 401) {
        return "API authentication failed. Check your API key configuration.";
      }
    }
  
    if (error instanceof Error) {
      return error.message || fallback;
    }
  
    return fallback;
  }
  
  export function isAxiosError(
    error: unknown,
  ): error is AxiosError<APIError> {
    return axios.isAxiosError<APIError>(error);
  }