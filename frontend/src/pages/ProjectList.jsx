import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Filter from '../components/Filter';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import { Typography, Button } from '@mui/material';

import Box from '@mui/material/Box';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [filter, setFilter] = useState();
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

      <div className="py-2">
        <Filter
          placeholder="Search Project or Token"
          filter={filter}
          setFilter={setFilter}
          className="flex-grow py-2 border border-gray-300"
        />
      </div>
      <Box className=" dark:text-white">
        <TableContainer
          component={Paper}
          className="bg-red-100 dark:bg-gray-900 shadow-md rounded-lg"
        >
          <Table className="dark:text-white">
            <TableHead className="bg-grey-500 dark:bg-gray-800  dark:text-white">
              <TableRow>
                <TableCell className="font-bold dark:text-white">#</TableCell>
                <TableCell className="font-bold dark:text-white">
                  Project
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  Description
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  Governance
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  Type
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  Token
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  Price
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  MarketCap
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  Audited
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  Website
                </TableCell>
                <TableCell className="font-bold dark:text-white">
                  Forum
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {projects.map((project, index) => (
                <TableRow
                  key={index}
                  className="hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-white"
                >
                  <TableCell className="dark:text-white">{index + 1}</TableCell>
                  <TableCell className="dark:text-white">
                    {project.project}
                  </TableCell>
                  <TableCell className="dark:text-white">
                    {project.description}
                  </TableCell>
                  <TableCell className="dark:text-white">
                    {project.governance}
                  </TableCell>
                  <TableCell className="dark:text-white">
                    {project.type}
                  </TableCell>
                  <TableCell className="dark:text-white">
                    {project.token}
                  </TableCell>
                  <TableCell className="dark:text-white">
                    {project.price}
                  </TableCell>
                  <TableCell className="dark:text-white">
                    {project.marketCap}
                  </TableCell>
                  <TableCell className="dark:text-white">
                    {project.audited}
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="outlined"
                      href={project.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-teal-500 hover:bg-blue-700 text-white"
                    >
                      Website
                    </Button>
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="outlined"
                      href={project.forum}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-green-500 hover:bg-green-700 text-white"
                    >
                      Forum
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </>
  );
};

export default ProjectList;
