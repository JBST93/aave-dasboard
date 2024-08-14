import { useEffect, useState } from 'react';
import axios from 'axios';
import Filter from '../components/Filter';
import ProjectDataTable from '../components/ProjectDataTable';

import { Typography, Button } from '@mui/material';

import Box from '@mui/material/Box';

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

      {/* <div>
        Top 3 gainers / top 3 Losers
        // Table with 2 sides
        // 1 top component
        // 2 table inside the component
        // List inside each side of the component
              - Logo
              - Coin Name
              - % Change

        ⬆
        ⬇
      </div> */}

      <div className="py-2">
        {/* <Filter
          placeholder="Search by Project or Token Name"
          filter={filter}
          setFilter={setFilter}
          className="flex-grow py-2 border border-gray-300"
        /> */}
      </div>

      <ProjectDataTable rows={projects} />
    </>
  );
};

export default ProjectList;
