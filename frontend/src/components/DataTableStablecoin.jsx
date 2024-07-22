import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { useMediaQuery } from '@mui/material';
import Box from '@mui/material/Box';

import '../App.css';

const DataTableStablecoin = ({ rows }) => {
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
        { field: 'sequentialId', headerName: '#', width: 50 },

        {
          field: 'token',
          headerName: 'Token',
          width: 110,
        },
        { field: 'supply_formatted', headerName: 'Supply', width: 120 },

        { field: 'price', headerName: 'Price', type: 'number' },

        {
          field: 'off_peg',
          headerName: 'Off Peg',
          type: 'number',
          sortable: true,
          width: 130,
        },

        {
          field: 'pegged_against',
          headerName: 'Against',
          width: 120,
        },
        {
          field: 'info',
          headerName: 'Type',
          width: 130,
        },
      ]
    : [
        { field: 'sequentialId', headerName: '#', width: 50 },

        {
          field: 'token',
          headerName: 'Token',
          width: 110,
        },
        { field: 'supply_formatted', headerName: 'Supply', width: 150 },

        { field: 'price_formatted', headerName: 'Price', type: 'number' },

        {
          field: 'off_peg',
          headerName: 'Off Peg',
          type: 'number',
          sortable: true,
          width: 130,
        },

        {
          field: 'pegged_against',
          headerName: 'Against',
          width: 120,
        },
        {
          field: 'info',
          headerName: 'Type',
          width: 130,
        },
        {
          field: 'link',
          headerName: 'LINK TO YIELD',
          width: 150,
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
        autoHeight
        slotProps={{
          loadingOverlay: {
            variant: 'skeleton',
            noRowsVariant: 'skeleton',
          },
        }}
        rows={rowsWithId}
        columns={columns}
        pageSize={5}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 50,
            },
          },
        }}
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
            'text-white dark:text-white bg-white dark:bg-gray-800',
          filler: 'bg-white dark:bg-gray-800',
        }}
      />
    </Box>
  );
};

export default DataTableStablecoin;
