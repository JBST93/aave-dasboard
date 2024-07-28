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
