function Socials() {
  return (
    <>
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg mb-6">
        <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-4">
          About Curve Finance
        </h2>
        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Curve Finance is a decentralized exchange (DEX) optimized for trading
          between closely correlated assets, such as stablecoins (USDT, USDC,
          DAI). It has expanded to support pools with volatile assets and
          introduced its own over-collateralized stablecoin, crvUSD.
          Additionally, Curve offers LlamaLend, a lending platform.
        </p>
        <div className="flex flex-row md:flex-row gap-4">
          <a
            href="https://twitter.com/CurveFinance"
            className="flex items-center justify-center py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            Twitter
          </a>
          <a
            href="https://gov.curve.fi/latest"
            className="flex items-center justify-center py-2 px-4 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            Governance
          </a>
          <a
            href="https://www.curve.fi/"
            className="flex items-center justify-center py-2 px-4 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
            target="_blank"
            rel="noopener noreferrer"
          >
            Website
          </a>
        </div>
      </div>
    </>
  );
}

export default Socials;
