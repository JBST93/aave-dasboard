import React from 'react';
import FilterButton from './FilterButton';

const Filter = ({ filter, setFilter }) => {
  const handleButtonClick = (token) => {
    setFilter(token);
  };

  return (
    <>
      <div className="flex flex-col md:flex-row w-full md:w-auto pb-2">
        <input
          type="text"
          placeholder="Type the ticker of the token you're looking"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="w-full md:w-auto my-2 md:mb-0 bg-white  dark:bg-black"
        />
        <div className="flex flex-wrap p-2 justify-start  md:justify-start space-x-2">
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
          <FilterButton
            token="DAI"
            onClick={handleButtonClick}
          />
        </div>
      </div>
    </>
  );
};

export default Filter;
