import React, { useEffect, useState, Suspense } from 'react';
import axios from '../api/axios';

import DataTable from '../components/DataTableStablecoin';
import AverageYieldRate from '../components/AverageRate';

function StablecoinInfo() {
  const [data, setData] = useState([]);
  const [summaryInfo, setSummaryInfo] = useState({
    centralised_dominance_percentage: '0%',
    total_supply: '0',
    total_tokens: 0,
    usd_dominance_percentage: '0%',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('api/stablecoin_info');
        const dataset = response.data.stablecoin_info;
        const summaryData = response.data.summary_info;

        const transformedData = dataset.map((item, index) => ({
          ...item,
          sequentialId: index + 1,
          off_peg: (((item.price - 1) / 1) * 100).toFixed(2),
          price_formatted: parseFloat(item.price).toFixed(4),
        }));

        setData(transformedData);
        setSummaryInfo(summaryData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <div className="flex justify-between items-center">
        <h1 className="md:text-4xl text-xl font-bold">Stablecoins </h1>
      </div>

      <div className="mb-4 text-center md:text-left">
        <p className="md:text-lg text-base text-left pt-1">
          Explore a complete list of both centralized and decentralized
          stablecoins, all in one place. Our directory offers detailed
          statistics and insights to help you navigate the stablecoin landscape
          with ease.
        </p>
        <p className="text-sm text-left text-gray-500">
          Disclaimer: We do not vet or audit the platforms we aggregate. Always
          conduct your own due diligence before making any investment decisions.
        </p>
      </div>

      <div className="flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-4 md:mb-0 pb-4">
        <AverageYieldRate
          title="# Stablecoin"
          data={summaryInfo.total_tokens}
          className="w-2/3 md:w-1/3"
        />
        <AverageYieldRate
          title="USD Dominance"
          data={summaryInfo.usd_dominance_percentage}
          className="w-2/3 md:w-1/3"
        />
        <AverageYieldRate
          title="Total Supply"
          data={summaryInfo.total_supply}
          className="w-2/3 md:w-1/3"
        />
        <AverageYieldRate
          title="Centralised Stablecoins Dominance"
          data={summaryInfo.centralised_dominance_percentage}
          className="w-2/3 md:w-1/3"
        />
      </div>

      <Suspense fallback={<div>Loading data...</div>}>
        <DataTable rows={data} />
      </Suspense>
    </>
  );
}

export default StablecoinInfo;
