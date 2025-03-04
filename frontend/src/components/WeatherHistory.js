import React from 'react';

const WeatherHistory = ({ history }) => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-4">
      <h2 className="text-2xl font-bold mb-2">Weather History</h2>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-4 py-2">Date</th>
              <th className="border px-4 py-2">Temp (°C)</th>
              <th className="border px-4 py-2">Humidity (%)</th>
              <th className="border px-4 py-2">Wind (m/s)</th>
            </tr>
          </thead>
          <tbody>
            {history.map((record, index) => (
              <tr key={index} className="text-center">
                <td className="border px-4 py-2">{record.timestamp}</td>
                <td className="border px-4 py-2">{record.temperature}</td>
                <td className="border px-4 py-2">{record.humidity}</td>
                <td className="border px-4 py-2">{record.wind_speed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default WeatherHistory;
