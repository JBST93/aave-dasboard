import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { useMediaQuery } from '@mui/material';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
  stickyColumn: {
    position: 'sticky',
    left: 0,
    backgroundColor: '#121212', // Adjust based on your theme
    zIndex: 1,
  },
});

const DataTable = ({ rows }) => {
  const classes = useStyles();
  const isSmallScreen = useMediaQuery('(max-width:600px)');

  const mobileColumns = [
    {
      field: 'token',
      headerName: 'Market',
      width: 100,
      cellClassName: classes.stickyColumn,
    },
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
    { field: 'protocol', headerName: 'Project', width: 130 },
    { field: 'chain', headerName: 'Chain', width: 150 },
    { field: 'collateral', headerName: 'Collateral', width: 100 },
    { field: 'humanized_timestamp', headerName: 'Last Updated', width: 160 },
  ];

  const desktopColumns = [
    { field: 'sequentialId', headerName: '#', width: 70 },
    { field: 'token', headerName: 'Market', width: 100 },
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
    { field: 'humanized_timestamp', headerName: 'Last Updated', width: 160 },
  ];

  return (
    <div style={{ height: '100%', width: '100%', overflow: 'auto' }}>
      <DataGrid
        rows={rows}
        columns={isSmallScreen ? mobileColumns : desktopColumns}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 20 },
          },
        }}
        pageSizeOptions={[5, 10, 20, 50]}
        autoHeight
      />
    </div>
  );
};

export default DataTable;
