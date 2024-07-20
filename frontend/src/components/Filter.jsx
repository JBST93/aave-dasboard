import React from 'react';
import FilterButton from './FilterButton';

const Filter = ({ filter, setFilter }) => {
  const handleButtonClick = (token) => {
    setFilter(token);
  };

  return (
    <div style={{ marginBottom: '20px' }}>
      <input
        type="text"
        placeholder="Filter by token..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        style={{
          padding: '10px',
          fontSize: '16px',
          width: '300px',
          borderRadius: '4px',
          border: '1px solid #ccc',
          marginBottom: '10px', // Ensure spacing between input and buttons on mobile
        }}
      />
      <div className="button-group flex">
        <FilterButton
          token=""
          onClick={handleButtonClick}
        />
        <FilterButton
          token="USDC"
          onClick={handleButtonClick}
        />
        <FilterButton
          token="USDT"
          onClick={handleButtonClick}
        />
      </div>
    </div>
  );
};

export default Filter;
