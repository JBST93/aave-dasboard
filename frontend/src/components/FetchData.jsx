import React, { useEffect, useState } from 'react';
import axios from '../api/axios';

const FetchData = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/');
        console.log('Response from Flask:', response); // Log the response
        setMessage(response.data.message);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Message from Flask:</h1>
      <p>{message}</p>
    </div>
  );
};

export default FetchData;
