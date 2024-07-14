import React from 'react';

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
      <div className="button-group">
        <button
          onClick={() => handleButtonClick('')}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            marginRight: '10px',
            cursor: 'pointer',
            color: 'white',
            backgroundColor: 'black', // Assuming you want a dark background for contrast
          }}
        >
          ALL
        </button>
        <button
          onClick={() => handleButtonClick('USDC')}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            marginRight: '10px',
            cursor: 'pointer',
            color: 'white',
            backgroundColor: 'black', // Assuming you want a dark background for contrast
          }}
        >
          USDC
        </button>
        <button
          onClick={() => handleButtonClick('USDT')}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            cursor: 'pointer',
            color: 'white',
            backgroundColor: 'black', // Assuming you want a dark background for contrast
          }}
        >
          USDT
        </button>
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
