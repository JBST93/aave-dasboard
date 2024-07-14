import React from 'react';

// Helper function to get the token icon URL
const getTokenIconUrl = (symbol) => {
  return `https://cdn.jsdelivr.net/gh/atomiclabs/cryptocurrency-icons@1a63530be6e374711a8554f31b17e4cb92c25fa5/32@2x/color/${symbol.toLowerCase()}@2x.png`;
};

const FilterButton = ({ token, onClick }) => (
  <button
    onClick={() => onClick(token)}
    style={{
      padding: '10px 20px',
      fontSize: '16px',
      borderRadius: '4px',
      border: '1px solid #ccc',
      marginRight: '10px',
      cursor: 'pointer',
      color: 'white',
      backgroundColor: 'black', // Assuming you want a dark background for contrast
      display: 'flex',
      alignItems: 'center',
    }}
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
