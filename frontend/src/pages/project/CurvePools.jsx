import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';

import axios from 'axios';
import CurvePoolTable from './CurvePoolTable';
import InfoCard from '../../components/InfoCard';
import Filter from '../../components/Filter';
import Socials from '../../components/Socials';

const ProjectList = () => {
  const [pools, setPools] = useState([]);
  const [price, setPrice] = useState(0);
  const [mktCap, setMktCap] = useState(0);

  const [filter, setFilter] = useState([]);

  const [totalTvl, setTotalTvl] = useState(0);
  const [totalVolume, setTotalVolume] = useState(0);

  useEffect(() => {
    const fetchPools = async () => {
      try {
        const response = await axios.get(
          'https://www.tokendataview.com/api/curve-pools'
        );
        const fetchedPools = response.data.pools;
        const fetchedPrice = response.data.price;
        const fetchedMktCap = response.data.supply;

        const totalTvlAmount = fetchedPools.reduce(
          (sum, pool) => sum + pool.tvl,
          0
        );

        const totalVolume = fetchedPools.reduce(
          (sum, pool) => sum + pool.volume,
          0
        );

        setPools(fetchedPools);
        setMktCap(fetchedMktCap);
        setPrice(fetchedPrice);
        setTotalTvl(totalTvlAmount);
        setTotalVolume(totalVolume);
      } catch (error) {
        console.error(error.message);
      }
    };

    fetchPools();
  }, []);

  const formattedNumber = (base) => {
    if (base >= 1e9) {
      return (base / 1e9).toFixed(2) + ' Billion';
    } else if (base >= 1e6) {
      return (base / 1e6).toFixed(2) + ' Million';
    } else {
      return base.toLocaleString('en-US', {
        minimumFractionDigits: 2,
      });
    }
  };

  const formattedTvl = formattedNumber(totalTvl);
  const formattedVolume = formattedNumber(totalVolume);
  const formattedMktCap = formattedNumber(mktCap);

  const clearFilter = () => {
    setFilter('');
    console.log('RESET');
  };

  return (
    <>
      <Helmet>
        <title>Curve Finance - Yield and Pool Data</title>
        <meta
          name="description"
          content="Explore Curve Finance pools, total value locked (TVL), and trading volume. Learn about the yield sources on Curve and access detailed pool data."
        />
        <meta
          name="keywords"
          content="Curve Finance, DEX, Stablecoins, Yield, TVL, Trading Volume, crvUSD, LlamaLend"
        />
      </Helmet>

      <h1>Curve Finance</h1>

      <Socials className="pb-4" />

      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg mb-4">
        <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-4">
          Where Does the Yield from Curve Comes From?
        </h2>
        <ul className="list-disc list-inside text-gray-700 dark:text-gray-300">
          <li className="mb-2">
            <span className="font-medium">
              <strong>Trading Fees </strong>: Trades on Curve costs 0.04% in
              fees, 50% of which go to Liquidity Providers and the rest to veCRV
              holders.
            </span>
          </li>
          <li className="mb-2 font-medium">
            <strong>CRV Token Rewards</strong>: Rate of CRV token receiced when
            stakes his LP position into the rewards gauge.
          </li>
          <li className="font-medium">
            <strong>Incentives Rewards:</strong> Some pools also choose to
            stream rewards in the form of a different token.
          </li>
        </ul>
      </div>

      <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-4">
        Key Statistics:
      </h2>

      <div className="md:flex md:gap-4 pb-4">
        <InfoCard
          title="Total Value Locked (TVL)"
          value={formattedTvl}
          scale="USD"
        />

        <InfoCard
          title="24h Volume"
          value={formattedVolume}
          scale="USD"
        />

        <InfoCard
          title="CRV Price "
          value={price}
          scale="USD"
        />
        <InfoCard
          title="Market Cap "
          value={formattedMktCap}
          scale="USD"
        />
      </div>

      <div>
        <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-4">
          Detailed Curve Pools Data
        </h2>

        <CurvePoolTable rows={pools} />
      </div>

      <div>
        CRV is the governance token of Curve Finance, one of the leading
        decentralized exchange (DEX) in the DeFi ecosystem. With a current price
        of $ {price}, CRV has a market capitalization of {mktCap}. Curve has a
        Total Value Locked of {totalTvl} and a Total Volume of {totalVolume},
        with a utilization ratio of
        {totalVolume / totalTvl} %.
      </div>
    </>
  );
};

export default ProjectList;
