import React from 'react';

const Filter = ({ filter, setFilter }) => {
  const handleButtonClick = (token) => {
    setFilter(token);
  };

  const handleClear = () => {
    setFilter('');
  };

  return (
    <>
      <div className="flex flex-col md:flex-row md:items-center">
        <div className="relative flex items-center md:flex-none md:w-1/3">
          <span className="absolute inset-y-0 left-0 flex items-center pl-3">
            <svg
              className="w-5 h-5 text-gray-500 dark:text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 103.5 10.5a7.5 7.5 0 0013.65 6.15z"
              ></path>
            </svg>
          </span>
          <input
            type="text"
            className="py-2 pl-10 pr-10 text-sm border border-gray-300 dark:border-teal-700 bg-white dark:bg-gray-800 text-black dark:text-white focus:outline-none focus:ring-1 focus:ring-yellow-500 dark:focus:ring-teal-600"
            placeholder="Search Token"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
        </div>
      </div>
    </>
  );
};

export default Filter;
