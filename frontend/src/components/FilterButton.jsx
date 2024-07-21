import React from 'react';

// Helper function to get the token icon URL
const getTokenIconUrl = (symbol) => {
  return `https://cdn.jsdelivr.net/gh/atomiclabs/cryptocurrency-icons@1a63530be6e374711a8554f31b17e4cb92c25fa5/32@2x/color/${symbol.toLowerCase()}@2x.png`;
};

const FilterButton = ({ token, onClick, label }) => (
  <button
    className="flex items-center justify-center focus:outline-none font-semibold text-black dark:text-white bg-yellow-400 dark:bg-teal-700 hover:bg-yellow-500 dark:hover:bg-teal-500 focus:ring-4 focus:ring-yellow-300 dark:focus:ring-yellow-900 rounded-lg text-sm px-4 p-2 m-1"
    onClick={() => onClick(token)}
  >
    {token && (
      <img
        src={getTokenIconUrl(token)}
        alt={token}
        className="w-5 h-5 mr-2"
      />
    )}
    {label || token || 'ALL'}
  </button>
);

export default FilterButton;
