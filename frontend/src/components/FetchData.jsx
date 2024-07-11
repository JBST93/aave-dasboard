import React, { useEffect, useState } from 'react';
import axios from '../api/axios';
import DataTable from './DataTable';
import Filter from './Filter'; // Import the Filter component

const FetchData = () => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState(''); // State for the filter input

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/');
        console.log('Response from Flask:', response); // Log the response

        // Transform data to include sequential IDs
        const transformedData = response.data.map((item, index) => ({
          ...item,
          sequentialId: index + 1, // Add a sequential ID starting from 1
          id: item.id, // Ensure each row has a unique `id` field for DataGrid
        }));

        setData(transformedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  // Filter the data based on the filter input
  const filteredData = data.filter((item) =>
    item.token.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <Filter
        filter={filter}
        setFilter={setFilter}
      />{' '}
      <DataTable rows={filteredData} />
    </div>
  );
};

export default FetchData;
