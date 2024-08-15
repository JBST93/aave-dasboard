import { DataGrid } from '@mui/x-data-grid';
import useMediaQuery from '@mui/material/useMediaQuery';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import '../App.css';

const CurvePoolTable = ({ rows }) => {
  const validRows = Array.isArray(rows) ? rows : [];

  const isSmallScreen = useMediaQuery('(max-width:600px)');

  // Add sequential ID to each row
  const rowsWithId = validRows.map((row, index) => ({
    ...row,
    id: index + 1,
  }));

  const columns = [
    {
      field: 'id',
      headerName: '#',
      width: 50,
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'symbol',
      headerName: 'symbol',
      width: 150,
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'tvl',
      headerName: 'tvl',
      width: 300,
      headerClassName: 'font-bold dark:text-white',
    },
    {
      field: 'volume',
      headerName: 'Volume',
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
      field: 'apy',
      headerName: 'apy',
      width: 100,
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
        getRowHeight={() => 'auto'}
        getRowClassName={() => 'DataGrid-row'}
        sx={{ m: 2, border: 'black' }}
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

export default CurvePoolTable;
