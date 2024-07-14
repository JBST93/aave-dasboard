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
          color: 'white',
          backgroundColor: 'black', // Assuming you want a dark background for contrast
        }}
      />
      <div
        className="button-group"
        style={{ display: 'flex', flexWrap: 'wrap' }}
      >
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

      <style jsx>{`
        .button-group {
          display: flex;
          flex-wrap: wrap;
        }
        @media (max-width: 600px) {
          .button-group {
            flex-direction: row;
            justify-content: space-between;
            margin-top: 10px; // Add space between input and buttons on mobile
          }
          .button-group button {
            flex: 1;
            margin-right: 5px;
            margin-bottom: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default Filter;
