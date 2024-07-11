import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';

const columns = [
  { field: 'sequentialId', headerName: '', width: 70 },
  { field: 'token', headerName: 'Market', width: 100 },
  { field: 'collateral', headerName: 'Collateral', width: 100 },

  { field: 'protocol', headerName: 'Project', width: 130 },
  { field: 'chain', headerName: 'Chain', width: 150 },
  {
    field: 'liquidity_rate_formatted',
    headerName: 'APY',
    type: 'number',
    width: 80,
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

export default function DataTable({ rows }) {
  return (
    <div style={{ height: '100%', width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 20 },
          },
        }}
        pageSizeOptions={[5, 50]}
      />
    </div>
  );
}
