import React, { useState } from 'react';
import SearchBar from './SearchBar';
import WeatherCard from './WeatherCard';
import WeatherHistory from './WeatherHistory';
import { getWeather, getWeatherHistory, getWeatherTrends, logoutUser } from '../api';
import { useNavigate } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Dashboard = () => {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [trends, setTrends] = useState(null);
  const [history, setHistory] = useState(null);
  const [error, setError] = useState('');
  const [days, setDays] = useState(7); // default 7 days
  const [view, setView] = useState('dashboard'); // 'dashboard' or 'history'
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logoutUser();
      localStorage.removeItem('access_token');
      navigate('/login');
    } catch (err) {
      console.error('Logout failed', err);
    }
  };

  const fetchWeather = async () => {
    try {
      const data = await getWeather(city);
      setWeather(data);
      setTrends(null);
      setHistory(null);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
  };

  const fetchTrends = async () => {
    try {
      const data = await getWeatherTrends(city, days);
      setTrends(data);
      setWeather(null);
      setHistory(null);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
  };

  const fetchHistory = async () => {
    try {
      const data = await getWeatherHistory(city, days);
      setHistory(data);
      setWeather(null);
      setTrends(null);
      setError('');
      setView('history');
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
  };

  // Prepare chart data from trends data
  const chartData = trends ? {
    labels: trends.map(t => t.date),
    datasets: [
      {
        label: 'Avg Temp (°C)',
        data: trends.map(t => t.avg_temperature),
        borderColor: 'rgba(75,192,192,1)',
        fill: false,
      },
      {
        label: 'Max Temp (°C)',
        data: trends.map(t => t.max_temperature),
        borderColor: 'rgba(255,99,132,1)',
        fill: false,
      },
      {
        label: 'Min Temp (°C)',
        data: trends.map(t => t.min_temperature),
        borderColor: 'rgba(54,162,235,1)',
        fill: false,
      },
    ],
  } : null;

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-3xl mx-auto">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold">Weather Dashboard</h1>
          <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded">Logout</button>
        </div>
        {view === 'dashboard' && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <SearchBar 
              city={city} 
              onCityChange={(e) => setCity(e.target.value)} 
              onSearch={fetchWeather} 
            />
            {weather && <WeatherCard data={weather} />}
            <div className="mt-4">
              <h2 className="text-2xl font-bold mb-2">Trends</h2>
              <div className="mb-4 flex items-center">
                <label className="mr-2">Select Days:</label>
                <select 
                  value={days} 
                  onChange={(e) => setDays(Number(e.target.value))} 
                  className="border p-2 rounded"
                >
                  <option value={7}>Last 7 days</option>
                  <option value={14}>Last 14 days</option>
                </select>
                <button 
                  onClick={fetchTrends} 
                  className="ml-4 bg-green-500 text-white px-4 py-2 rounded"
                >
                  Fetch Trends
                </button>
              </div>
              {trends && chartData && (
                <div className="bg-gray-50 p-4 rounded">
                  <Line data={chartData} />
                </div>
              )}
            </div>
            <div className="mt-4">
              <button 
                onClick={fetchHistory} 
                className="bg-gray-500 text-white px-4 py-2 rounded"
              >
                View History
              </button>
            </div>
            {error && <p className="text-red-500 mt-4">{error}</p>}
          </div>
        )}
        {view === 'history' && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <button 
              onClick={() => setView('dashboard')} 
              className="bg-blue-500 text-white px-4 py-2 rounded mb-4"
            >
              Back
            </button>
            {history && <WeatherHistory history={history} />}
            {error && <p className="text-red-500 mt-4">{error}</p>}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
