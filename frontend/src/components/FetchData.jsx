import React, { useEffect, useState, Suspense } from 'react';
import axios from '../api/axios';
import AverageYieldRate from '../components/AverageRate';
import TableFilter from './TableFilter';

const DataTable = React.lazy(() => import('./DataTable'));
const Filter = React.lazy(() => import('./Filter'));

const FetchData = () => {
  const [data, setData] = useState();
  const [filter, setFilter] = useState();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/stablecoin_yield_rates');
        console.log(response);

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
          information_formatted: Array.isArray(item.information)
            ? item.information.join(', ')
            : item.information || '',
        }));

        setData(transformedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleFilterChange = (filters) => {
    const { tokens, chains, minApy, minAmountSupplied } = filters;
    const filtered = data.filter((item) => {
      return (
        (tokens.length === 0 || tokens.includes(item.token)) &&
        (chains.length === 0 || chains.includes(item.chain)) &&
        item.apy >= minApy &&
        item.amountSupplied >= minAmountSupplied
      );
    });
    setFilter(filtered);
  };

  return (
    <>
      <TableFilter
        data={data}
        onFilterChange={handleFilterChange}
      />

      <div className="min-h-screen">
        <Suspense fallback={<div>Loading filter...</div>}>
          <Filter
            filter={filter}
            setFilter={setFilter}
          />
        </Suspense>
        <div className="container mx-auto">
          <Suspense fallback={<div>Loading data...</div>}>
            <DataTable rows={data} />
          </Suspense>
        </div>
      </div>
    </>
  );
};

export default FetchData;
