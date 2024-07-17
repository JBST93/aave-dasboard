import React, { useEffect, useState, Suspense } from 'react';
import axios from '../api/axios';

const DataTable = React.lazy(() => import('./DataTable'));
const Filter = React.lazy(() => import('./Filter'));

const FetchData = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/liquidity_rates');

        // Transform data to include sequential IDs
        const transformedData = response.data.map((item, index) => ({
          ...item,
          sequentialId: index + 1, // Add a sequential ID starting from 1
          id: item.id, // Ensure each row has a unique `id` field for DataGrid
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
          ).toFixed(2), // Calculate APY sum
        }));

        setData(transformedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  // Filter the data based on the filter input
  const filteredData = data.filter((item) =>
    item.token.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
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
