import React from 'react';

const getTokenIconUrl = (symbol) => {
  return `https://cdn.jsdelivr.net/gh/atomiclabs/cryptocurrency-icons@1a63530be6e374711a8554f31b17e4cb92c25fa5/32@2x/color/${symbol.toLowerCase()}@2x.png`;
};

const FilterButton = ({ token, onClick }) => (
  <button
    className="flex items-center focus:outline-none font-semibold text-black dark:text-white bg-yellow-400 dark:bg-teal-700 hover:bg-yellow-500 dark:hover:bg-teal-500 focus:ring-4 focus:ring-yellow-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 md:mb-0"
    onClick={() => onClick(token)}
  >
    {token && (
      <img
        src={getTokenIconUrl(token)}
        alt={token}
        style={{ width: '20px', marginRight: '8px' }}
      />
    )}
    {token || 'ALL'}
  </button>
);

export default FilterButton;
