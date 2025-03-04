// import React, { useState } from 'react';
// import axios from 'axios';
// import SearchBar from './components/SearchBar';
// import WeatherCard from './components/WeatherCard';
// import './styles.css';

// function App() {
//   const [city, setCity] = useState('');
//   const [weather, setWeather] = useState(null);
//   const [error, setError] = useState('');

//   const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

//   const fetchWeather = async () => {
//     try {
//       const response = await axios.get(`${API_URL}/weather/${city}`);
//       setWeather(response.data);
//       setError('');
//     } catch (err) {
//       setError('Error fetching weather data');
//       setWeather(null);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gray-100 p-4">
//       <div className="max-w-md mx-auto">
//         <h1 className="text-3xl font-bold mb-4 text-center">Weather Monitor</h1>
//         <SearchBar 
//           city={city}
//           onCityChange={(e) => setCity(e.target.value)}
//           onSearch={fetchWeather}
//         />
//         {error && <p className="text-red-500 text-center">{error}</p>}
//         {weather && <WeatherCard data={weather} />}
//       </div>
//     </div>
//   );
// }

// export default App;









import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
import Dashboard from './components/Dashboard';

function App() {
  const isAuthenticated = !!localStorage.getItem('access_token');

  return (
    <Router>
      <Routes>
        <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
        <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} />
        <Route path="/signup" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Signup />} />
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
