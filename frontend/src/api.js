// import axios from 'axios';

// const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// export const getWeather = async (city) => {
//   try {
//     const response = await axios.get(`${API_URL}/weather/${city}`);
//     return response.data;
//   } catch (error) {
//     throw new Error(error.response?.data?.detail || 'Failed to fetch weather');
//   }
// };import axios from 'axios';




// import axios from 'axios';

// const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// export const getWeather = async (city) => {
//   const response = await axios.get(`${API_URL}/weather/${city}`);
//   return response.data;
// };

// export const getWeatherHistory = async (city, days) => {
//   const response = await axios.get(`${API_URL}/weather/history/${city}?days=${days}`);
//   return response.data;
// };

// export const getWeatherTrends = async (city, days) => {
//   const response = await axios.get(`${API_URL}/weather/trends/${city}?days=${days}`);
//   return response.data;
// };





import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: API_URL,
});

// Add an interceptor to attach the token from localStorage
axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getWeather = async (city) => {
  const response = await axiosInstance.get(`/weather/${city}`);
  return response.data;
};

export const getWeatherHistory = async (city, days) => {
  const response = await axiosInstance.get(`/weather/history/${city}?days=${days}`);
  return response.data;
};

export const getWeatherTrends = async (city, days) => {
  const response = await axiosInstance.get(`/weather/trends/${city}?days=${days}`);
  return response.data;
};

export const loginUser = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);
  const response = await axiosInstance.post('/token', formData);
  return response.data;
};

export const signupUser = async (username, password) => {
  const response = await axiosInstance.post('/users/', { username, password });
  return response.data;
};

export const logoutUser = async () => {
  const response = await axiosInstance.post('/logout');
  return response.data;
};
