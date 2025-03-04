import React from 'react';

const WeatherTrends = ({ trends }) => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-4">
      <h2 className="text-2xl font-bold mb-2">Weather Trends</h2>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-4 py-2">Date</th>
              <th className="border px-4 py-2">Avg Temp (°C)</th>
              <th className="border px-4 py-2">Max Temp (°C)</th>
              <th className="border px-4 py-2">Min Temp (°C)</th>
              <th className="border px-4 py-2">Avg Humidity (%)</th>
            </tr>
          </thead>
          <tbody>
            {trends.map((trend, index) => (
              <tr key={index} className="text-center">
                <td className="border px-4 py-2">{trend.date}</td>
                <td className="border px-4 py-2">{trend.avg_temperature}</td>
                <td className="border px-4 py-2">{trend.max_temperature}</td>
                <td className="border px-4 py-2">{trend.min_temperature}</td>
                <td className="border px-4 py-2">{trend.avg_humidity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default WeatherTrends;
