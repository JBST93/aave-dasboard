import React, { useEffect, useState, Suspense } from 'react';
import axios from '../api/axios';

import DataTable from '../components/DataTableStablecoin';
import AverageYieldRate from '../components/AverageRate';
import FilterButton from '../components/FilterButton';

function EthereumYield() {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState('');

  const [summaryInfo, setSummaryInfo] = useState({
    lido_dominance_percentage: '0%',
    total_supply: '0',
    total_tokens: 0,
    usd_dominance_percentage: '0%',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/eth_yiel_rates');
        const dataset = response.data.eth_yield;
        const summaryData = response.data.summary_info;

        const transformedData = dataset.map((item, index) => ({
          ...item,
          sequentialId: index + 1,
          off_peg: (((item.price_peg - 1) / 1) * 100).toFixed(2),
          price_usd_formatted: parseFloat(item.price_usd).toFixed(4),
          price_peg_formatted: parseFloat(item.price_peg).toFixed(4),
        }));

        setData(transformedData);
        setSummaryInfo(summaryData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const filteredData = data.filter((item) =>
    item.pegged_against.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <>
      <div className="flex justify-between items-center">
        <h1 className="md:text-4xl text-xl font-bold">
          Ethereum (ETH) Yields{' '}
        </h1>
      </div>

      <div className="mb-4 text-center md:text-left">
        <p className="md:text-lg text-base text-left pt-1">
          Unlock the potential of your Ethereum holdings with our real-time ETH
          yield aggregation service. By accessing the highest yields available,
          ensure your investments are always working their hardest for you.
          Effortlessly discover the best ETH yields and maximize your returns.
        </p>
        <p className="text-sm text-left text-gray-500">
          Disclaimer: We do not vet or audit the platforms we aggregate. Always
          conduct your own due diligence before making any investment decisions.
        </p>
      </div>

      <div className="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-4 md:mb-0 pb-4">
        <AverageYieldRate
          title="# ETH in circulation"
          data={summaryInfo.total_tokens}
          className="w-2/3 md:w-1/3"
        />
        <AverageYieldRate
          title="Total Supply"
          data={summaryInfo.total_supply}
          className="w-2/3 md:w-1/3"
        />
        <AverageYieldRate
          title="Lido Dominance"
          data={summaryInfo.centralised_dominance_percentage}
          className="w-2/3 md:w-1/3"
        />
      </div>

      <div className="flex flex-wrap justify-start md:mt-0">
        <FilterButton onClick={() => setFilter('')} />
        <FilterButton
          token="USD"
          onClick={() => setFilter('USD')}
        />
        <FilterButton
          token="EUR"
          onClick={() => setFilter('EUR')}
        />
      </div>

      <Suspense fallback={<div>Loading data...</div>}>
        <DataTable rows={filteredData} />
      </Suspense>
    </>
  );
}

export default EthereumYield;
