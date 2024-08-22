import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Filter from '../components/Filter';
import ProjectDataTable from '../components/ProjectDataTable';

import { Typography } from '@mui/material';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [filter, setFilter] = useState('');
  const [error, setError] = useState('');

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
        <h1 className="md:text-4xl text-xl font-bold">Project Directory</h1>
      </div>

      <div className="mb-4 text-center md:text-left">
        <p className="md:text-lg text-base text-left pt-1">
          Navigate the world of digital assets with our comprehensive directory.
          Explore real-time data on your favorite cryptocurrencies, compare
          market performance, and stay ahead with the latest updates.
        </p>
        <p className="text-sm text-left text-gray-500">
          Disclaimer: We do not vet or audit the platforms we aggregate. Always
          conduct your own due diligence before making any investment decisions.
        </p>
      </div>

      <div className="flex flex-col md:flex-row gap-4 mb-4">
        <div>
          <h2 className="text-lg font-semibold mb-2 ">⬆ Top Daily Gainers</h2>
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

      <div className="py-2">
        <h2 className="text-xl font-semibold mb-2">Project Directory</h2>

        <Filter
          placeholder="Search"
          filter={filter}
          setFilter={setFilter}
          className="flex-grow py-2 border border-gray-300"
        />
      </div>

      <ProjectDataTable rows={filteredProjects} />
    </>
  );
};

export default ProjectList;
