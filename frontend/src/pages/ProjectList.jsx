import { useEffect, useState } from 'react';
import axios from 'axios';
import Filter from '../components/Filter';
import ProjectDataTable from '../components/ProjectDataTable';
import InfoCard from '../components/InfoCard';

import { Typography } from '@mui/material';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [filter, setFilter] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await axios.get(
          'https://www.tokendataview.com/api/projects'
        );
        setProjects(response.data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchProjects();
  }, []);

  const topGainers = [...projects]
    .filter((project) => project.price_day_delta < 99)
    .sort((a, b) => b.price_day_delta - a.price_day_delta)
    .slice(0, 3);

  // Filtering top 3 losers
  const topLosers = [...projects]
    .sort((a, b) => a.price_day_delta - b.price_day_delta)
    .slice(0, 3);

  const filteredProjects = projects.filter((project) => {
    const searchTerm = filter.toLocaleLowerCase();
    return (
      project.token.toLocaleLowerCase().includes(searchTerm) ||
      project.project.toLocaleLowerCase().includes(searchTerm) ||
      project.type.toLocaleLowerCase().includes(searchTerm)
    );
  });

  if (error) {
    return (
      <Typography
        variant="h2"
        color="error"
      >
        Error: {error}
      </Typography>
    );
  }

  return (
    <>
      <div className="flex justify-between items-center flex-wrap">
        <h1 className="md:text-5xl text-3xl font-extrabold text-gray-800 dark:text-white tracking-tight md:tracking-wide text-center md:text-left">
          Project Directory
        </h1>
      </div>

      <div className="mb-8 text-center md:text-left">
        <p className="md:text-xl text-lg text-left pt-2 leading-relaxed dark:text-white text-gray-700 md:text-gray-600 border-l-4 border-yellow-300 pl-4">
          Navigate the world of digital assets with our comprehensive directory.
          Explore real-time data on your favorite cryptocurrencies, compare
          market performance, and stay ahead with the latest updates.
        </p>
      </div>

      <div className="flex flex-col md:flex-row gap-8 items-center">
        {/* <div className="flex flex-col md:w-3/3 w-full">
          <InfoCard
            title="Total Market Cap"
            description=""
            value="5"
          /> */}
        {/* </div> */}

        <div className="flex flex-col md:flex-row gap-4 mb-4 w-full">
          <div className="">
            <h2 className="text-lg font-semibold mb-2">⬆ Daily Gainers</h2>
            <table className=" bg-white border shadow dark:bg-gray-800 border-gray-300 dark:border-gray-800 min-w-full text-black dark:text-white text-left">
              <thead>
                <tr>
                  <th className="py-2 px-4">Token</th>
                  <th className="py-2 px-4">Price Change</th>
                </tr>
              </thead>
              <tbody>
                {topGainers.map((project) => (
                  <tr key={project.token}>
                    <td className="py-2 px-4 flex">
                      {project.logo && (
                        <img
                          src={project.logo}
                          alt={`${project.token} logo`}
                          className="mr-2 w-6 h-6"
                        />
                      )}
                      {project.token}
                    </td>
                    <td className="py-2 px-4 text-green-600">
                      {project.price_day_delta}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-2">⬇ Top Daily Losers</h2>
            <table className="min-w-full  bg-white border shadow dark:bg-gray-800 dark:border-gray-800 border-gray-300 text-black dark:text-white text-left">
              <thead>
                <tr>
                  <th className="py-2 px-4">Token</th>
                  <th className="py-2 px-4">Price Change</th>
                </tr>
              </thead>
              <tbody>
                {topLosers.map((project) => (
                  <tr key={project.token}>
                    <td className="py-2 px-4 flex">
                      {project.logo && (
                        <img
                          src={project.logo}
                          alt={`${project.token} logo`}
                          className="mr-2 w-6 h-6"
                        />
                      )}
                      {project.token}
                    </td>
                    <td className="py-2 px-4 text-red-600">
                      {project.price_day_delta}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="py-2">
        <h2 className="text-xl font-semibold mb-2">Project Directory</h2>
        <div className="flex gap-4 justify-between">
          <div className="flex gap-4">
            <Filter
              placeholder="Search"
              filter={filter}
              setFilter={setFilter}
              className="flex-grow py-2 border border-gray-300"
            />
            <div className="hidden lg:inline-block flex gap-4">
              <button
                className="justify-end px-4 py-1 m-2 border-gray-300 dark:border-yellow-300 border align-right"
                onClick={() => setFilter('Blockchain')}
              >
                Blockchains
              </button>{' '}
              <button
                className="justify-end px-4 py-1 m-2 border-gray-300 dark:border-yellow-300 border align-right"
                onClick={() => setFilter('Stablecoin')}
              >
                Stablecoins
              </button>{' '}
              <button
                className="justify-end px-4 py-1 m-2 border-gray-300 dark:border-yellow-300 border align-right"
                onClick={() => setFilter('Lending Market')}
              >
                Lending Markets
              </button>{' '}
            </div>{' '}
          </div>
          <div className="flex justify-end">
            <button
              className="justify-end px-4 py-1 m-2 dark:border-yellow-500 bg-yellow-400 dark:bg-yellow-500 dark:text-black border align-right"
              onClick={() => setFilter('')}
            >
              Reset
            </button>
          </div>
        </div>
      </div>

      <ProjectDataTable rows={filteredProjects} />
    </>
  );
};

export default ProjectList;
