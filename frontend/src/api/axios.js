import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Replace with your Flask backend URL if different
});

export default instance;
