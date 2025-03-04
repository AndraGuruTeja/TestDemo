import React from 'react';

const SearchBar = ({ city, onCityChange, onSearch }) => (
  <div className="flex gap-2 mb-4">
    <input
      type="text"
      placeholder="Enter city name"
      className="flex-1 p-2 border rounded-lg"
      value={city}
      onChange={onCityChange}
    />
    <button
      onClick={onSearch}
      className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
    >
      Search
    </button>
  </div>
);

export default SearchBar;