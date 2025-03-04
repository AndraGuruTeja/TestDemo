import React from 'react';
import clearSky from '../assets/clear-sky.png';
import fewClouds from '../assets/few-clouds.png';
import overcastClouds from '../assets/overcast-clouds.png';
import smoke from '../assets/smoke.png';
import brokenClouds from '../assets/broken-image.png';
import scatteredClouds from '../assets/scattered-clouds.png';
import rain from '../assets/rain.png';
import defaultImage from '../assets/default.png';

const WeatherCard = ({ data }) => {
  let backgroundImage;

  switch (data.description.toLowerCase()) {
    case 'clear sky':
      backgroundImage = clearSky;
      break;
    case 'few clouds':
      backgroundImage = fewClouds;
      break;
    case 'overcast clouds':
      backgroundImage = overcastClouds;
      break;
    case 'smoke':
      backgroundImage = smoke;
      break;
    case 'broken clouds':
      backgroundImage = brokenClouds;
      break;
    case 'scattered clouds':
      backgroundImage = scatteredClouds;
      break;
    case 'rain':
      backgroundImage = rain;
      break;
    default:
      backgroundImage = defaultImage;
      break;
  }

  return (
    <div
      className="bg-white rounded-lg shadow-lg p-6 mt-4"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <h2 className="text-2xl font-bold mb-2">{data.city}</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-gray-600">Temperature</p>
          <p className="text-xl">{data.temperature}°C</p>
        </div>
        <div>
          <p className="text-gray-600">Humidity</p>
          <p className="text-xl">{data.humidity}%</p>
        </div>
        <div>
          <p className="text-gray-600">Wind Speed</p>
          <p className="text-xl">{data.wind_speed} m/s</p>
        </div>
        <div>
          <p className="text-gray-600">Conditions</p>
          <p className="text-xl capitalize">{data.description}</p>
        </div>
      </div>
      {/* {data.cached && (
        <p className="mt-4 text-sm text-blue-500">Served from cache</p>
      )} */}
    </div>
  );
};

export default WeatherCard;
