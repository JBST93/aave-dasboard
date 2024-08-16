import { DataGrid } from '@mui/x-data-grid';
import useMediaQuery from '@mui/material/useMediaQuery';
import Box from '@mui/material/Box';

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
      cellClassName: 'text-center',
    },
    {
      field: 'symbol',
      headerName: 'Name',
      width: 150,
      headerClassName: 'font-bold dark:text-white',
      cellClassName: 'text-center',
    },
    {
      field: 'coins',
      headerName: 'Coins',
      width: 170,
      headerClassName: 'font-bold dark:text-white',
      cellClassName: 'text-center',
      renderCell: (params) => {
        const coins = params.value; // array of coins
        return (
          <div
            style={{
              justifyContent: 'center',
              alignItems: 'center',
              paddingTop: '10px',
              paddingBottom: '10px',
            }}
          >
            {coins.map((coin, index) => (
              <div key={index}>
                {coin[0]} ({coin[2]}%)
              </div>
            ))}
          </div>
        );
      },
    },
    {
      field: 'apy',
      headerName: 'APY',
      width: 100,
      headerClassName: 'font-bold dark:text-white',
      type: 'number',
      cellClassName: 'text-center',
    },
    {
      field: 'tvl',
      headerName: 'TVL (in $)',
      width: 170,
      headerClassName: 'font-bold dark:text-white',
      type: 'number',
      cellClassName: 'text-center',
    },
    {
      field: 'volume',
      headerName: 'Volume (in $)',
      width: 150,
      headerClassName: 'font-bold dark:text-white',
      type: 'number',
      cellClassName: 'text-center',
    },
    {
      field: 'chain',
      headerName: 'Chain',
      width: 150,
      headerClassName: 'font-bold dark:text-white',
      cellClassName: 'text-center',
    },
    {
      field: 'type',
      headerName: 'Type',
      width: 100,
      headerClassName: 'font-bold dark:text-white',
      cellClassName: 'text-center',
    },

    {
      field: 'base_apy',
      headerName: 'base APY',
      width: 100,
      headerClassName: 'font-bold dark:text-white',
      type: 'number',
      cellClassName: 'text-center',
    },
    {
      field: 'reward_apy',
      headerName: 'reward APY',
      width: 100,
      headerClassName: 'font-bold dark:text-white',
      type: 'number',
      cellClassName: 'text-center',
    },
  ];

  return (
    <Box
      sx={{
        backgroundColor: 'inherit',
        '& .MuiDataGrid-root': {
          '& .MuiDataGrid-cell': {
            display: 'flex',
            justifyContent: 'left',
            alignItems: 'center',
            textAlign: 'left',
          },
          '& .MuiDataGrid-columnHeader': {
            justifyContent: 'center',
            textAlign: 'center',
          },
        },
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
              pageSize: 100,
            },
          },
        }}
        rowsPerPageOptions={[5, 10, 20]}
        disableSelectionOnClick
        disableColumnResize={true}
        disableColumnMenu={true}
        getRowHeight={() => 'auto'}
        getRowClassName={() => 'DataGrid-row'}
        sx={{
          m: 2,
          border: 'black',
        }}
        classes={{
          root: 'bg-white dark:bg-gray-800 text-black dark:text-white',
          columnHeader: 'text-black dark:text-white bg-white dark:bg-gray-800',
          cell: 'text-black dark:text-white item-center',
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
