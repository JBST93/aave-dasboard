import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { useMediaQuery } from '@mui/material';
import Box from '@mui/material/Box';
import '../App.css';

const DataTable = ({ rows }) => {
  const isSmallScreen = useMediaQuery('(max-width:600px)');

  const columns = isSmallScreen
    ? [
        {
          field: 'token',
          headerName: 'Market',
          cellClassName: 'sticky',
          headerClassName: 'sticky',
        },
        { field: 'protocol', headerName: 'Project' },
        {
          field: 'liquidity_rate_formatted',
          headerName: 'Base APY',
          type: 'number',
          cellClassName: 'sticky',
        },
        {
          field: 'liquidity_reward_rate',
          headerName: 'Reward APY',
        },
        {
          field: 'tvl_formatted2',
          headerName: 'Supplied',
          type: 'number',
          sortable: true,
          cellClassName: 'sticky',
        },
        { field: 'collateral', headerName: 'Collateral' },

        { field: 'chain', headerName: 'Chain' },
        {
          field: 'humanized_timestamp',
          headerName: 'Last Updated',
        },
      ]
    : [
        { field: 'sequentialId', headerName: '#', width: 70 },
        {
          field: 'token',
          headerName: 'Market',
          width: 150,
        },
        { field: 'collateral', headerName: 'Collateral', width: 100 },
        { field: 'protocol', headerName: 'Project', width: 130 },
        { field: 'chain', headerName: 'Chain', width: 130 },
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
        width: isSmallScreen ? '80vw' : '100%',
        backgroundColor: 'inherit',
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 20]}
        disableSelectionOnClick
        disableColumnResize={true}
        className="DataGrid-container"
        getRowClassName={() => 'DataGrid-row'}
        sx={{
          '& .sticky': {
            position: 'sticky',
            left: 0,
            backgroundColor: 'inherit',
            zIndex: 1,
          },
        }}
      />
    </Box>
  );
};

export default DataTable;
