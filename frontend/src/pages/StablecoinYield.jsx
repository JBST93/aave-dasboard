import { Suspense, lazy, useEffect, useState } from 'react';
import fetchData from '../utils/fetch_data';
const DataTable = lazy(() => import('../components/DataTable'));

import InfoCard from '../components/InfoCard';
import Filter from '../components/Filter';
import InputFilter from '../components/InputFilter';

const StablecoinYield = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState('');
  const [numericalFilter, setNumericalFilter] = useState('');
  const [dataCount, setDataCount] = useState(0);
  const [selectedBlockchains, setSelectedBlockchains] = useState([]);
  const [avgRate, setAvgRate] = useState(0);

  useEffect(() => {
    const getData = async () => {
      const transformedData = await fetchData('/stablecoin_yield_rates');
      setData(transformedData);
    };
    getData();
  }, []);

  const filteredData = data.filter((item) => {
    const yieldRateBase = parseFloat(item.yield_rate_base);
    const filterValue = parseFloat(numericalFilter);

    const matchesTextFilter = item.market
      .toLowerCase()
      .includes(filter.toLowerCase());
    const matchesNumericalFilter =
      isNaN(filterValue) || yieldRateBase >= filterValue;
    const matchesBlockchainFilter =
      selectedBlockchains.length === 0 ||
      selectedBlockchains.includes(item.chain);

    return (
      matchesTextFilter && matchesNumericalFilter && matchesBlockchainFilter
    );
  });

  const clearFilter = () => {
    setFilter('');
    setNumericalFilter('');
    setSelectedBlockchains([]);
  };

  useEffect(() => {
    setDataCount(filteredData.length);
  }, [filteredData]);

  useEffect(() => {
    const filteredYieldData = filteredData.filter(
      (item) =>
        (item.market === 'USDC' ||
          item.market === 'DAI' ||
          item.market === 'USDT') &&
        parseFloat(item.tvl) > 500000000
    );

    if (filteredYieldData.length > 0) {
      const total_yield = filteredYieldData.reduce(
        (acc, currentValue) => acc + parseFloat(currentValue.yield_rate_base),
        0
      );
      const res = total_yield / filteredYieldData.length;
      setAvgRate(res.toFixed(2));
    } else {
      setAvgRate(0);
    }
  }, [data]);

  return (
    <>
      <div className="flex justify-between items-center flex-wrap">
        <h1 className="md:text-4xl text-xl font-bold">Stablecoin Rates</h1>
      </div>
      <div className="mb-4 text-center md:text-left">
        <p className="md:text-lg text-base text-left pt-1">
          We aggregate interest rates and yields, ensuring you always have
          access to the highest yields. Discover the best rates in real-time and
          make informed investment decisions effortlessly.
        </p>
        <p className="text-sm text-left text-gray-500">
          Disclaimer: We do not vet or audit the platforms we aggregate. Always
          conduct your own due diligence before making any investment decisions.
        </p>
      </div>

      <InfoCard
        title="DeFi Base Rate"
        description="Based on the average yields of USDC, USDT, and DAI across pools with
        more than $500 million in TVL (Total Value Locked)."
        value={avgRate}
      />

      <div className="flex flex-wrap md:flex-nowrap items-center py-2 space-y-2 md:space-y-0 md:space-x-2">
        <Filter
          placeholder="Search Token"
          filter={filter}
          setFilter={setFilter}
          className="flex-grow py-2 border border-gray-300"
        />

        <div className="w-full md:flex-grow md:px-2 focus:outline-none focus:ring-1 focus:ring-yellow-500 dark:focus:ring-teal-600">
          <InputFilter
            data={data}
            setSelectedBlockchains={setSelectedBlockchains}
            resetFilter={clearFilter}
          />
        </div>

        <Filter
          placeholder="Minimum APY"
          filter={numericalFilter}
          setFilter={setNumericalFilter}
          className="flex-grow py-2 border border-gray-300"
        />

        <div className="w-full md:w-auto md:px-2">
          <button
            className="w-full py-2 px-4 text-sm dark:bg-teal-700 text-black dark:text-white focus:outline-none focus:ring-2 bg-yellow-500"
            onClick={clearFilter}
          >
            Reset
          </button>
        </div>
      </div>
      <div>
        <p>{dataCount} results found</p>
        <Suspense fallback={<div>Loading...</div>}>
          <DataTable rows={filteredData} />
        </Suspense>
      </div>
    </>
  );
};

export default StablecoinYield;
