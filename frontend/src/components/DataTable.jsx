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
          minwidth: 100,
          pinned: 'left',
          cellClassName: 'sticky',
        },

        {
          field: 'liquidity_rate_formatted',
          headerName: 'APY',
          type: 'number',
          minwidth: 100,
          renderCell: (params) => `${params.value}%`,
          cellClassName: 'sticky',
        },
        {
          field: 'tvl_formatted',
          headerName: 'Supplied',
          type: 'number',
          minwidth: 150,
        },
        {
          field: 'collateral',
          headerName: 'Collateral',
          minwidth: 100,
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
    <Box sx={{ height: 'auto', width: '100%', overflow: 'hidden' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 20]}
        disableSelectionOnClick
        disableColumnResize={true}
        sx={{
          '& .sticky': {
            position: 'sticky',
            left: 0,
            backgroundColor: 'inherit',
            zIndex: 1,
          },
          '& .MuiDataGrid-root': {
            width: '100%',
            overflowX: 'auto',
          },
        }}
      />
    </Box>
  );
};

export default DataTable;
