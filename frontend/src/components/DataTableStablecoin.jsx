// import React from 'react';
// import { DataGrid } from '@mui/x-data-grid';
// import { useMediaQuery } from '@mui/material';
// import Box from '@mui/material/Box';

// import '../App.css';

// const DataTableStablecoin = ({ rows }) => {
//   const isSmallScreen = useMediaQuery('(max-width:600px)');

//   const handleImageError = (event) => {
//     event.target.style.display = 'none';
//   };

//   // Add sequential ID to each row
//   const rowsWithId = rows.map((row, index) => ({
//     ...row,
//     sequentialId: index + 1,
//   }));

//   // Define all columns
//   const allColumns = [
//     { field: 'sequentialId', headerName: '#', width: 50 },
//     { field: 'token', headerName: 'Token', width: 110 },
//     { field: 'supply_formatted', headerName: 'Supply', width: 150 },
//     { field: 'price_usd_formatted', headerName: 'Price (USD)', type: 'number' },
//     { field: 'price_peg_formatted', headerName: 'Price (LCY)', type: 'number' },
//     {
//       field: 'off_peg',
//       headerName: 'Off Peg',
//       type: 'number',
//       sortable: true,
//       width: 130,
//     },
//     { field: 'pegged_against', headerName: 'Against', width: 120 },
//     { field: 'info', headerName: 'Decentralisation', width: 130 },
//   ];

//   // Define columns to display on small screens
//   const smallScreenColumns = [
//     { field: 'sequentialId', headerName: '#', width: 50 },
//     { field: 'token', headerName: 'Token', width: 110 },
//     { field: 'supply_formatted', headerName: 'Supply', width: 120 },
//     { field: 'price_usd_formatted', headerName: 'Price', type: 'number' },
//     { field: 'price_peg_formatted', headerName: 'Price (LCY)', type: 'number' },
//     {
//       field: 'off_peg',
//       headerName: 'Off Peg',
//       type: 'number',
//       sortable: true,
//       width: 130,
//     },
//     { field: 'pegged_against', headerName: 'Against', width: 120 },
//     { field: 'info', headerName: 'Decentralisation', width: 130 },
//   ];

//   // Determine columns based on screen size
//   const columns = isSmallScreen ? smallScreenColumns : allColumns;

//   return (
//     <Box
//       sx={{
//         backgroundColor: 'inherit',
//       }}
//       className="bg-white dark:bg-gray-800 text-black dark:text-white"
//     >
//       <DataGrid
//         autoHeight
//         autoWidth
//         slotProps={{
//           loadingOverlay: {
//             variant: 'skeleton',
//             noRowsVariant: 'skeleton',
//           },
//         }}
//         rows={rowsWithId}
//         columns={columns}
//         pageSize={5}
//         initialState={{
//           pagination: {
//             paginationModel: {
//               pageSize: 50,
//             },
//           },
//         }}
//         rowsPerPageOptions={[5, 10, 20]}
//         disableSelectionOnClick
//         disableColumnResize={true}
//         disableColumnMenu={true}
//         getRowClassName={() => 'DataGrid-row'}
//         classes={{
//           root: 'bg-white dark:bg-gray-800 text-black dark:text-white',
//           columnHeader: 'text-black dark:text-white bg-white dark:bg-gray-800',
//           cell: 'text-black dark:text-white',
//           row: 'bg-white dark:bg-gray-800',
//           footerContainer:
//             'text-white dark:text-white bg-white dark:bg-gray-800',
//           filler: 'bg-white dark:bg-gray-800',
//         }}
//       />
//     </Box>
//   );
// };

// export default DataTableStablecoin;
