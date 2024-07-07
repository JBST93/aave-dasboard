import React from 'react';

const Filter = ({ filter, setFilter }) => {
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
        }}
      />
    </div>
  );
};

export default Filter;
