import FetchData from '../components/FetchData';

function StablecoinYield() {
  return (
    <>
      <h1 className="m-15">Stablecoin Rates</h1>
      <p>Get the latest yiedls on your stablecoins.</p>
      <FetchData />
    </>
  );
}

export default StablecoinYield;
