import axios from 'axios';

const instance = axios.create({
  baseURL: import.meta.env.REACT_APP_API_URL, // Use the environment variable
});

export default instance;
