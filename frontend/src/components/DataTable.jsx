import { DataGrid } from '@mui/x-data-grid/DataGrid';
import useMediaQuery from '@mui/material/useMediaQuery';
import Box from '@mui/material/Box';
import '../App.css';
import { NetworkIcon } from '@web3icons/react';

const DataTable = ({ rows }) => {
  const validRows = Array.isArray(rows) ? rows : [];

  const isSmallScreen = useMediaQuery('(max-width:600px)');

  // Add sequential ID to each row
  const rowsWithId = validRows.map((row, index) => ({
    ...row,
    sequentialId: index + 1,
  }));

  const columns = isSmallScreen
    ? [
        { field: 'market', headerName: 'Market', width: 110 },
        { field: 'project', headerName: 'Project', width: 120 },
        { field: 'apy_sum', headerName: 'APY', type: 'number' },
        {
          field: 'tvl_formatted2',
          headerName: 'Supplied',
          type: 'number',
          sortable: true,
          width: 130,
        },
        {
          field: 'yield_rate_base',
          headerName: 'Base APY',
          type: 'number',
          width: 120,
        },
        {
          field: 'chain',
          headerName: 'Chain',
          width: 120,
          renderCell: (params) => {
            const symbol = params.value?.toLowerCase() || 'default';
            return (
              <div className="flex items-center">
                <NetworkIcon
                  network={symbol}
                  variant="branded"
                />
                {params.value} {/* Cell Value */}
              </div>
            );
          },
        },

        {
          field: 'yield_rate_reward_formatted',
          headerName: 'Reward APY',
          type: 'number',
          width: 130,
        },
        {
          field: 'information_formatted',
          headerName: 'Information',
          width: 300,
        },
        {
          field: 'humanized_timestamp',
          headerName: 'Last Updated',
        },
      ]
    : [
        { field: 'sequentialId', headerName: '#', width: 50 },
        { field: 'market', headerName: 'Market', width: 100 },

        { field: 'project', headerName: 'Project', width: 130 },
        { field: 'apy_sum', headerName: 'APY', type: 'number', width: 90 },
        {
          field: 'chain',
          headerName: 'Chain',
          width: 100,
          renderCell: (params) => {
            const symbol = params.value?.toLowerCase() || 'default';
            return (
              <div className="flex items-center">
                <NetworkIcon
                  network={symbol}
                  variant="mono"
                />
                {params.value} {/* Cell Value */}
              </div>
            );
          },
        },
        {
          field: 'tvl_formatted2',
          headerName: 'Amount Supplied',
          type: 'number',
          sortable: true,
          width: 150,
        },

        {
          field: 'information_formatted',
          headerName: 'Information',
          width: 200,
        },
        {
          field: 'yield_rate_base',
          headerName: 'Base APY',
          type: 'number',
          width: 100,
        },
        {
          field: 'yield_rate_reward_formatted',
          headerName: 'Reward APY',
          type: 'number',
          width: 105,
        },
        {
          field: 'humanized_timestamp',
          headerName: 'Last Updated',
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

export default DataTable;
