import { DataGrid } from '@mui/x-data-grid';
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
              className="mr-2 shrink-0 w-6 h-6"
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
      width: 100,
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'price',
      headerName: 'Price',
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
