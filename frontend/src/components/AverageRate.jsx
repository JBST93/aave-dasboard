import React from 'react';

const AverageYieldRate = ({ averageYield }) => (
  <div className="bg-white dark:bg-gray-700 p-4 rounded-lg shadow-md text-black dark:text-white">
    <h2 className="text-lg font-semibold">Average Yield Rate</h2>
    <p className="text-2xl">{averageYield}%</p>
  </div>
);

export default AverageYieldRate;
