import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { useMediaQuery } from '@mui/material';
import Box from '@mui/material/Box';
import '../App.css';

const DataTable = ({ rows }) => {
  const isSmallScreen = useMediaQuery('(max-width:600px)');

  const handleImageError = (event) => {
    event.target.style.display = 'none';
  };

  // Add sequential ID to each row
  const rowsWithId = rows.map((row, index) => ({
    ...row,
    sequentialId: index + 1,
  }));

  const columns = isSmallScreen
    ? [
        {
          field: 'token',
          headerName: 'Market',
          width: 110,
        },
        { field: 'protocol', headerName: 'Project', width: 120 },
        { field: 'apy_sum', headerName: 'APY', type: 'number' },
        {
          field: 'liquidity_rate_formatted',
          headerName: 'Base APY',
          type: 'number',
        },
        {
          field: 'liquidity_reward_rate_formatted',
          headerName: 'Reward APY',
          type: 'number',
        },
        {
          field: 'tvl_formatted2',
          headerName: 'Supplied',
          type: 'number',
          sortable: true,
        },
        { field: 'collateral_formatted', headerName: 'Collateral' },
        { field: 'chain', headerName: 'Chain' },
        {
          field: 'humanized_timestamp',
          headerName: 'Last Updated',
        },
      ]
    : [
        { field: 'sequentialId', headerName: '#', width: 50 },
        {
          field: 'token',
          headerName: 'Market',
          width: 100,
        },
        { field: 'collateral_formatted', headerName: 'Collateral', width: 100 },
        { field: 'protocol', headerName: 'Project', width: 130 },
        { field: 'apy_sum', headerName: 'APY', type: 'number', width: 90 },

        { field: 'chain', headerName: 'Chain', width: 100 },
        {
          field: 'liquidity_rate_formatted',
          headerName: 'Base APY',
          type: 'number',
          width: 100,
        },
        {
          field: 'liquidity_reward_rate_formatted',
          headerName: 'Reward APY',
          type: 'number',
          width: 105,
        },

        {
          field: 'tvl_formatted2',
          headerName: 'Amount Supplied',
          type: 'number',
          sortable: true,
          width: 150,
        },
        {
          field: 'humanized_timestamp',
          headerName: 'Last Updated',
          width: 160,
        },
      ];

  return (
    <Box
      sx={{
        backgroundColor: 'inherit',
      }}
      className="bg-white dark:bg-gray-800 text-black dark:text-white"
    >
      <DataGrid
        rows={rowsWithId}
        columns={columns}
        pageSize={5}
        pagination
        rowsPerPageOptions={[5, 10, 20]}
        disableSelectionOnClick
        disableColumnResize={true}
        disableColumnMenu={true}
        getRowClassName={() => 'DataGrid-row'}
        classes={{
          root: 'bg-white dark:bg-gray-800 text-black dark:text-white',
          columnHeader: 'text-black dark:text-white bg-white dark:bg-gray-800',
          cell: 'text-black dark:text-white',
          row: 'bg-white dark:bg-gray-800',
          footerContainer:
            'text-black dark:text-white bg-white dark:bg-gray-800',
          filler: 'bg-white dark:bg-gray-800',
        }}
      />
    </Box>
  );
};

export default DataTable;
