import FetchData from '../components/FetchData';
import AverageYieldRate from '../components/AverageRate';

const StablecoinYield = () => {
  return (
    <>
      <div className="px-4">
        <div className="flex justify-between items-center">
          <h1 className="md:text-4xl text-xl font-bold">Stablecoin Rates</h1>
        </div>
        <div className="mb-4 text-center md:text-left">
          <p className="md:text-lg text-base text-left">
            We aggregate interest rates and yields, ensuring you always have
            access to the highest yields. Discover the best rates in real-time
            and make informed investment decisions effortlessly.
          </p>
          <p className="text-sm text-left	 text-gray-500">
            Disclaimer: We do not vet or audit the platforms we aggregate.
            Always conduct your own due diligence before making any investment
            decisions.
          </p>
        </div>
      </div>

      <FetchData />
    </>
  );
};

export default StablecoinYield;
