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

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/stablecoin_yield_rates');
        console.log(response);
        console.log(data);

        const transformedData = response.data.map((item, index) => ({
          ...item,
          sequentialId: index + 1,
          id: item.id,
          tvl_formatted2: Math.round(item.tvl),
          yield_rate_reward_formatted:
            item.yield_rate_reward === null || item.yield_rate_reward === 0
              ? ''
              : item.yield_rate_reward.toFixed(2),
          apy_sum: (
            parseFloat(item.yield_rate_base) +
            (item.yield_rate_reward ? parseFloat(item.yield_rate_reward) : 0)
          ).toFixed(2),
          information_formatted: item.information
            ? item.information.join(', ')
            : '',
        }));

        setData(transformedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const filteredData = data.filter((item) =>
    item.market.toLowerCase().includes(filter.toLowerCase())
  );

  useEffect(() => {
    const calculateAverageRate = (dataToProcess) => {
      if (dataToProcess && dataToProcess.length > 0) {
        const filteredData = dataToProcess.filter(
          (item) => item.tvl_formatted2 > 500000000
        );
        const totalSum = filteredData.reduce((sum, item) => {
          const rate =
            typeof item.yield_rate_base === 'number' ? item.yield_rate_base : 0;
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
            typeof item.yield_rate_base === 'number' ? item.yield_rate_base : 0;
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
    <div className="min-h-screen">
      <div className="pb-0">
        <div className="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-4 md:mb-0">
          <AverageYieldRate
            title="DeFi Base Yield"
            description="The average yield rate for assets with TVL greater than 500 million across all of DeFi."
            data={avgRate}
            input="%"
            className="w-2/3 md:w-1/3"
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
            description="The FED rate is the risk-free rate, representing the return on low-risk investments like government bonds. The difference between this rate and the yields listed here is the risk premium, which compensates for the higher risk associated with DeFi investments."
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
