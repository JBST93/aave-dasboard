import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://defi-dashboard-99d015fc546e.herokuapp.com', // Use environment variable or default to localhost for development
});

export default instance;
