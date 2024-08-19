import { DataGrid } from '@mui/x-data-grid';
import Tooltip from '@mui/material/Tooltip'; // Import Tooltip component

import useMediaQuery from '@mui/material/useMediaQuery';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import '../App.css';

const DataTable = ({ rows }) => {
  const validRows = Array.isArray(rows) ? rows : [];

  const isSmallScreen = useMediaQuery('(max-width:600px)');

  // Add sequential ID to each row
  const rowsWithId = validRows.map((row, index) => ({
    ...row,
    id: index + 1, // DataGrid requires a unique `id` field
    price_day_delta_color:
      row.price_day_delta > 0
        ? 'green'
        : row.price_day_delta < 0
        ? 'red'
        : 'inherit',
  }));

  const columns = [
    {
      field: 'id',
      headerName: '#',
      width: 50,
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'token',
      headerName: 'Token',
      width: 150,
      renderCell: (params) => (
        <div className="flex items-center dark:text-white">
          {params.row.logo && (
            <img
              src={params.row.logo}
              alt={`${params.row.token} logo`}
              className="mr-2 shrink-0 w-6 h-6 text-center"
            />
          )}
          {params.value}
        </div>
      ),
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'description',
      headerName: 'Description',
      width: 300,
      headerClassName: 'font-bold dark:text-white',
      renderCell: (params) => (
        <Tooltip
          title={params.value}
          arrow
        >
          <span className="truncate block max-w-xs">
            {params.value.length > 100
              ? `${params.value.substring(0, 100)}...`
              : params.value}
          </span>
        </Tooltip>
      ),
    },
    {
      field: 'project',
      headerName: 'Project',
      width: 150,
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'type',
      headerName: 'Type',
      width: 150,
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'price',
      headerName: 'Price',
      type: 'number',
      headerAlign: 'left',

      align: 'left',
      width: 100,
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'price_day_delta',
      headerName: '24H Price',
      width: 100,
      renderCell: (params) => (
        <span style={{ color: params.row.price_day_delta_color }}>
          {params.value}%
        </span>
      ),
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'marketCap',
      headerName: 'MarketCap',
      width: 150,
      align: 'left',
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'website',
      headerName: 'Website',
      width: 150,
      renderCell: (params) => (
        <Button
          variant="outlined"
          href={params.value}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-teal-500 hover:bg-blue-700 text-white"
        >
          Website
        </Button>
      ),
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'forum',
      headerName: 'Forum',
      width: 150,
      renderCell: (params) =>
        params.value !== '' ? (
          <Button
            variant="outlined"
            href={params.value}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-green-500 hover:bg-green-700 text-white"
          >
            Forum
          </Button>
        ) : (
          ''
        ),
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'update_status',
      headerName: 'Update Status',
      width: 150,
      renderCell: (params) => {
        const timestamp = params.row.timestamp;
        const currentTime = new Date();
        let circleColor = '';
        let displayText = '';

        if (timestamp === 'NEW') {
          displayText = 'Recently added';
        } else {
          const dataTime = new Date(timestamp);
          const timeDifference = (currentTime - dataTime) / (1000 * 60 * 60); // Time difference in hours

          if (timeDifference < 1) {
            circleColor = 'bg-green-500';
          } else if (timeDifference <= 24) {
            circleColor = 'bg-yellow-500';
          } else {
            circleColor = 'bg-red-500';
          }
        }

        return (
          <div className="flex items-center">
            {circleColor && (
              <span
                className={`w-3 h-3 rounded-full mr-2 ${circleColor}`}
              ></span>
            )}
            <span>{displayText}</span>
          </div>
        );
      },
      headerClassName: 'font-bold dark:text-white',
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
        getRowHeight={() => 60}
        getRowClassName={() => 'DataGrid-row'}
        sx={{
          m: 2,
          border: 'black',
          '& .MuiDataGrid-sortIcon': {
            opacity: 'inherit !important',
            color: 'inherit',
          },
          '& .MuiDataGrid-row:hover': {
            backgroundColor: 'rgba(0, 0, 0, 0.05)', // Row hover effect
            cursor: 'pointer',
          },
        }}
        classes={{
          root: 'bg-white dark:bg-gray-800 text-black dark:text-white',
          columnHeader: 'text-black dark:text-white bg-white dark:bg-gray-800',
          cell: 'text-black dark:text-white text-center flex items-center justify-center',
          row: 'bg-white dark:bg-gray-800',
          footerContainer:
            'text-white dark:text-white bg-white dark:bg-gray-800',
          filler: 'bg-white dark:bg-gray-800',
          sortIcon: 'black dark:white',
        }}
      />
    </Box>
  );
};

export default DataTable;
