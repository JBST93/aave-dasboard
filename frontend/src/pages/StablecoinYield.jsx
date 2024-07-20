import FetchData from '../components/FetchData';
import AverageYieldRate from '../components/AverageRate';

const StablecoinYield = ({ data }) => {
  const { averageYield } = 5;

  return (
    <>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-4xl font-bold">Stablecoin Rates</h1>
        <div className="flex space-x-4">
          <AverageYieldRate averageYield="5" />{' '}
        </div>
      </div>

      <FetchData />
    </>
  );
};

export default StablecoinYield;
