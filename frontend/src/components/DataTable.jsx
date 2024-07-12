import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { useMediaQuery } from '@mui/material';
import Box from '@mui/material/Box';

const DataTable = ({ rows }) => {
  const isSmallScreen = useMediaQuery('(max-width:600px)');

  const columns = isSmallScreen
    ? [
        {
          field: 'token',
          headerName: 'Market',
          width: 80,
          pinned: 'left',
        },
        {
          field: 'collateral',
          headerName: 'Collateral',
          width: 80,
        },
        {
          field: 'liquidity_rate_formatted',
          headerName: 'APY',
          type: 'number',
          width: 80,
          renderCell: (params) => `${params.value}%`,
        },
        {
          field: 'tvl_formatted',
          headerName: 'Supplied',
          type: 'number',
          width: 120,
        },
      ]
    : [
        { field: 'sequentialId', headerName: '#', width: 70 },
        {
          field: 'token',
          headerName: 'Market',
          width: 150,
          pinned: 'left',
        },
        { field: 'collateral', headerName: 'Collateral', width: 100 },
        { field: 'protocol', headerName: 'Project', width: 130 },
        { field: 'chain', headerName: 'Chain', width: 150 },
        {
          field: 'liquidity_rate_formatted',
          headerName: 'APY',
          type: 'number',
          width: 100,
          renderCell: (params) => `${params.value}%`,
        },
        {
          field: 'tvl_formatted',
          headerName: 'Amount Supplied',
          type: 'number',
          width: 150,
        },
        {
          field: 'humanized_timestamp',
          headerName: 'Last Updated',
          width: 160,
        },
      ];

  return (
    <Box sx={{ height: 'auto', width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 20]}
        disableSelectionOnClick
        sx={{
          '& .super-app-theme--header': {
            backgroundColor: 'rgba(255, 7, 0, 0.55)',
          },
          '& .super-app-theme--cell': {
            backgroundColor: 'rgba(255, 7, 0, 0.55)',
          },
        }}
      />
    </Box>
  );
};

export default DataTable;
