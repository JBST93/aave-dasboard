import { useEffect, useState, useMemo } from 'react';
import fetchData from '../utils/fetch_data';
import DataTable from '../components/DataTable';
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

      <div className="w-full md:max-w-sm p-4 my-2 bg-white border shadow dark:bg-gray-800 border-gray-300 dark:border-teal-700">
        <div className="flex items-center gap-2">
          <svg
            className="w-7 h-7 text-gray-500 dark:text-gray-400"
            height="64"
            viewBox="0 0 64 64"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
          >
            <circle
              cx="16"
              cy="16"
              r="6"
            />
            <circle
              cx="48"
              cy="48"
              r="6"
            />
            <line
              x1="16"
              y1="48"
              x2="48"
              y2="16"
              stroke="currentColor"
              strokeWidth="4"
            />
          </svg>
          <h5 className="md:text-xl text-xl font-semibold tracking-tight text-gray-900 dark:text-white">
            DeFi Base Rate
          </h5>
        </div>
        <p className="text-2xl font-medium text-gray-900 dark:text-white py-2">
          {avgRate}%
        </p>
        <p className="text-xs md:text-sm text-gray-500 dark:text-gray-400">
          Based on the average yields of USDC, USDT, and DAI across pools with
          more than $500 million in TVL (Total Value Locked).
        </p>
      </div>

      <div className="flex flex-wrap md:flex-nowrap items-center py-2 space-y-2 md:space-y-0 md:space-x-2">
        <Filter
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

        <div className="flex flex-col md:flex-row md:items-center max-w-full w-full md:w-2/5">
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
              placeholder="Minimum APY"
              value={numericalFilter}
              onChange={(e) => setNumericalFilter(e.target.value)}
            />
          </div>
        </div>

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
        <DataTable rows={filteredData} />
      </div>
    </>
  );
};

export default StablecoinYield;
