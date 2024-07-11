import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000', // Use environment variable or default to localhost for development
});

export default instance;
