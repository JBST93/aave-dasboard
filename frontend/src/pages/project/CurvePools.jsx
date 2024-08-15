import { useEffect, useState } from 'react';
import axios from 'axios';
import CurvePoolTable from './CurvePoolTable';

const ProjectList = () => {
  const [pools, setPools] = useState([]);

  useEffect(() => {
    const fetchPools = async () => {
      try {
        const response = await axios.get(
          'https://www.tokendataview.com/api/curve-pools'
        );
        setPools(response.data);
      } catch (error) {
        error.message;
      }
    };

    fetchPools();
  }, []);

  return (
    <>
      <div className="flex justify-between items-center flex-wrap">
        <h1 className="md:text-4xl text-xl font-bold">Curve Pools</h1>
      </div>

      <div className="mb-4 text-center md:text-left">
        <p className="md:text-lg text-base text-left pt-1">
          Our comprehensive list of DeFi projects. Here you can find detailed
          information about various decentralized finance (deFi) protocols Click
          on the buttons to visit their websites and forums for more
          information.
        </p>
        <p className="text-sm text-left text-gray-500">
          Disclaimer: We do not vet or audit the platforms we aggregate. Always
          conduct your own due diligence before making any investment decisions.
        </p>
      </div>

      <CurvePoolTable rows={pools} />
    </>
  );
};

export default ProjectList;
