import React, { useEffect, useState, Suspense } from 'react';
import axios from '../api/axios';
import AverageYieldRate from '../components/AverageRate';

const DataTable = React.lazy(() => import('./DataTable'));
const Filter = React.lazy(() => import('./Filter'));

const FetchData = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState('');
  const [avgRate, setAvgRate] = useState('');
  const [filteredAvgRate, setFilteredAvgRate] = useState('');

  const transformCollateral = (collateral) => {
    if (collateral === null) {
      return '';
    } else if (Array.isArray(collateral)) {
      if (collateral.length === 1) {
        return collateral[0];
      } else {
        return collateral.join(', ');
      }
    }
    return collateral;
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/liquidity_rates');

        const transformedData = response.data.map((item, index) => ({
          ...item,
          sequentialId: index + 1,
          id: item.id,
          tvl_formatted2: Math.round(item.tvl),
          liquidity_reward_rate_formatted:
            item.liquidity_reward_rate === null ||
            item.liquidity_reward_rate === 0
              ? ''
              : item.liquidity_reward_rate.toFixed(2),
          apy_sum: (
            parseFloat(item.liquidity_rate) +
            (item.liquidity_reward_rate
              ? parseFloat(item.liquidity_reward_rate)
              : 0)
          ).toFixed(2),
          collateral_formatted: transformCollateral(item.collateral),
        }));

        setData(transformedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const filteredData = data.filter((item) =>
    item.token.toLowerCase().includes(filter.toLowerCase())
  );

  useEffect(() => {
    const calculateAverageRate = (dataToProcess) => {
      if (dataToProcess && dataToProcess.length > 0) {
        const filteredData = dataToProcess.filter(
          (item) => item.tvl_formatted2 > 500000000
        );
        const totalSum = filteredData.reduce((sum, item) => {
          const rate =
            typeof item.liquidity_rate === 'number' ? item.liquidity_rate : 0;
          return sum + rate;
        }, 0);

        const numberOfEntries = filteredData.length;
        const average = numberOfEntries > 0 ? totalSum / numberOfEntries : 0;
        return average.toFixed(2);
      } else {
        return 0;
      }
    };

    setAvgRate(calculateAverageRate(data));
  }, [data]);

  useEffect(() => {
    const calculateAverageRate = (dataToProcess) => {
      if (dataToProcess && dataToProcess.length > 0) {
        const totalSum = dataToProcess.reduce((sum, item) => {
          const rate =
            typeof item.liquidity_rate === 'number' ? item.liquidity_rate : 0;
          return sum + rate;
        }, 0);

        const numberOfEntries = dataToProcess.length;
        const average = numberOfEntries > 0 ? totalSum / numberOfEntries : 0;
        return average.toFixed(2);
      } else {
        return 0;
      }
    };

    setFilteredAvgRate(calculateAverageRate(filteredData));
  }, [filteredData]);

  return (
    <div className="min-h-screen p-4 bg-white dark:bg-gray-900 text-black dark:text-white">
      <div className="pb-4">
        <div className="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-4 mb-4 md:mb-0">
          <AverageYieldRate
            title="DeFi Base Yield"
            description="The average yield rate for assets with TVL greater than 500 million across all of DeFi."
            data={avgRate}
            input="%"
            className="w-2/3 pt-0 md:w-1/3"
          />
          <AverageYieldRate
            title="Selection Average Yield"
            description="The average yield rate from your selection, including those with TVL less than 500 million."
            data={filteredAvgRate}
            input="%"
            className="hidden md:block w-full md:w-1/3"
          />
          <AverageYieldRate
            title="FED Rate"
            description="The average yield rate from your selection, including those with TVL less than 500 million."
            data="5.3"
            input="%"
            className="hidden md:block w-full md:w-1/3"
          />
        </div>
      </div>
      <Suspense fallback={<div>Loading filter...</div>}>
        <Filter
          filter={filter}
          setFilter={setFilter}
        />
      </Suspense>

      <Suspense fallback={<div>Loading data...</div>}>
        <DataTable rows={filteredData} />
      </Suspense>
    </div>
  );
};

export default FetchData;
